# Contents
Directory containing:
1. Conservation Lists
2. Sensitive Lists
3. GRIIS invasive List
4. Migratory Bird Agreement Lists
  
## Lists in Pipelines
 Sensitive and threatened go through different pathways in the pipelines. 

 1. Conservation lists should have isThreatened=true (Threatened flag) and require both status and sourceStatus columns, 
 2. Sensitive lists should have isThreatened=false, isSDS=true (part of Sensitive data service) and require category and generalisation fields.
 3. Both lists require Authoritative flag and Region set

## List Information

[Production List Information](../Monitoring/Authoritative-lists-prod.md)

[Test List Information](../Monitoring/Authoritative-lists-test.md)


### Test


## Sensitive List XML
**SDS XML:** https://sds.ala.org.au/sensitive-species-data.xml

Information relating to processing of data can be found at:

1. [Data Processing](https://github.com/AtlasOfLivingAustralia/authoritative-lists/tree/master/source-data#data-processing)
2. [Status/Source status mapping by State](https://raw.githubusercontent.com/AtlasOfLivingAustralia/authoritative-lists/master/analysis/Status-SourceStatus-Mapping.csv)



