# New workflow for automating authoritative lists

### NOTE: UNDER CONSTRUCTION

## Overall workflow

This is going to be an apache airflow job, running once a week on **needs to be confirmed** Tuesdays at midnight.  The workflow will consist of the following:

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