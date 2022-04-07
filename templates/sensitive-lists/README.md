# Sensitive Lists - Templates

## Background

[Sensitive lists in the ALA's Lists tool](https://lists.ala.org.au/public/speciesLists?isSDS=eq:true) are provided by each state jurisdiction to supply data obfuscation rules to the ALA's sensitive data service (SDS). THe SDS obsfucates location and other information to each occurrence record in the ALA's ingestion process.

See the `List info` link for metadata about each list. Some lists apply a single level of obsfucation to every species in the list, and other lists apply supplied obfuscation rules for each species. The rules are specified in the `generalisation` field.

See https://github.com/AtlasOfLivingAustralia/sds for info about SDS processing.

**What does the ALA do with them?**

We ingest the lists into our Lists tool. Each item on the lists is passed through our name matching algorithm.

When species occurrence data is ingested into the ALA, we do a lot of processing to check location coordinates and parse the species information again through our name matching algorithm.
We then use the Australian state of the location and the matched species to look up these lists and obfuscate the location details according to the rules in the list.

## Recommended fields

A template csv can be found here: [stateSensitiveListTemplate.csv](stateSensitiveListTemplate.csv)

The minimum mandatory fields are marked below with an asterisk. However, the provided lists should contain as much taxonomic information as possible, so that the name matching algorithm can find the best match. The below list contains the relevant Darwin Core terms that may be used by the algorithm.

Sensitive lists contain a field called `generalisation`. Values in this list are currently `WITHHOLD`,'`100m`,`1km`,`10km`,`100km`.
A single value can be supplied for the entire list separately.

Additional fields can be provided and will be retained with the list.

| Field Name               | Darwin Core Uri | Darwin Core definition|
|--------------------------|-----------------|-----------------------|
| *scientificName          |     |     |
| vernacularName           |     |     |
| acceptedNameUsage        |     |     |
| taxonomicStatus          |     |     |
| taxonRank                |     |     |
| nomenclaturalCode        |     |     |
| kingdom                  |     |     |
| phylum                   |     |     |
| class                    |     |     |
| order                    |     |     |
| family                   |     |     |
| scientificNameAuthorship |     |     |
| taxonRemarks             |     |     |
| generalisation           |     |     |
