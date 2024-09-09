# Authorisation parameters for ALA API and collectory

# Production
# baseUrl = 'https://api.ala.org.au/specieslist/ws/speciesList/?sort=dataResourceUid&'
# collectoryUrl = 'https://collections.ala.org.au/ws/'
# litemsUrl = 'https://lists.ala.org.au/ws/speciesListItems/'

# Test
baseUrl = 'https://api.test.ala.org.au/specieslist/ws/speciesList/?sort=dataResourceUid&'
collectoryUrl = 'https://collections-test.ala.org.au/ws/'
# litemsUrl = 'https://lists-test.ala.org.au/ws/speciesListItems/'
litemPrefix = 'https://api.test.ala.org.au/specieslist/ws/speciesListItems/'
litemSuffix = '?q=%20&nonulls=true&sort=itemOrder&max=12000&offset=0&includeKVP=true'