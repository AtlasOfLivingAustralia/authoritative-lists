# ---------------------------------------------------------------------------
# vocab.py
#
# This script contains all of the variables that don't change for the lists
# update that will eventually run weekly.
#
# NOTE: Do not include SA - they manage their own lists.
# ---------------------------------------------------------------------------

authorize_url = (
    "https://auth-secure.auth.ap-southeast-2.amazoncognito.com/oauth2/authorize"
)
token_url = "https://auth-secure.auth.ap-southeast-2.amazoncognito.com/oauth2/token"

# URLs for ALA lists for test and production
get_listsProd = "https://api.ala.org.au/specieslist/ws/speciesListItems/"
get_listsTest = "https://lists-test.ala.org.au/ws/speciesListItems/"  # -ws.
# upload_listsTest = "https://lists-develop-ws.dev.ala.org.au/v2/upload"
# ingest_listsTest = "https://lists-develop-ws.dev.ala.org.au/v2/ingest/"
# progress_listsTest = "https://lists-develop-ws.dev.ala.org.au/v2/ingest/{speciesListID}/progress"
# get_listsTest = "https://lists-develop-ws.dev.ala.org.au/v1/speciesListItems/" # was v2
"""
upload_listsTest = "https://lists-ws.test.ala.org.au/v2/upload"
ingest_listsTest = "https://lists-ws.test.ala.org.au/v2/ingest/"
progress_listsTest = "https://lists-ws.test.ala.org.au/v2/ingest/{speciesListID}/progress"
get_listsTest = "https://lists-ws.test.ala.org.au/v2/speciesListItems/"
"""
urlSuffix = "?max=10000&includeKVP=true"

state_abbreviations = {
    "ACT": "Australian Capital Territory",
    "NSW": "New South Wales",
    "NT": "Northern Territory",
    "QLD": "Queensland",
    "VIC": "Victoria",
    "TAS": "Tasmania",
    "WA": "Western Australia",
    "EPBC": "EPBC",
}

# urls for conservation lists
conservation_list_urls = {
    "ACT": [
        "https://www.data.act.gov.au/resource/9ikf-qahj.json"
    ],  # or is this correct?
    "NSW": ["https://data.bionet.nsw.gov.au/biosvcapp/odata/SpeciesNames"],
    "NT": [
        "https://ftp-dlrm.nt.gov.au/main.html?download&weblink=1e717d654034af5e5f840d2ba3fd9187&realfilename=NT_Species_List_Fauna.xlsx",  # fauna
        "https://ftp-dlrm.nt.gov.au/main.html?download&weblink=60088e77ecef6c6cbf515c299f07a420&realfilename=NT_Species_List_Flora.xlsx",
    ],  # flora
    "QLD": ["https://apps.des.qld.gov.au/data-sets/wildlife/wildnet/species.csv"],
    "VIC": ["https://vba.biodiversity.vic.gov.au/vba/downloadVSC.do"],
    "TAS": ["TasThreatSpecies.xlsx"],
    "WA": ["https://www.dbca.wa.gov.au/management/threatened-species-and-communities"],
    "EPBC": [
        "https://data.gov.au/data/dataset/threatened-species-state-lists/resource/78401dce-1f40-49d3-92c4-3713d6e34974"
    ],
}

# urls for relevant sensitive lists
sensitive_list_urls = {
    "NSW": ["https://data.bionet.nsw.gov.au/biosvcapp/odata/SpeciesNames"],
    "QLD": [
        "https://apps.des.qld.gov.au/data-sets/wildlife/wildnet/qld-confidential-species.csv"
    ],
    "VIC": ["https://vba.biodiversity.vic.gov.au/vba/downloadVSC.do"],
    "WA": ["https://www.dbca.wa.gov.au/management/threatened-species-and-communities"],
}

