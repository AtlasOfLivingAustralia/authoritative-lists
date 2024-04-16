# Updating Authoritative Conservation and Sensitive Species Lists in the ALA

This repository is intended to document the automatic collection and preparation of Conservation and Sensitive lists from 
Australian jurisdictions into the ALA's list tool.

## Overall workflow

This is going to be an **apache airflow job (TBC)**, running once a week on **needs to be confirmed** Tuesdays at midnight.  
The workflow consists of the following:

1. Download the following authoritiative conservation and sensitive lists from each state using relevant links:

    | State | Conservation | Sensitive |
    |-------|--------------|-----------|
    | ACT   |       X      |           |
    | NT    |       X      |           |
    | NSW   |       X      |     X     |
    | QLD   |       X      |     X     |
    | TAS   |       X      |           |
    | VIC   |       X      |     X     |
    | WA    |       X      |     X     |

2. Compare them with the current lists on the ALA to determine what changes, if any, have been made.
3. Email relevant parties to check the updates to the list.
4. Once relevant parties have approved changes, upload changes to production.

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