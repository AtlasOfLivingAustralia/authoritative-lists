import logging
import argparse
import os
import requests
import csv

logger = logging.getLogger("nsw_threatened_species")
logger.setLevel(logging.INFO)
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
logger.addHandler(console)

FIELDS = [ 'scientificName', 'vernacularName', 'kingdom', 'family', 'status', 'countryStatus', 'profileID', 'threats', 'distribution', 'profile']

OEH_ODATA = "https://data.bionet.nsw.gov.au/biosvcapp/odata"
THREATENED = OEH_ODATA + "/ThreatenedBiodiversity_Species"


def isPresent(value):
    if value == None:
        return False
    if type(value) == str:
        return len(value) > 0 and value != 'None' and value != 'N/A'
    return True

def getValue(value, defaultValue = None):
    return value if isPresent(value) else defaultValue

def translate(row: dict):
    val = {}
    val['scientificName'] = getValue(row.get('scientificName'))
    val['vernacularName'] = getValue(row.get('vernacularName'))
    val['kingdom'] = getValue(row.get('kingdom'))
    val['family'] = getValue(row.get('family'))
    val['status'] = getValue(row.get('stateConservation'))
    val['countryStatus'] = getValue(row.get('countryConservation'))
    val['profileID'] = getValue(row.get('profileID'))
    val['threats'] = getValue(row.get('threats'))
    val['distribution'] = getValue(row.get('distribution'))
    return val


parser = argparse.ArgumentParser(description='Get NSW Threatend Species Data from OEH')
parser.add_argument('-o', '--output', type=str, help='Output directory', default='.')

args = parser.parse_args()

output_dir = args.output
species_csv = os.path.join(output_dir, "species.csv")

url = THREATENED + "?count=true"

with open(species_csv, "w") as ofile:
    ocsv = csv.DictWriter(ofile, FIELDS)
    ocsv.writeheader()
    while url:
        logger.info("Retrieving " + url)
        response = requests.get(url)
        if response.status_code != 200:
            logger.error("Unable to retrive " + url)
            exit(1)
        species = response.json()
        count = species.get('@odata.count')
        logger.info("Retrieved " + str(count) + " rows")
        for row in species.get('value'):
            trow = translate(row)
            ocsv.writerow(trow)
        url = species.get('@odata.nextLink')