# urls for all species in state/territory
all_species_urls = {
    "ACT": ["data/lists-from-ste-terr/ACT_taxa_table.csv"],  # might switch to URL
    "NSW": ["https://data.bionet.nsw.gov.au/biosvcapp/odata/SpeciesNames"],
    "NT": [
        "data/lists-from-ste-terr/NTSpeciesList_17_9_2025.csv"
    ],  # might switch to URL
    "QLD": ["https://apps.des.qld.gov.au/data-sets/wildlife/wildnet/species.csv"],
    "SA": [
        "https://www.environment.sa.gov.au/topics/science/information-and-data/census-of-sa-vertebrates",
        "https://data.environment.sa.gov.au/Content/Publications/vascular-plants-bdbsa-taxonomy.xlsx",
        "https://data.environment.sa.gov.au/Content/Publications/other-taxonomic-groups-bdbsa-taxonomy.xlsx",
    ],
    "TAS": [
        "data/lists-from-ste-terr/TasmanianNaturalValuesAtlas.xlsx"
    ],  # might switch to URL
    "VIC": ["https://vba.biodiversity.vic.gov.au/vba/downloadVSC.do"],
    "WA": ["data/lists-from-ste-terr/WAFloraList2025.csv"],  # might switch to URL
}

# all the state lists that are automatically checked every week
conservation_lists = ["ACT", "EPBC", "NSW", "NT", "QLD", "TAS", "VIC", "WA"]

sensitive_lists = ["NSW", "QLD", "VIC", "WA"]

all_conservation_lists = ["ACT", "EPBC", "NSW", "NT", "QLD", "TAS", "VIC", "WA"]

all_sensitive_lists = ["ACT", "BirdLife", "NSW", "NT", "QLD", "TAS", "VIC", "WA"]

all_species_ste_terr = ["ACT", "NSW", "NT", "QLD", "SA", "TAS", "VIC", "WA"]  #

all_conservation_druid_test = "dr23326"

all_conservation_druid_prod = ""

all_sensitive_druid = "dr23005"

all_sensitive_druid_prod = ""

all_species_ste_terr_druid_test = "dr23335"

all_species_ste_terr_druid_prod = ""

# ALA list ids for all conservation authoritative lists on test
list_ids_conservation_test = {
    "ACT": "dr649",
    "NSW": "dr650",
    "NT": "dr651",
    "QLD": "dr652",
    "TAS": "dr654",
    "VIC": "dr655",
    "WA": "dr2201",
    "EPBC": "dr656",
}

# ALA list ids for all conservation authoritative lists on prod
list_ids_conservation_prod = {
    "ACT": "dr649",
    "NSW": "dr650",
    "NT": "dr651",
    "QLD": "dr652",
    "TAS": "dr654",
    "VIC": "dr655",
    "WA": "dr2201",
    "EPBC": "dr656",
}

# ALA list ids for all sensitive authoritative lists on test we are updating
list_ids_sensitive_test = {
    "NSW": "dr18457",
    "QLD": "dr18404",
    "VIC": "dr18669",
    "WA": "dr18406",
    "ACT": "dr2627",
    "NT": "dr18690",
    "TAS": "dr18692",
    "BirdLife": "dr22224",
    "All": "dr23005",
}

# ALA list ids for all sensitive authoritative lists on test we are updating
list_ids_sensitive_prod = {
    "NSW": "dr487",
    "QLD": "dr493",
    "VIC": "dr490",
    "WA": "dr467",
    "ACT": "dr2627",
    "NT": "dr492",
    "TAS": "dr491",
    "BirdLife": "dr494",
}

list_ids_species_dummy_test = {
    "ACT": "dr23327",
    "NSW": "dr23328",
    "NT": "dr23329",
    "QLD": "dr23330",
    "SA": "dr23331",
    "TAS": "dr23332",
    "VIC": "dr23333",
    "WA": "dr23334",
}


list_names_sensitive_test = {
    "NSW": "NSW Sensitive Species List",
    "QLD": "Queensland Confidential Species",
    "VIC": "Victorian Restricted Species List",
    "WA": "Western Australia: Sensitive Species",
    "All": "All Sensitive Australian Species",
}

