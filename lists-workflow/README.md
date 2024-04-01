# New workflow for automating authoritative lists

### NOTE: UNDER CONSTRUCTION

## Overall workflow

This is going to be an apache airflow job, running once a week on **needs to be confirmed** Tuesdays at midnight.  The workflow will consist of the following:

1. Download the following authoritiative conservation and sensitive lists from relevant links:

    | State | Conservation | Sensitive |
    |-------|--------------|-----------|
    | ACT   |       X      |           |
    | NT    |       X      |           |
    | NSW   |       X      |     X     |
    | QLD   |       X      |     X     |
    | TAS   |       X      |           |
    | VIC   |       X      |     X     |
    | WA    |       X      |     X     |


2. Compare them with the current 