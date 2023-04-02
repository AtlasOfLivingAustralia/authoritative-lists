# Contents
Directory containing:
1. Conservation Lists
2. Sensitive Lists
3. GRIIS invasive List
4. Migratory Bird Agreement Lists
  
## Lists in Pipelines
 Sensitive and threatened go through different pathways in the pipelines. 

 1. Conservation lists should have isThreatened=true (Threatened flag) and require both status and sourceStatus columns, 
 2. Sensitive lists should have isSDS=true (part of Sensitive data service) and require category and generalisation fields.
 3. Both lists require Authoritative flag and Region set

## List Update dates

### Conservation Lists

| **State** | DR Prod/Test  | **Source date** | **ALA Upload date** | **Source date origin**    |
|-----------|---------------|-----------------|---------------------|---------------------------|
| EPBC      | dr656/dr656   | 2022-05-10      | 2022-11-            | No Date. Reg update reqd  |
| ACT       | dr649/dr649   | 2023-01-05      | 2023-02-28          | Website. Reg check reqd   |
| NSW       | dr650/dr650   | current date    | 2022-03-16          | No Date. Reg update reqd  |
| NT        | dr651/dr651   | current date    | 2022-05-18          | No date. Email Cam/Tania Laity|
| QLD       | dr652/dr652   | 2023-02-01      | 2023-01-17          | No Date. Reg update reqd  |
| SA        | dr653/dr653   | 2023-02-13      | not current         | Website. Reg update reqd  |
| TAS       | dr654/dr654   | 2022-12-21      | 2023-02-28          | Website. Reg check reqd   |
| VIC       | dr655/dr655   | 2023-01-19      | not current         | Website. Reg check reqd   |
| WA        | dr2201/dr2201 | 2022-10-07      | not current         | File name. Reg check reqd |
| BONN      | dr18987/18505 | 2022-05-10      | 2022-12-09          | See EPBC                  |
| CAMBA     | dr18989/18504 | 2022-05-10      | 2022-12-09          | See EPBC                  |
| JAMBA     | dr18988/18503 | 2022-05-10      | 2022-12-09          | See EPBC                  |
| ROKAMBA   | dr18990/18502 | 2022-05-10      | 2022-12-09          | See EPBC                  |

### Sensitive Lists

| **State** | **DR Prod/Test** | **Source date** | **ALA Upload date** | **Source date origin**         |
|-----------|------------------|-----------------|---------------------|--------------------------------|
| ACT       | dr2627/dr2627    | 2022-10-05      | 2023-02-21          | No date. Email Cam/Tania Laity |
| NSW       | dr487/dr18457    | current date    | 2022-03-16          | No Date. Reg update reqd       |
| NT        | dr492/dr18690    | 2022-03-22      | 2023-02-22          | No date. Email Cam/Tania Laity |
| QLD       | dr493/dr18404    | current date    | 2023-04-03          | No Date. Reg update reqd       |
| SA        | dr884/dr18706    | 2023-02-13      | not current         | Website. Reg update reqd       |
| TAS       | dr491/18692      | 2022-09-21      | 2023-02-22          | No date. Email Cam/Tania Laity |
| VIC       | dr490/dr18669    | current date    | not current         | Website. Reg check reqd        |
| WA        | dr467/dr18406    | 2019-01-03      | not current         | File name. Reg check reqd      |

## Sensitive List XML
**SDS XML:** https://sds.ala.org.au/sensitive-species-data.xml

Information relating to processing of data can be found at:

1. [Data Processing](https://github.com/AtlasOfLivingAustralia/authoritative-lists/tree/master/source-data#data-processing)
2. [Status/Source status mapping by State](https://raw.githubusercontent.com/AtlasOfLivingAustralia/authoritative-lists/master/analysis/Status-SourceStatus-Mapping.csv)