list_names_conservation_test = {
    "ACT": "Australian Capital Territory : Conservation Status",
    "NSW": "New South Wales : Conservation Status",
    "NT": "Northern Territory : Conservation Status",
    "QLD": "Queensland : Conservation Status",
    "TAS": "Tasmania : Conservation Status",
    "VIC": "Victoria : Conservation Status",
    "WA": "Western Australia: Conservation Status",
    "EPBC": "EPBC Act Threatened Species",
    "All": "All Threatened Australian Species",
}

list_names_all_species_state_test = {
    "ACT": "ACT Species List (for test)",
    "NSW": "NSW Species List (for test)",
    "NT": "NT Species List (for test)",
    "QLD": "QLD Species List (for test)",
    "SA": "SA Species List (for test)",
    "TAS": "TAS Species List (for test)",
    "VIC": "VIC Species List (for test)",
    "WA": "WA Species List (for test)",
}

# categories (from NSW?) to generalise
generalisation_categories = {
    "Category 3": "1km",
    "Category 2": "10km",
    "Category 1": "WITHHOLD",
}

# other variables from NSW
codeMap = {
    "C": "LC",
    "CR": "CR",
    "E": "EN",
    "NT": "NT",
    "PE": "EW",
    "SL": "SL",
    "V": "VU",
}
kingdomMap = {"animals": "Animalia", "plants": "Plantae", "fungi": "Fungi"}
classMap = {
    "AMPHIBIAN": "Amphibia",
    "MAMMAL": "Mammalia",
    "INVERTEBRATE": "",
    "FISH": "",
    "BIRD": "Aves",
    "REPTILE": "Reptilia",
}

# columns to rename for both sensitive and conservation lists
conservation_columns_rename = {
    "QLD": {
        "Scientific_name": "scientificName",
        "Common_name": "vernacularName",
        "Taxon_author": "scientificNameAuthorship",
        "Family": "family",
        "Taxon_Id": "WildNetTaxonID",
    },
    "NT": {
        "TERRITORY PARKS AND WILDLIFE ACT CLASSIFICATION": "status",
        "COMMON NAME": "vernacularName",
        "FAMILY": "family",
        "GENUS": "genus",
        "SPECIES": "species",
    },
    "NSW": {},
    "WA": {},
    "ACT": {
        "scientificname": "scientificName",
        "vernacularname": "vernacularName",
        "actconservationstatus": "sourceStatus",
        "taxonomicrank": "rank",
    },
    "TAS": {
        "SPECIES_NAME": "scientificName",  # Scientific name
        "PREFERRED_COMMON_NAMES": "vernacularName",  # Common name
        "STATE_SCHEDULE": "status",  # Current TSPA schedule classification
        # 'Category': 'sourceStatus',
        "FAMILY": "family",
    },  # Family
    "VIC": {
        "FFG_ACT_STATUS": "status",
        "SCIENTIFIC_NAME": "scientificName",
        "COMMON_NAME": "vernacularName",
    },
    "EPBC": {
        "Scientific Name": "scientificName",
        "Common Name": "vernacularName",
        "Threatened status": "sourceStatus",
        "Family": "family",
        "Genus": "genus",
        "Species": "species",
    },
}

sensitive_columns_rename = {
    "NSW": {},
    "QLD": {
        "Scientific name": "scientificName",
        "Common name": "vernacularName",
        "NCA status": "category",
        "Taxon Id": "WildNetTaxonID",
        "Code_description": "status",
        "Kingdom": "kingdom",
        "Family": "family",
    },
    "VIC": {
        "FFG_ACT_STATUS": "category",  # NOT VIC_ADVISORY_STATUS
        "SCIENTIFIC_NAME": "scientificName",
        "COMMON_NAME": "vernacularName",
    },
    "WA": {},
}

# key word to get values out if list is coming from API
api_values = {"New South Wales": "value"}

