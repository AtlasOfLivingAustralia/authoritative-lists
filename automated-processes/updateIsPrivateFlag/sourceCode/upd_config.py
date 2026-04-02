# Authorisation parameters for ALA API and collectory

# JWT token from Cognito auth system"""

token_url: str = "https://auth-secure.auth.ap-southeast-2.amazoncognito.com/oauth2/token"
client_id: str = "76n2kf3fa5f1ispatr436u9t96"
client_secret: str = "9l7diuhf8uifenhc466n8c8bmgqnv98l88d8gbov8nm7nkf35c7"

# JWT token from CAS
# token_url: str = "https://auth.ala.org.au/cas/oidc/oidcAccessToken"
# client_id: str = "4e30bd46431fa06d6975981fb047a3496ef6f836"
# client_secret: str = "6f39e1bdbbe6533883272f4e2eb4f15c1b8ad6c8"

# Production
# collectory_url = "https://collections.ala.org.au/ws/dataResource/"
# list_url = "https://api.ala.org.au/specieslist/ws/speciesList/"
# list_info_url = "https://api.ala.org.au/specieslist/ws/speciesList/?isAuthoritative=False&isPrivate=False"
# graphql_url = "https://lists.ala.org.au/graphql"  # URL for list update

# Test
collectory_url = "https://collections-test.ala.org.au/ws/dataResource/"
collectory_api_key = "dba60c96-380f-4793-90c8-5dbc4764ca4b"
# list_url = "https://lists-ws.test.ala.org.au/v2/speciesList/"
# list_url = "https://lists-ws.test.ala.org.au/v1/speciesListInternal/"
# list_info_url = "https://lists-ws.test.ala.org.au/v2/speciesList?isAuthoritative=False&isPrivate=False"

list_url = "https://lists-ws.test.ala.org.au/v2/speciesList/"
list_info_url = "https://lists-ws.test.ala.org.au/v2/speciesList?isAuthoritative=False&isPrivate=False"
# list_info_url = "https://lists-develop-ws.dev.ala.org.au/v2/speciesList?isAuthoritative=False&isPrivate=False"
graphql_url = "https://lists-ws.test.ala.org.au/graphql"  # URL for list update

# Dev
# list_url = "https://lists-develop-ws.dev.ala.org.au/v2/speciesList/"
# list_info_url = "https://lists-develop-ws.dev.ala.org.au/v2/speciesList?isAuthoritative=False&isPrivate=False"
# graphql_url = "https://lists-develop-ws.dev.ala.org.au/graphql"  # URL for list update

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
