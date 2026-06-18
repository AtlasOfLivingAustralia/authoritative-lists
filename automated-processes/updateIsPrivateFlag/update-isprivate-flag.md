# Lists isPrivate flag update using graphql

Script to identify and update lists to be made private based on defined criteria.
Updating the collectory dataresource `isPrivate` flag does not flow through to the list itself. This is a problem as the `Lists API` does not currently expose the list `isPrivate` flag. 

The option is to update

Direct update of the lists database is fraught with error and 

## Criteria for list selection for update?
List must be `non-authoritative` and meet the following criteria:

   1. Lists with zero records
   2. Lists with only 1 record
   3. Lists marked with list type – “Test%”
   4. Lists with list name contains "test%"
   5. Exclude BioCollect Lists


