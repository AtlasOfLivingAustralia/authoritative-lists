import requests
import pandas as pd
from vocab import generalisation_categories

response = requests.get("https://data.bionet.nsw.gov.au/biosvcapp/odata/SpeciesNames")
response_json = response.json()

# get data frame
NSW_df = pd.DataFrame(response_json['value'])
print(NSW_df.columns)
current_species = NSW_df[NSW_df['isCurrent'] == "true"]

# first, sensitive list
sensitive_species = current_species[current_species['sensitivityClass'].isin(["Category 1","Category 2","Category 3"])].reset_index(drop=True)

# add a generalisation column
sensitive_species['generalisation'] = sensitive_species['sensitivityClass']

# replace the category names with generalisations, including witheld
sensitive_species['generalisation'] = sensitive_species['generalisation'].replace(generalisation_categories)

# write 
sensitive_species[['scientificName', 'family', 'genus', 'vernacularName','generalisation', 'sensitivityClass']].to_csv("NSW-sensitive.csv",index=False)
# sensitivelist['generalisation'] = sensitivelist['sensitivityClass']

## 22/08/2023
# add an item to the list
# NSW have added a subspecies level entry (Calyptorhynchus lathami lathami) and replaced it with a species entry (Calyptorhynchus lathami), which the SDS will not work with, because it doesn't necessarily cascade changes. Both need to be in the list.
# Add the species entry back to the list, upload it to test, and run the changelist process again
new = sensitive_species[sensitive_species.scientificName == "Calyptorhynchus lathami lathami"].copy()
new[['scientificName']] = "Calyptorhynchus lathami" # replace the name
new[['vernacularName']] = "Glossy Black-cockatoo"
sensitive_species = pd.concat([sensitive_species,new])
sensitive_species[sensitive_species['scientificName'].str.startswith('Calyptorhynchus lathami')]

# then, conservation list
conservation_list= NSW_df[(NSW_df['stateConservation'] !='Not Listed') & (NSW_df['isCurrent'] == 'true')].reset_index(drop=True)
conservation_list = conservation_list[['scientificName', 'vernacularName', 'family', 'genus', 'stateConservation']]
conservation_list['status'] = conservation_list['stateConservation']
conservation_list = conservation_list.rename(columns={"stateConservation": "sourceStatus"})
conservation_list.to_csv("NSW-conservation.csv",index=False)