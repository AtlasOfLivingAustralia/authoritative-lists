## Archive Lists
Python script to archive species lists

### Archive list criteria

Lists are not authoritative lists and have one or more of the following criteria:
 -  1 or less records
 -  list type – “Test%”  (not case-sensitive)
 -  list name contains "test%"   (not case-sensitive

### Process

- Download species list information for all lists via ALA Lists API
- Extract lists to be archived - save to CSV
- Extract lists not to be archived- save to CSV
- Update collectory dataresource **isPrivate** for each list to be archived

