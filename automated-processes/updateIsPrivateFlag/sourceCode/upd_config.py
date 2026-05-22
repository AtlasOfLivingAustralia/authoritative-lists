# Authorisation parameters for ALA API and collectory

# JWT token from Cognito auth system"""

token_url: str = (
    "https://auth-secure.auth.ap-southeast-2.amazoncognito.com/oauth2/token"
)
client_id: str = "76n2kf3fa5f1ispatr436u9t96"
client_secret: str = "9l7diuhf8uifenhc466n8c8bmgqnv98l88d8gbov8nm7nkf35c7"

# Test
# Collectory
# collectory_url = "https://collections-test.ala.org.au/ws/"
collectory_api_key = "dba60c96-380f-4793-90c8-5dbc4764ca4b"
# list_url = "https://lists-ws.test.ala.org.au/v2/speciesList/"
# list_info_url = "https://lists-ws.test.ala.org.au/v2/speciesList?isAuthoritative=False&isPrivate=False"
# graphql_url = "https://lists-ws.test.ala.org.au/graphql"  # URL for list update

# Prod - New Lists tool
# Collectory
collectory_url = "https://collections.ala.org.au/ws/"
# collectory_api_key = "dba60c96-380f-4793-90c8-5dbc4764ca4b"
list_url = "https://lists-ws.ala.org.au/v2/speciesList/"
# list_info_url = "https://lists-ws.ala.org.au/specieslist?isAuthoritative=false"
# list_info_url = "https://lists-ws.ala.org.au/v2/speciesList?isAuthoritative=false"
list_info_url = (
    # "https://lists-ws.ala.org.au/v2/speciesList?isAuthoritative=false&isPrivate=false"
    "https://lists.ala.org.au/?filters=isAuthoritative:true.isPrivate:false"
    # "https://lists-ws.ala.org.au/v2/speciesList?isAuthoritative=false&isPrivate=true"
)
# list_info_url = "https://lists-ws.ala.org.au/isAuthoritative=false&isPrivate=false"
# Web URL - https://lists.ala.org.au/admin-lists?filters=isAuthoritative:true.isPrivate:false - 21,792 records
#   -  https://lists.ala.org.au/?filters=isAuthoritative:true.isPrivate:false    - 10,920 records
#   -  https://lists.ala.org.au/?filters=isAuthoritative:false    - 10,858 records


# list_info_url = (
#     "https://lists-ws.ala.org.au/v2/speciesList?isAuthoritative=false&isPrivate=true"
# )
graphql_url = "https://lists-ws.ala.org.au/graphql"

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
# Data fields required for graphql update
keys_to_keep = [
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
