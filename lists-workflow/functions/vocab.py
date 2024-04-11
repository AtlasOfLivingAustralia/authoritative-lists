# ---------------------------------------------------------------------------
# vocab.py
# 
# This script contains all of the variables that don't change for the lists 
# update that will eventually run weekly.
# 
# NOTE: Do not include SA - they manage their own lists.
# ---------------------------------------------------------------------------

authorize_url = "https://auth-secure.auth.ap-southeast-2.amazoncognito.com/oauth2/authorize"
token_url = "https://auth-secure.auth.ap-southeast-2.amazoncognito.com/oauth2/token"

# URLs for ALA lists for test and production
listsProd = "https://lists.ala.org.au/ws/speciesListItems/"
listsTest = "https://lists-test.ala.org.au/ws/speciesListItems/"
urlSuffix = "?max=10000&includeKVP=true"

conservation_lists = [] # Queensland
sensitive_lists = ["Western Australia"]

# all the state lists that are automatically checked every week
# conservation_lists = ["Queensland",
#          "Northern Territory",
#          "New South Wales",
#          "Western Australia",
#          "Australian Capital Territory", ## Done - sensitive managed by org
#          "Tasmania", ## Done - sensitive managed by org
#         "Victoria", #authentication error]
#          "EPBC"
#          ]

# sensitive_lists = ["New South Wales",
#                     "Queensland",
#                     "Victoria",
#                     "Western Australia"]

# ALA list ids for all conservation authoritative lists on test
list_ids_conservation_test = {"Australian Capital Territory": "dr649",
                              "New South Wales": "dr650",
                              "Northern Territory": "dr651",
                              "Queensland": "dr652",
                              "South Australia": "dr653",
                              "Tasmania": "dr654",
                              "Victoria": "dr655",
                              "Western Australia": "dr2201",
                              "EPBC": "dr656"}

# ALA list ids for all conservation authoritative lists on prod
list_ids_conservation_prod = {"Australian Capital Territory": "dr649",
                              "New South Wales": "dr650",
                              "Northern Territory": "dr651",
                              "Queensland": "dr652",
                              "Tasmania": "dr654",
                              "Victoria": "dr655",
                              "Western Australia": "dr2201",
                              "EPBC": "dr656"}

# ALA list ids for all sensitive authoritative lists on test we are updating
list_ids_sensitive_test = {"New South Wales": "dr18457",
                           "Queensland": "dr18404",
                           "Victoria": "dr18669",
                           "Western Australia": "dr18406"}

# ALA list ids for all sensitive authoritative lists on test we are updating
list_ids_sensitive_prod = {"New South Wales": "dr487",
                           "Queensland": "dr493",
                           "Victoria": "dr490",
                           "Western Australia": "dr467"}

# --------------------------------------------------------------------------
### TODO: change
list_names_sensitive_test = {"New South Wales": "NSW Sensitive Species List",
                             "Queensland": "Queensland Confidential Species",
                             "Victoria": "Victorian Restricted Species List",
                             "Western Australia": "Western Australia: Sensitive Species"}

list_names_conservation_test = {"Australian Capital Territory": "Australian Capital Territory : Conservation Status",
                                "New South Wales": "New South Wales : Conservation Status",
                                "Northern Territory": "Northern Territory : Conservation Status",
                                "Queensland": "Queensland : Conservation Status",
                                "Tasmania": "Tasmania : Conservation Status",
                                "Victoria": "Victoria : Conservation Status",
                                "Western Australia": "Western Australia: Conservation Status",
                                "EPBC": "EPBC Act Threatenet Species"}
# --------------------------------------------------------------------------

# categories (from NSW?) to generalise
generalisation_categories = {"Category 3": "1km",
                             "Category 2": "10km",
                             "Category 1": "WITHHOLD"}

# other variables from NSW 
codeMap = {'C': 'LC', 'CR': 'CR', 'E': 'EN',
        'NT': 'NT','PE': 'EW', 'SL': 'SL',
        'V': 'VU'}
kingdomMap = {'animals':'Animalia','plants':'Plantae','fungi':'Fungi'}

