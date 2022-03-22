# Authoritative Conservation and Sensitive Species Lists

This repository is intended to document the collection and preparation of Conservation and Sensitive lists from Australian jurisdictions into the ALA's list tool.

## Contents
Each of the directories listed below has its own **README.md** file describing source content and processes used to create the datasets.

| **Directory** | **Description**                                                                 |
| --------- |---------------------------------------------------------------------------------|
| historical-lists | Conservation and Sensitive Species Lists in the ALA Lists tool as at 16/03/2022 |
| source-data| Source data and translation information                                         |
| current-lists | Lists processed/extracted from source |

## Sensitive Lists

[Sensitive lists in the ALA's Lists tool](https://lists.ala.org.au/public/speciesLists?isSDS=eq:true) are provided by each state jurisdiction to supply data obfuscation rules to the ALA's sensitive data service (SDS). THe SDS obsfucates location and other information to each occurrence record in the ALA's ingestion process. 

See the `List info` link for metadata about each list. Some lists apply a single level of obsfucation to every species in the list, and other lists apply supplied obfuscation rules for each species. The rules are specified in the `generalisation` field.

See https://github.com/AtlasOfLivingAustralia/sds for info about SDS processing.

| druid |list|
|-------|---------|
| dr2627 |[Australian Capital Territory : Sensitive Species](https://lists.ala.org.au/speciesListItem/list/dr2627)|
| dr487 |[New South Wales : Sensitive Species](https://lists.ala.org.au/speciesListItem/list/dr487)|
| dr492 |[Northern Territory : Sensitive Species](https://lists.ala.org.au/speciesListItem/list/dr492)|
| dr493 |[Queensland : Sensitive Species](https://lists.ala.org.au/speciesListItem/list/dr493)|
| dr884 |[South Australia : Sensitive Species](https://lists.ala.org.au/speciesListItem/list/dr884)|
| dr491 |[Tasmania: Sensitive Species](https://lists.ala.org.au/speciesListItem/list/dr491)|
| dr490 |[Victoria: Sensitive Species](https://lists.ala.org.au/speciesListItem/list/dr490)|
| dr467 |[Western Australia :Sensitive Species](https://lists.ala.org.au/speciesListItem/list/dr467)|

    
## Conservation Lists 
[Conservation lists](https://lists.ala.org.au/public/speciesLists?listType=eq:CONSERVATION_LIST&isAuthoritative=eq:true) are for each state plus the national EPBC list.

Conservation lists contain the fields `status` and `sourceStatus`, the former usually representing a final parsed IUCN like vocabulary to enable faceting, and the latter containing the raw values provided by the state jurisdiction.

| druid |list|
|-------|---------|
| dr649 |[Australian Capital Territory : Conservation Status](https://lists.ala.org.au/speciesListItem/list/dr649)|
| dr656 |[EPBC Act Threatened Species : Conservation Status](https://lists.ala.org.au/speciesListItem/list/dr656)|
| dr650 |[New South Wales : Conservation Status](https://lists.ala.org.au/speciesListItem/list/dr650)|
| dr651 |[Northern Territory : Conservation Status](https://lists.ala.org.au/speciesListItem/list/dr651)|
| dr652 |[Queensland : Conservation Status](https://lists.ala.org.au/speciesListItem/list/dr652)|
| dr653 |[South Australia : Conservation Status](https://lists.ala.org.au/speciesListItem/list/dr653)|
| dr654 |[Tasmania: Conservation Status](https://lists.ala.org.au/speciesListItem/list/dr654)|
| dr655 |[Victoria: Conservation Status](https://lists.ala.org.au/speciesListItem/list/dr655)|
| dr2201 |[Western Australia : Conservation Status](https://lists.ala.org.au/speciesListItem/list/dr2201)|

