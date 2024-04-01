# ---------------------------------------------------------------------------
# vocab.py
# 
# This script contains all of the variables that don't change for the lists 
# update that will eventually run weekly.
# 
# NOTE: Do not include SA - they manage their own lists.
# ---------------------------------------------------------------------------

# URLs for ALA lists for test and production
listsProd = "https://lists.ala.org.au/ws/speciesList/"
listsTest = "https://lists-test.ala.org.au/ws/speciesList/"

# all the state lists that are automatically checked every week
lists = ["Queensland",
         "Northern Territory",
         "New South Wales",
         "Western Australia",
         "Australian Capital Territory", ## Done - sensitive managed by org
         "Tasmania", ## Done - sensitive managed by org
#          "Victoria", #authentication error]
         ]

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
list_ids_sensitive_test = {"New South Wales": "dr487",
                           "Queensland": "dr18404",
                           "Victoria": "dr490",
                           "Western Australia": "dr467"}

# ALA list ids for all sensitive authoritative lists on test we are updating
list_ids_sensitive_prod = {"Australian Capital Territory": "dr2627",
                      "New South Wales": "dr487",
                      "Northern Territory": "dr492",
                      "Queensland": "dr493",
                      "South Australia": "dr884",
                      "Tasmania": "dr491",
                      "Victoria": "dr490",
                      "Western Australia": "dr467"}

# categories (from NSW?) to generalise
generalisation_categories = {"Category 3": "1km",
                             "Category 2": "10km",
                             "Category 1": "WITHHOLD"}

# TODO: find out where this is in the code
return_columns = {"Australian Capital Territory": "dr2627",
                      "New South Wales": "dr487",
                      "Northern Territory": "dr492",
                      "Queensland": "dr493",
                      "South Australia": "dr884",
                      "Tasmania": "dr491",
                      "Victoria": "dr490",
                      "Western Australia": "dr467"}

# not sure what this is
api_values = {"New South Wales": "value"}

# urls for conservation lists
conservation_list_urls = {"Australian Capital Territory": ["https://www.data.act.gov.au/resource/9ikf-qahj.json"], # or is this correct?
             "New South Wales": ["https://data.bionet.nsw.gov.au/biosvcapp/odata/SpeciesNames"],
             "Northern Territory": ["https://ftp-dlrm.nt.gov.au/main.html?download&weblink=1e717d654034af5e5f840d2ba3fd9187&realfilename=NT_Species_List_Fauna.xlsx", #fauna
                                    "https://ftp-dlrm.nt.gov.au/main.html?download&weblink=60088e77ecef6c6cbf515c299f07a420&realfilename=NT_Species_List_Flora.xlsx"], #flora
             "Queensland": ["https://apps.des.qld.gov.au/data-sets/wildlife/wildnet/species.csv"],
             "Tasmania": ["https://nre.tas.gov.au/Documents/TasThreatenedSpecies.xls.xlsx"],
             "Victoria": ["https://vba.dse.vic.gov.au/vba/downloadVSC.do"],
             "Western Australia": ["https://www.dbca.wa.gov.au/wildlife-and-ecosystems/plants/list-threatened-and-priority-flora",
                                   "https://www.dbca.wa.gov.au/wildlife-and-ecosystems/plants/list-threatened-and-priority-fauna"]} 

# urls for relevant sensitive lists
sensitive_list_urls = {"New South Wales": ["https://data.bionet.nsw.gov.au/biosvcapp/odata/SpeciesNames"],
             "Queensland": ["https://apps.des.qld.gov.au/data-sets/wildlife/wildnet/qld-confidential-species.csv"],
             "Victoria": ["https://vba.dse.vic.gov.au/vba/downloadVSC.do"], ### TODO: check on this
             "Western Australia": ["https://www.dbca.wa.gov.au/wildlife-and-ecosystems/animals/list-threatened-and-priority-fauna",
                                   "https://www.dbca.wa.gov.au/wildlife-and-ecosystems/plants/list-threatened-and-priority-flora"]}            