statuses_rename = {
    "ACT": {
        "Extinct": "Extinct",
        "Extinct in the Wild": "Extinct in the Wild",
        "Critically Endangered ": "Critically Endangered",
        "Endangered": "Endangered",
        "Vulnerable": "Vulnerable",
        "Regionally Conservation Dependent": "Conservation Dependent",
    },
    "EPBC": {
        "Extinct": "Extinct",
        "Extinct in wild": "Extinct in the Wild",
        "Extinct in the wild": "Extinct in the Wild",
        "Critically Endangered": "Critically Endangered",
        "Endangered": "Endangered",
        "Vulnerable": "Vulnerable",
        "Conservation dependent": "Conservation Dependent",
        "JAMBA CAMBA KAMBA": "Migratory",
        "CITES": "CITES",
    },
    "NSW": {
        "Extinct": "Extinct",
        "Critically Endangered": "Critically Endangered",
        "Endangered": "Endangered",
        "Vulnerable": "Vulnerable",
    },
    "NT": {
        "EX": "Extinct",
        "EW": "Critically Endangered",
        "CE": "Critically Endangered",
        "CR": "Critically Endangered",
        "EN": "Endangered",
        "VU": "Vulnerable",
        "NT": "Near Threatened",
        "LC": "Least concern",
        "DD": "Data Deficient",
        "NE": "Not Evaluated",
    },
    "QLD": {
        "Extinct wildlife": "Extinct",
        "Extinct in the wild wildlife": "Extinct in the Wild",
        "Extinct in the wild": "Extinct in the Wild",
        "Critically endangered wildlife": "Critically Endangered",
        "Endangered wildlife": "Endangered",
        "Vulnerable wildlife": "Vulnerable",
        "Near threatened wildlife": "Near Threatened",
        "Special least concern wildlife": "Least concern",
        "Least concern wildlife": "Least concern",
        "International wildlife": "CITES",
    },
    "SA": {
        "Endangered": "Endangered",
        "Vulnerable": "Vulnerable",
        "Rare": "Near Threatened",
    },
    "TAS": {
        "Extinct": "Extinct",
        "Endangered": "Endangered",
        "Vulnerable": "Vulnerable",
        "Rare": "Near Threatened",
        "extinct": "Extinct",
        "endangered": "Endangered",
        "vulnerable": "Vulnerable",
        "rare": "Near Threatened",
        "x": "Extinct",
        "e": "Endangered",
        "v": "Vulnerable",
        "r": "Near Threatened",
    },
    "VIC": {
        "Extinct": "Extinct",
        "Extinct in the Wild": "Extinct in the Wild",
        "Endangered (Extinct in Victoria)": "Extinct in the Wild",
        "Critically Endangered": "Critically Endangered",
        "Endangered": "Endangered",
        "Vulnerable": "Vulnerable",
        "Conservation Dependent": "Conservation Dependent",
        "Restricted": "Restricted",
    },
    "WA": {
        "CR": "Critically Endangered",
        "EN": "Endangered",
        "VU": "Vulnerable",
        "EX": "Extinct",
        "EW": "Extinct in the Wild",
        "SP": "Specially Protected",
        "MI": "Migratory",
        "CD": "Conservation Dependent",
        "CD & MI": "Conservation Dependent",
        "OS": "Other Specially Protected",
        "P1": "Priority 1: Poorly-known species",
        "P2": "Priority 2: Poorly-known species",
        "P3": "Priority 3: Poorly-known species",
        "P4": "Priority 4: Rare, Near Threatened",
        "MI & P1": "Priority 1: Poorly-known species",
        "MI & P3": "Priority 2: Poorly-known species",
        "MI & P4": "Priority 4: Rare, Near Threatened",
    },
}

