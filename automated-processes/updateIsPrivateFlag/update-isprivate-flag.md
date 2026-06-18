# Lists - set lists to private
| Script | Description |
| ------ | ---------- |
| **update-isprivate-flag.py** | Identify and update list `isPrivate` flag based on defined criteria |
| **update-isprivate-flag-collectory.py** | Update `isPrivate` flag in collectory metadata |

## Criteria for list selection for update?
List must be `non-authoritative` and meet the following criteria:

   1. Lists with zero records
   2. Lists with only 1 record
   3. Lists marked with list type – “Test%”
   4. Lists with list name contains "test%"
   4. Lists with list name contains "My species list"  
   5. Exclude `BioCollect` Lists

**Note**: In future updating of collectory dataresource `isPrivate` flag will be automated by new lists tool on update of list `isPrivate` flag

## Collectory API Keys

**Defined in Airflow Variables**

| Env | Variable | File |
| ---- | ---- | ------ |
| Prod |  ala_api_key | https://github.com/AtlasOfLivingAustralia/databox/blob/master/airflow/airflow-variables-production.json
| Databox |  ala_api_key | https://github.com/AtlasOfLivingAustralia/databox/blob/master/airflow/airflow-variables-databox.json |
| Databox-dev |  ala_api_key | https://github.com/AtlasOfLivingAustralia/databox/blob/master/airflow/airflow-variables-databox-dev.json |