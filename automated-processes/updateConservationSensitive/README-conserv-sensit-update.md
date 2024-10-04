# New workflow for automating authoritative lists

*Note:* In the workflow, there is a column called `vernacularName`, which refers to the common name used in each state.  DO NOT CHANGE THIS.  The ALA will assign each species a common name on file, if they have it, under `commonName`.  This will ensure we preserve the name that each state gives its species.

## What are Conservation vs. Sensitive Lists?
[Conservation lists](https://lists.ala.org.au/public/speciesLists?isAuthoritative=eq:true&isThreatened=eq:true) refer to lists put out by juristictions, such as 
states and territories, that have assessed the status of species in their jurisdiction.  A species is put on a conservation list if the relevant authorities determine its conservation is a cause for concern.  [Sensitive lists](https://lists.ala.org.au/public/speciesLists?isSDS=eq:true), on the other hand, may contain 
species that are not on the conservation list of said juristiction, but will have its exact locality obfuscated by our [Sensitive Data Service](https://github.com/AtlasOfLivingAustralia/sds).  The level of obfuscation depends on the level of sensitivity of the species.

For FAQs about our Sensitive Data Service, refer [here](https://rasd.org.au/pdf/RASD-FAQs.pdf).

For a full list of conservation and sensitive lists in Australia, refer to the table below:

| State/Entity                 | Conservation                                                   | Sensitive                                                      | 
|------------------------------|----------------------------------------------------------------|----------------------------------------------------------------|
| Australian Capital Territory | [dr649](https://lists.ala.org.au/speciesListItem/list/dr649)   | [dr2627](https://lists.ala.org.au/speciesListItem/list/dr2627) |
| EPBC Act                     | [dr656](https://lists.ala.org.au/speciesListItem/list/dr656)   | None                                                           |
| New South Wales              | [dr650](https://lists.ala.org.au/speciesListItem/list/dr650)   | [dr487](https://lists.ala.org.au/speciesListItem/list/dr487)   |
| Northern Territory           | [dr651](https://lists.ala.org.au/speciesListItem/list/dr651)   | [dr492](https://lists.ala.org.au/speciesListItem/list/dr492)   |
| Queensland                   | [dr652](https://lists.ala.org.au/speciesListItem/list/dr652)   | [dr493](https://lists.ala.org.au/speciesListItem/list/dr493)   |
| South Australia              | [dr653](https://lists.ala.org.au/speciesListItem/list/dr653)   | [dr884](https://lists.ala.org.au/speciesListItem/list/dr884)   |
| Tasmania                     | [dr654](https://lists.ala.org.au/speciesListItem/list/dr654)   | [dr491](https://lists.ala.org.au/speciesListItem/list/dr491)   |
| Victoria                     | [dr655](https://lists.ala.org.au/speciesListItem/list/dr655)   | [dr490](https://lists.ala.org.au/speciesListItem/list/dr490)   |
| Western Australia            | [dr2201](https://lists.ala.org.au/speciesListItem/list/dr2201) | [dr467](https://lists.ala.org.au/speciesListItem/list/dr467)   |

## Overall workflow

This is going to be **needs to be confirmed** *a cron job*, running **needs to be confirmed** *once a week on Thursdays at midnight*.  The workflow will consist of the following:

1. Download the following authoritiative conservation and sensitive lists from each state using relevant links.  Below list is what is automatically updated with this workflow:

    | State/Entity                 | Conservation | Sensitive |
    |------------------------------|--------------|-----------|
    | Australian Capital Territory |       X      |           |
    | EPBC Act                     |       X      |           |
    | New South Wales              |       X      |     X     |
    | Northern Territory           |       X      |           |
    | Queensland                   |       X      |     X     |
    | South Australia              |              |           |
    | Tasmania                     |              |           |
    | Victoria                     |       X      |     X     |
    | Western Australia            |       X      |     X     |



2. Compare them with the current lists on the ALA to determine what changes, if any, have been made.
3. Email relevant parties to check the updates to the list.
4. Once relevant parties have approved changes, upload changes to production.

## Files and requirements you need before use

To install all requirements, run

    pip install -r requirements.txt

You will need 4 files in the same directory as the `conservation-sensitive-update.py` to have this run correctly:

```
login.txt
ids.txt
auth-confidential.json
s3_info.txt
```

Description and formats:

#### `login.txt`

Username and Password for your CSIRO email (default name is `login.txt`, specify filename with `-eid` argument).

```
username = USERNAME
password = PASSWORD
```

#### `ids.txt`

Your ALA client ID and your secret client ID **for the test environment** (default name is `ids.txt`; specify filename by using `-cids` argument).

```
client_id = CLIENT_ID
client_secret = CLIENT_SECRET
```

#### `auth-confidential.txt`

ALA Authentication json file (default name is `auth-confidential.json`, specify filename by using `-auth` argument).  To download your authentication, go [here from test for now](https://auth-secure.auth.ap-southeast-2.amazoncognito.com/login?response_type=code&redirect_uri=https%3A%2F%2Faws-auth-test-2023.test.ala.org.au%2Fuserdetails%2Fcallback%3Fclient_name%3DOidcClient&state=059c4be224&client_id=61mj7ivlmf22e5588lgtr8vi7d&scope=openid+profile+email+ala%2Fattrs+ala%2Froles+aws.cognito.signin.user.admin>)


#### `s3_info.txt`

Your s3 bucket information, along with the directories in that bucket (default name is `s3_info.txt`; specify filename by using `-s3` argument).

```
bucket = BUCKET
key_conservation_changes = CONSERVATION_CHANGES_DIR
key_sensitive_changes = SENSITIVE_CHANGES_DIR
key_conservation_lists = CONSERVATION_LISTS_DIR
key_sensitive_lists = SENSITIVE_LISTS_DIR
key_conservation_historical = CONSERVATION_HISTORICAL_DIR
key_sensitive_historical = SENSITIVE_HISTORICAL_DIR
```

## How to run the script

**Note: The option to upload and send email by default is False.  When you're ready to run it for manual checks, set these to True.**

To run the script for all lists we are able to update, type the following into the command line.

    python conservation-sensitive-update.py

To get changes for specific lists, use the `-cl` (conservation lists) or `-sl` (sensitive lists) arguments:

    python conservation-sensitive-update.py -cl QLD,NSW
    python conservation-sensitive-update.py -cl WA

To run the script including the upload and email options, you will have to set up access to ALA's AWS instance. See [this confluence page](https://confluence.csiro.au/display/ALASD/AWS+access) for more information, or ask Joe.

    prod-login
    python conservation-sensitive-update.py -up True -sem True