all_species_ste_terr_column_names = {
    "ACT": {
        "verbatimScientificName": "scientificname",
        "verbatimVernacularName": "vernacularname",
        "verbatimRank": "taxonomicrank",
        "verbatimFamily": "family",
        "verbatimScientificNameAuthorship": "scientificnameauthor",
    },
    "NSW": {
        "verbatimScientificName": "currentScientificName",
        "verbatimVernacularName": "currentVernacularName",
        "verbatimRank": "taxonRank",
        "verbatimFamily": "family",
        "verbatimScientificNameAuthorship": "scientificNameAuthorship",
    },
    "NT": {
        "verbatimScientificName": "scientificName",
        "verbatimVernacularName": None,
        "verbatimRank": None,
        "verbatimFamily": None,
        "verbatimScientificNameAuthorship": None,
    },
    "QLD": {
        "verbatimScientificName": "Scientific_name",
        "verbatimVernacularName": "Common_name",
        "verbatimRank": None,
        "verbatimFamily": "Family",
        "verbatimScientificNameAuthorship": "Taxon_author",
    },
    "SA": {
        "verbatimScientificName": "SCIENTIFIC NAME",
        "verbatimVernacularName": "COMMON NAME",
        "verbatimRank": None,
        "verbatimFamily": "FAMILYNAME",
        "verbatimScientificNameAuthorship": "SPECIES AUTHOR",
    },
    "TAS": {
        "verbatimScientificName": "SPECIES_NAME",
        "verbatimVernacularName": "PREFERRED_COMMON_NAMES",
        "verbatimRank": None,
        "verbatimFamily": "FAMILY",
        "verbatimScientificNameAuthorship": "SPECIES_AUTHORITY",
    },
    "VIC": {
        "verbatimScientificName": "SCIENTIFIC_NAME",
        "verbatimVernacularName": "COMMON_NAME",
        "verbatimRank": "TAXON_LEVEL_CDE",
        "verbatimFamily": None,
        "verbatimScientificNameAuthorship": "AUTHORITY",
    },
    "WA": {
        "verbatimScientificName": "scientificName",
        "verbatimVernacularName": "VERNACULAR",
        "verbatimRank": "rank",
        "verbatimFamily": None,
        "verbatimScientificNameAuthorship": "author",
    },
}

all_species_ste_terr_column_names_use = {
    "ACT": [
        "scientificname",
        "vernacularname",
        "taxonomicrank",
        "family",
        "scientificnameauthor",
    ],
    "NSW": [
        "currentScientificName",
        "currentVernacularName",
        "taxonRank",
        "family",
        "scientificNameAuthorship",
    ],
    "NT": ["scientificName"],
    "QLD": ["Scientific_name", "Common_name", "Family", "Taxon_author"],
    "SA": [
        "SCIENTIFIC NAME",
        "COMMON NAME",
        "FAMILYNAME",
        "SPECIES AUTHOR",
    ],
    "TAS": [
        "SPECIES_NAME",
        "PREFERRED_COMMON_NAMES",
        "FAMILY",
        "SPECIES_AUTHORITY",
    ],
    "VIC": [
        "SCIENTIFIC_NAME",
        "COMMON_NAME",
        "TAXON_LEVEL_CDE",
        "AUTHORITY",
    ],
    "WA": [
        "scientificName",
        "VERNACULAR",
        "rank",
        "author",
    ],
}

all_species_ste_terr_column_rename = {
    "ACT": {
        "scientificname": "scientificName",
        "vernacularname": "vernacularName",
        "taxonomicrank": "rank",
        "scientificnameauthor": "scientificNameAuthorship",
    },
    "NSW": {
        "currentScientificName": "scientificName",
        "currentVernacularName": "vernacularName",
        "taxonRank": "rank",
    },
    "NT": {},
    "QLD": {
        "Scientific_name": "scientificName",
        "Common_name": "vernacularName",
        "Family": "family",
        "Taxon_author": "scientificNameAuthorship",
    },
    "SA": {
        "SCIENTIFIC NAME": "scientificName",
        "COMMON NAME": "vernacularName",
        "FAMILYNAME": "family",
        "SPECIES AUTHOR": "scientificNameAuthorship",
    },
    "TAS": {
        "SPECIES_NAME": "scientificName",
        "PREFERRED_COMMON_NAMES": "vernacularName",
        "FAMILY": "family",
        "SPECIES_AUTHORITY": "scientificNameAuthorship",
    },
    "VIC": {
        "SCIENTIFIC_NAME": "scientificName",
        "COMMON_NAME": "vernacularName",
        "TAXON_LEVEL_CDE": "rank",
        "AUTHORITY": "scientificNameAuthorship",
    },
    "WA": {
        "VERNACULAR": "vernacularName",
        "author": "scientificNameAuthorship",
    },
}
