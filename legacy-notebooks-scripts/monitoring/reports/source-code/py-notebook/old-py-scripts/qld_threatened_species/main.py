import logging
import argparse
import csv
import importlib.resources


logger = logging.getLogger("qld_threatened_species")
logger.setLevel(logging.INFO)
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
logger.addHandler(console)

SENSITIVE_FIELDS = [ 'scientificName', 'scientificNameAuthorship', 'vernacularName', 'kingdom', 'class', 'family', 'status', 'statusDescription', 'countryStatus', 'countryStatusDescription', 'significant', 'endemicity', 'taxonID' ]
CONSERVATION_FIELDS = [ 'scientificName', 'scientificNameAuthorship', 'vernacularName', 'kingdom', 'class', 'family', 'status', 'sourceStatus', 'statusCode', 'significant', 'endemicity', 'taxonID' ]

KINGDOMS = { 'animals': 'Animalia', 'bacteria': 'Bacteria', 'chromists': 'Chromista', 'fungi': 'Fungi', 'plants': 'Plantae', 'protozoans': 'Protozoa' }
CLASSES = { 'amphibians': 'Amphibia', 'arachnids': 'Arachnida', 'birds': 'Aves', 'euglenoids': 'Euglenophyceae', 'insects': 'Insecta', 'land plants': 'Equisetopsida', 'liverworts': None, 'malacostracans': None, 'mammals': 'Mammalia', 'ray-finned fishes': 'Actinopterygii', 'reptiles': 'Reptilia', 'slime moulds': None, 'uncertain': None }

def isPresent(value):
    if value == None:
        return False
    if type(value) == str:
        return len(value) > 0 and value != 'None' and value != 'N/A'
    return True

def _getValue(value, defaultValue = None):
    return value if isPresent(value) else defaultValue

def getValue(record, *args):
    for a in args:
        value = _getValue(record.get(a))
        if value is not None:
            return value
    return None

def translate(row: dict, status: dict, source_status: dict, conservation: bool):
    val = {}
    val['scientificName'] = getValue(row, 'Scientific name', 'Scientific_name')
    val['scientificNameAuthorship'] = getValue(row, 'Taxon author', 'Taxon_author')
    val['vernacularName'] = getValue(row, 'Common name', 'Common_name')
    kingdom = getValue(row, 'Kingdom')
    val['kingdom'] = KINGDOMS.get(kingdom)
    clazz = getValue(row, 'Class')
    val['class'] = CLASSES.get(clazz)
    val['family'] = getValue(row, 'Family')
    if conservation:
        s = getValue(row, 'NCA status', 'NCA_status')
        if s is not None:
            val['statusCode'] = s
            val['status'] = status.get(('NCA_status', s))
            val['sourceStatus'] = source_status.get(('NCA_status', s))
        else:
            s = getValue(row, 'EPBC status', 'EPBC_status')
            if s is not None:
                val['statusCode'] = s
                val['status'] = status.get(('EPBC_status', s))
                val['sourceStatus'] = source_status.get(('EPBC_status', s))
    else:
        s = getValue(row, 'NCA status', 'NCA_status')
        val['status'] = s
        val['statusDescription'] = status.get(('NCA_status', s))
        s = getValue(row, 'EPBC status', 'EPBC_satus')
        val['countryStatus'] = s
        val['countryStatusDescription'] = status.get(('EPBC_status', s))
    s = getValue(row, 'Endemicity')
    val['endemicity'] = status.get(('Endemicity', s), s)
    val['taxonID'] = getValue(row, 'Taxon Id', 'Taxon_Id')
    val['significant'] = getValue(row, 'Significant')
    return val

def read_status(file):
    scsv = csv.DictReader(sfile)
    status = { (row['Field'], row['Code']): row.get('Code_description') for row in scsv }
    return status

parser = argparse.ArgumentParser(description='Get Queensland Threatend Species Data from Wildnet')
parser.add_argument('-o', '--output', type=str, help='Output file', default='./species.csv')
parser.add_argument('-e', '--encoding', type=str, help='Input file encoding', default='utf-8')
parser.add_argument('-s', '--status', type=str, help='Status vocabulary file')
parser.add_argument('--conservation', action='store_true', help='The output is a conservation list (a sensitive species list if empty)')
parser.add_argument('--include-empty', dest='include_empty', action='store_true', help='Include rows with empty status entries')
parser.add_argument('source', metavar="FILE", nargs='+', type=str, help='Source files')
args = parser.parse_args()

include_empty = args.include_empty
conservation = args.conservation
input_encoding = args.encoding
output_encoding = 'utf-8'
output_csv = args.output

with importlib.resources.open_text('resources', 'sensitive-species-status-codes.csv') as sfile:
    source_status = read_status(sfile)
if args.status is not None:
    with open(args.status, 'r') as sfile:
        status = read_status(sfile)
elif conservation:
    with importlib.resources.open_text('resources', 'conservation-species-status-codes.csv') as sfile:
        status = read_status(sfile)
else:
    status = source_status

with open(output_csv, "w", encoding=output_encoding) as ofile:
    ocsv = csv.DictWriter(ofile, CONSERVATION_FIELDS if conservation else SENSITIVE_FIELDS)
    ocsv.writeheader()
    for file in args.source:
        with open(file, 'r', encoding=input_encoding) as ifile:
            icsv = csv.DictReader(ifile)
            for line in icsv:
                row = translate(line, status, source_status, conservation)
                if include_empty or row.get('status') is not None:
                    ocsv.writerow(row)
