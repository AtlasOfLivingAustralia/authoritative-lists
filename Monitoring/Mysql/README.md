# MYSQL Scripts - DO NOT USE
## Use Monitoring/ArchiveLists python script

## ala-lists-create-update.mysql

Mysql script to extract records from **species_list** table to temporary table **temp_list** with conditions as 
described below. 

List must be **non-authoritative** and meet the following criteria:

   1. Lists with zero records
   2. Lists with only 1 record
   3. Lists marked with list type – “Test%”
   4. Lists with list name contains "test%"

Process:

   1. Query data
   2. Populate temp table
   3. Update all records - set is_private flag = true
   4. Remove temp table after testing

## ala-lists-check-update.mysql

MYSQL script to do some post-checking on the data

## Database: specieslist 
### Table schema: species_list


| **Field**         | **Type**     | **Null** | **Key** | 
|-------------------|--------------|----------|---------|
| id                | bigint       | NO       | 0       | 
| version           | bigint       | NO       | NULL    |  
| data_resource_uid | varchar(255) | NO       | NULL    |
| date_created      | datetime     | NO       | NULL    |
| description       | mediumtext   | YES      | NULL    |
| first_name        | varchar(255) | YES      | NULL    |
| last_updated      | datetime     | NO       | NULL    |
| list_name         | varchar(255) | NO       | NULL    |
| list_type         | varchar(255) | YES      | NULL    |
| surname           | varchar(255) | YES      | NULL    |
| url               | varchar(255) | YES      | NULL    |
| username          | varchar(255) | NO       | NULL    |
| is_private        | bit(1)       | YES      | NULL    |
| editors           | tinyblob     | YES      | NULL    |
| wkt               | longtext     | YES      | NULL    |
| isbie             | bit(1)       | YES      | NULL    |
| issds             | bit(1)       | YES      | NULL    |
| authority         | varchar(255) | YES      | NULL    |
| category          | varchar(255) | YES      | NULL    |
| generalisation    | varchar(255) | YES      | NULL    |
| region            | varchar(255) | YES      | NULL    |
| sds_type          | varchar(255) | YES      | NULL    |
| user_id           | varchar(255) | YES      | NULL    |
| is_authoritative  | bit(1)       | YES      | NULL    |
| is_invasive       | bit(1)       | YES      | NULL    |
| is_threatened     | bit(1)       | YES      | NULL    |

