# Field Conversion Information


## Tasmania
### Field Name Mappings
| **Source Field Name**|**New Field Name**|
|-----------------|-------------|
|Origin|sourceOrigin|
|Species|scientificName|
|Authority|scientificNameAuthorship|
|Common Name|vernacularName|
|Family|family|
|Group|class|
|sch|sourceStatus|
|EPBCA|EPBCA_status|
|Flora/Fauna|sourceKingdom|
|Classification|speciesGroup|
**Note:** records with null 'sch' value are excluded

|  | **Source Field**|**New Field**|Legend Description|
| --------- | ------------------|-----------------|----|
|Field|**Origin**|**higherGeography**||
|Data Value|end|endemic Tasmania|endemic to Tasmania|
||t|Tasmania |within Australia, occurs only in Tasmania|
||?i||possibly introduced and naturalised in Tasmania|
||#||sparingly naturalised or known from only one or two populations or collections|
||br end|migratory breeding endemic Tasmania|migratory, breeding endemic|
||mig|migratory|migratory|
||MI|Macquarie Island|Macquarie Island|
||eMI|endemic Macquarie Island|endemic to Macquarie Island|
||sa|sub-Antarctic Islands|sub-Antarctic Islands|
|Field|**Flora/Fauna**|**kingdom**||
|Data Value|Flora|Plantae|
||Fauna|Animalia|
|Field|**sch**|**status**||
|Data Value|||Refer to current-lists/README.md|

## Victoria
### Field Name Mappings
| **Source Field Name**|**New Field Name**|
|-----------------|-------------|
|TAXON_MOD|modified|
|TAXON_ID|VBA_TaxonId|
|SCI_NAME|scientificName|
|COMM_NAME|vernacularName|
|AUTHORITY|scientificNameAuthoritiy|
|FAMILY|family|
|FFG|FFG_status|
|FFG_DESC|FFG_desc|
|EPBC|EPBC_status|
|EPBC_DESC|EPBC_desc|
|VICADV|sourceStatus|
|VICADVDESC|status|
|RESTRICTN|generalisation|
|ORIGIN|VBA_origin|
|TAXON_TYPE|speciesGroup|
|VIC_LF|identificationRemarks|
|DISCIPLINE|VBA_discipline|
||kingdom|
|TAXN_LEV|taxonRank|
|Field|**Flora/Fauna**|**kingdom**||
|Data Value|Flora|Plantae|
||Fauna|Animalia|
