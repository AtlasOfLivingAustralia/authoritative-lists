## Report Scripts
Python scripts to:

1. Generate change logs for Conservation Lists and Sensitive Lists
2. Extract list information for all lists

## Change Logs

Directory of change log CSV files output from Report Scripts

## Mysql
**Note: These scripts are not currently in use.**

**ala-lists-create.mysql**

Script to query lists write records to temp table. 
List must be non-authoritative and meet the following criteria:
   - Lists with zero records
   - Lists with only 1 record
   - Lists marked with list type – “Test%”
   - Lists NOT marked with list type “Test%” and List name contains "test%"

**ala-lists-check-update.mysql**

Script to recheck data in species_list is updated as expected by extracting same data into a 
check_list then examining is_private flag
