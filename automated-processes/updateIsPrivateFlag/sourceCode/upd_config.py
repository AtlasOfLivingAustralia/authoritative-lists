# Authorisation parameters for ALA API and collectory

# JWT token from Cognito auth system"""

token_url: str = (
    "https://auth-secure.auth.ap-southeast-2.amazoncognito.com/oauth2/token"
)
client_id: str = "76n2kf3fa5f1ispatr436u9t96"
client_secret: str = "9l7diuhf8uifenhc466n8c8bmgqnv98l88d8gbov8nm7nkf35c7"

# *************************************************************************************************************
# Test
# Collectory
# collectory_url = "https://collections-test.ala.org.au/ws/"
# collectory_api_key = "dba60c96-380f-4793-90c8-5dbc4764ca4b" # See airflow variable

# Lists Service
# list_url = "https://lists-ws.test.ala.org.au/v2/speciesList/"
# list_info_url = "https://lists-ws.test.ala.org.au/v2/speciesList?isAuthoritative=False&isPrivate=False"
# graphql_url = "https://lists-ws.test.ala.org.au/graphql"  # URL for list update

# *************************************************************************************************************
# Prod - New Lists tool
# Collectory
collectory_url = "https://collections.ala.org.au/ws/"
collectory_api_key = "d58043a0-e589-4d3d-b547-b51651c9ec73"  # See airflow variable

# Lists Service
list_url = "https://lists-ws.ala.org.au/v2/speciesList/"
list_info_url = (
    "https://lists-ws.ala.org.au/v2/speciesList?isAuthoritative=false&isPrivate=false"
)
graphql_url = "https://lists-ws.ala.org.au/graphql"

# *************************************************************************************************************
# Data fields required for graphql update

# Data fields required for graphql update
graphql_keys_to_keep = [
    "id",
    "authority",
    "description",
    "isAuthoritative",
    "isInvasive",
    "isPrivate",
    "isBIE",
    "isSDS",
    "isThreatened",
    "licence",
    "listType",
    "region",
    "title",
    "wkt",
    "tags",
]

# BioCollect DRs to exclude

drExclude = [
    "dr10638",
    "dr10886",
    "dr1107",
    "dr11174",
    "dr11300",
    "dr11422",
    "dr11424",
    "dr11427",
    "dr11428",
    "dr1266",
    "dr12990",
    "dr13329",
    "dr13397",
    "dr13398",
    "dr13406",
    "dr13414",
    "dr13449",
    "dr13450",
    "dr13697",
    "dr13911",
    "dr14060",
    "dr14137",
    "dr14140",
    "dr14242",
    "dr14526",
    "dr15082",
    "dr15735",
    "dr15831",
    "dr15837",
    "dr16109",
    "dr16112",
    "dr16119",
    "dr16154",
    "dr16202",
    "dr16296",
    "dr16297",
    "dr16298",
    "dr16300",
    "dr16320",
    "dr16326",
    "dr16328",
    "dr16329",
    "dr16342",
    "dr16450",
    "dr17180",
    "dr17211",
    "dr17338",
    "dr1770",
    "dr17820",
    "dr17888",
    "dr18223",
    "dr18224",
    "dr18236",
    "dr18237",
    "dr18680",
    "dr19577",
    "dr19618",
    "dr19730",
    "dr20077",
    "dr20541",
    "dr21536",
    "dr2171",
    "dr21797",
    "dr22130",
    "dr22384",
    "dr2505",
    "dr2587",
    "dr2683",
    "dr28205",
    "dr28398",
    "dr28401",
    "dr29939",
    "dr30245",
    "dr31198",
    "dr31994",
    "dr32169",
    "dr33798",
    "dr33869",
    "dr33878",
    "dr33879",
    "dr33883",
    "dr33884",
    "dr33886",
    "dr33888",
    "dr33889",
    "dr34082",
    "dr34084",
    "dr34090",
    "dr34091",
    "dr4658",
    "dr4671",
    "dr4727",
    "dr5155",
    "dr5468",
    "dr5536",
    "dr6758",
    "dr7239",
    "dr7380",
    "dr7524",
    "dr7537",
    "dr7592",
    "dr7804",
    "dr7826",
    "dr7849",
    "dr7872",
    "dr7873",
    "dr7900",
    "dr7901",
    "dr7902",
    "dr7903",
    "dr7942",
    "dr7968",
    "dr7972",
    "dr7981",
    "dr8013",
    "dr8016",
    "dr8052",
    "dr8080",
    "dr8082",
    "dr8100",
    "dr8123",
    "dr8134",
    "dr8207",
    "dr8214",
    "dr8215",
    "dr8860",
    "dr914",
    "dr9310",
    "dr9563",
    "dr9570",
    "dr9802",
    "drt1361236915816",
]