# columns to rename for both sensitive and conservation lists
conservation_columns_rename = {"Queensland": {'Scientific_name':'scientificName',
                                              'Common_name': 'vernacularName',
                                              'Taxon_author':'scientificNameAuthorship',
                                              'Family': 'family',
                                              'NCA_status':'sourceStatus',
                                              'Code_description':'status',
                                              'Taxon_Id':'WildNetTaxonID'},
                               "Northern Territory": {'TERRITORY PARKS AND WILDLIFE ACT CLASSIFICATION': 'status',
                                                      'COMMON NAME': 'vernacularName',
                                                      'FAMILY': 'family', 
                                                      'GENUS': 'genus', 
                                                      'SPECIES': 'species'},
                               "New South Wales": {},
                               "Western Australia": {},
                               "Australian Capital Territory": {'scientificname': 'scientificName',
                                                                'vernacularname': 'vernacularName',
                                                                'sourcestatus': 'sourceStatus'},
                               "Tasmania": {'Scientific name': 'scientificName', 
                                            'Common name': 'vernacularName',
                                            'Current TSPA schedule classification': 'status',
                                            'Category': 'sourceStatus',
                                            'Family': 'family'},
                               "Victoria": {'VIC_ADVISORY_STATUS': 'status',
                                            'SCIENTIFIC_NAME': 'scientificName', 
                                            'COMMON_NAME': 'vernacularName'},
                               "EPBC": {'Scientific Name': 'scientificName',
                                        'Common Name': 'vernacularName',
                                        'Threatened status': 'sourceStatus',
                                        'Family': 'family',
                                        'Genus': 'genus',
                                        'Species': 'species'}}

sensitive_columns_rename = {"New South Wales": {},
                            "Queensland": {'Scientific name':'scientificName',
                                           'Common name': 'vernacularName',
                                           'NCA status': 'category', 
                                           'Taxon Id':'WildNetTaxonID',
                                           'Code_description':'status',
                                           'Kingdom':'kingdom',
                                           'Family':'family'},
                            "Victoria": {'VIC_ADVISORY_STATUS': 'category',
                                         'SCIENTIFIC_NAME': 'scientificName', 
                                         'COMMON_NAME': 'vernacularName'},
                            "Western Australia": {}}

# key word to get values out if list is coming from API
api_values = {"New South Wales": "value"}

# urls for conservation lists
conservation_list_urls = {"Australian Capital Territory": ["https://www.data.act.gov.au/resource/9ikf-qahj.json"], # or is this correct?
             "New South Wales": ["https://data.bionet.nsw.gov.au/biosvcapp/odata/SpeciesNames"],
             "Northern Territory": ["https://ftp-dlrm.nt.gov.au/main.html?download&weblink=1e717d654034af5e5f840d2ba3fd9187&realfilename=NT_Species_List_Fauna.xlsx", #fauna
                                    "https://ftp-dlrm.nt.gov.au/main.html?download&weblink=60088e77ecef6c6cbf515c299f07a420&realfilename=NT_Species_List_Flora.xlsx"], #flora
             "Queensland": ["https://apps.des.qld.gov.au/data-sets/wildlife/wildnet/species.csv"],
             "Tasmania": ["https://nre.tas.gov.au/Documents/TasThreatenedSpecies.xls.xlsx"],
             "Victoria": ["https://vba.biodiversity.vic.gov.au/vba/downloadVSC.do"],
             "Western Australia": ["https://www.dbca.wa.gov.au/wildlife-and-ecosystems/plants/list-threatened-and-priority-flora",
                                   "https://www.dbca.wa.gov.au/wildlife-and-ecosystems/animals/list-threatened-and-priority-fauna"],
             "EPBC": ["https://data.gov.au/data/dataset/threatened-species-state-lists/resource/78401dce-1f40-49d3-92c4-3713d6e34974"]} 

# urls for relevant sensitive lists
sensitive_list_urls = {"New South Wales": ["https://data.bionet.nsw.gov.au/biosvcapp/odata/SpeciesNames"],
             "Queensland": ["https://apps.des.qld.gov.au/data-sets/wildlife/wildnet/qld-confidential-species.csv"],
             "Victoria": ["https://vba.biodiversity.vic.gov.au/vba/downloadVSC.do"], ### TODO: check on this
             "Western Australia": ["https://www.dbca.wa.gov.au/wildlife-and-ecosystems/animals/list-threatened-and-priority-fauna",
                                   "https://www.dbca.wa.gov.au/wildlife-and-ecosystems/plants/list-threatened-and-priority-flora"]}            