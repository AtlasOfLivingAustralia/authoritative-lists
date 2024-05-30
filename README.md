# New workflow for automating authoritative lists

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
    | Tasmania                     |       X      |           |
    | Victoria                     |       X      |     X     |
    | Western Australia            |       X      |     X     |



2. Compare them with the current lists on the ALA to determine what changes, if any, have been made.
3. Email relevant parties to check the updates to the list.
4. Once relevant parties have approved changes, upload changes to production.

## Files and requirements you need before use

To install all requirements, run

    `pip install -r requirements.txt`

You will need 4 files to have this run correctly:

1. ALA Authentication json file (default name is `auth-confidential.json`, specify filename by using `-auth` argument).  To download your authentication, go [here from test for now](https://auth-secure.auth.ap-southeast-2.amazoncognito.com/login?response_type=code&redirect_uri=https%3A%2F%2Faws-auth-test-2023.test.ala.org.au%2Fuserdetails%2Fcallback%3Fclient_name%3DOidcClient&state=059c4be224&client_id=61mj7ivlmf22e5588lgtr8vi7d&scope=openid+profile+email+ala%2Fattrs+ala%2Froles+aws.cognito.signin.user.admin>)

2. Username and Password for your CSIRO email (default name is `login.txt`, specify filename with `-eid` argument).  Format:

    `username = USERNAME`
    `password = PASSWORD`

3. Your ALA client ID and your secret client ID (default name is `ids.txt`; specify filename by using `-cids` argument).  Format:

    `client_id = CLIENT_ID`
    `client_secret = CLIENT_SECRET`

4. Your s3 bucket information, along with the directories in that bucket (default name is `s3_info.txt`; specify filename by using `-s3` argument).  Format:

    `bucket = BUCKET`
    `key_conservation_changes = CONSERVATION_CHANGES_DIR`
    `key_sensitive_changes = SENSITIVE_CHANGES_DIR`
    `key_conservation_lists = CONSERVATION_LISTS_DIR`
    `key_sensitive_lists = SENSITIVE_LISTS_DIR`

## How to run the script

If you indent to update and send an email for all lists, run

    `python main.py`

However, there are three arguments that you can use to run this code for select lists, as well as turning the email capacity off: `-cl`, `-sl`, and `-sem`.  

First are the arguments to the conservation lists (`-cl`) and the sensitive lists (`-sl`).  The default value is `all`; however, you can specify different lists you want to run this workflow on (i.e. one didn't run correctly).  You split lists by `,` and you fill in the spaces in the states with `_`.  Examples are here using the `-cl` argument, but this can also be applied to the `-sl` arguments.

    `-cl Queensland`
    `-cl Northern_Territory`
    `-cl Queensland,Northern_Territory`

Next is the argument to choose whether or not to send an email (`-sem`).  This will inform the relevant parties that lists have been updated and need to be checked for relevance, taxonomy and any other information.  `-sem` is a boolean and is, by default, set to `True`.  Set to `False` if you are updating lists and don't want to spam the relevant parties with updates.