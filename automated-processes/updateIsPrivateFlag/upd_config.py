# Authorisation parameters for ALA API and collectory

# Production
# list_url = "https://lists-ws.test.ala.org.au/v2/speciesList/"
# list_info_url = "https://lists-ws.test.ala.org.au/v2/speciesList?isAuthoritative=False&isPrivate=False"
# graphql_url = "https://lists.ala.org.au/graphql"  # URL for list update

# Test
# collectory_url = "https://api.test.ala.org.au/metadata/ws/dataResource/"
# collectory_url = "https://collections.test.ala.org.au/ws/dataResource/"
collectory_url = "https://collections.test.ala.org.au/ws/dataResource/"
list_url = "https://lists-ws.test.ala.org.au/v2/speciesList/"
list_info_url = "https://lists-ws.test.ala.org.au/v2/speciesList?isAuthoritative=False&isPrivate=False"
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
