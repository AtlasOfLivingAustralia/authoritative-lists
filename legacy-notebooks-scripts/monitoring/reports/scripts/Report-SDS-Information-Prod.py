##############################################################################################
#
# SDS List Information Report
#  Extract SDS Information for each state
# For each sensitive species list:
# - Extract counts for Sensitive Assertions: generalised, alreadyGeneralised, not supplied
# - Extract species count for each
# - Write to markdown file
#
# Output information files to : ..\authoritative-lists\Monitoring\SDS-Information-<date>.md
##############################################################################################
#
import sys
import os
import urllib.request
import json
import certifi
import ssl
import datetime
import tabulate
import pandas as pd
import os.path as path

projectDir = path.abspath(path.join(os.getcwd(), "../..")) + "/"
outDir = projectDir + "reports/"
sys.path.append(os.path.abspath(projectDir + "source-code/includes"))
# monthStr = datetime.datetime.now().strftime('%Y%m%d')
monthStr = datetime.datetime.now().strftime("%Y-%m-%d")


##############################################################################################


def download_url(urlprefix: str, urlsuffix: str, drId: str):
    lUrl = urlprefix + drId + urlsuffix
    print("download from: ", lUrl)
    with urllib.request.urlopen(
        lUrl, context=ssl.create_default_context(cafile=certifi.where())
    ) as lUrl:
        if lUrl.status == 200:
            data = json.loads(lUrl.read().decode())
            data = pd.json_normalize(data)
        else:
            # Handle the error
            print("Error in download_ala_list:", lUrl.status)
    return data, lUrl


def concat_columns(row, col_pairs):
    for tcol, new_tcol, lcol in col_pairs:
        row[new_tcol] = "[" + row[tcol] + "]" + row[lcol]
    return row


def build_markdown(df, dStr):
    # Create markdown from dataframe, add headers and description
    mheader = "## State Sensitive Species Lists - Occurrence Assertions Summary \n"
    updateInfo = "### Date Last Updated: " + dStr + "\n"
    mfooter = "\n"
    d1 = (
        "\n The table below summarises the occurrence record count for sensitive species \
                   within each of the states respectively.\n"
    )
    d2 = "\n * The location of each occurrence should be generalised within the species list state. "
    d3 = "\n * The value of **Not Supplied** should always be zero. \n\n"
    # Format links for markdown
    tcols = [
        "ListID",
        "Total Occurrences",
        "Generalised",
        "Already Generalised",
        " Not Supplied",
    ]
    lcols = ["splUrl", "tcUrl", "gUrl", "agUrl", "nsUrl"]
    df[tcols] = df[tcols].astype(str)
    df[lcols] = df[lcols].astype(str).apply(lambda x: "(" + x + ")")
    # Create column pairs from tcols and lcols
    colpairs = list(zip(tcols, ["New" + col for col in tcols], lcols))
    df = df.apply(lambda row: concat_columns(row, colpairs), axis=1)
    # Drop the original columns
    df = df.drop(
        columns=[col for col in df.columns if col in set(sum([tcols, lcols], []))]
    )
    df.columns = df.columns.str.replace("New", "")
    df = df.iloc[:, [0, 3, 1, 4, 2, 5, 6, 7]]
    mdf = df.to_markdown(index=False)
    mdf = mheader + updateInfo + d1 + d2 + d3 + mdf + mfooter

    return mdf


def get_sds_info(state, sName, drId):
    # Get number of records in Species list
    lprefix = "https://lists.ala.org.au/speciesListItem/list/"
    urlprefix = "https://api.ala.org.au/specieslist/ws/speciesList/"
    urlsuffix = ""
    data, splUrl = download_url(urlprefix, urlsuffix, drId)
    splUrl.url = splUrl.url.replace(urlprefix, lprefix)
    splCt = data["itemCount"][0]

    apiPrefix = "https://api.ala.org.au/occurrences/occurrences"
    bioPrefix = "https://biocache.ala.org.au/occurrence"

    # Total Occurrences
    urlprefix = (
        "https://api.ala.org.au/occurrences/occurrences/search?q=species_list_uid%3A"
    )
    urlsuffix = "&fq=state%3A%22" + sName + "%22"
    data, tcUrl = download_url(urlprefix, urlsuffix, drId)
    tcUrl.url = tcUrl.url.replace(apiPrefix, bioPrefix)
    totCt = data["totalRecords"][0]

    # Generalised count
    urlprefix = (
        "https://api.ala.org.au/occurrences/occurrences/search?q=species_list_uid%3A"
    )
    urlsuffix = "&fq=sensitive%3Ageneralised&fq=state%3A%22" + sName + "%22"
    data, gUrl = download_url(urlprefix, urlsuffix, drId)
    gUrl.url = gUrl.url.replace(apiPrefix, bioPrefix)
    genCt = data["totalRecords"][0]

    # Already Generalised
    urlsuffix = "&fq=sensitive%3AalreadyGeneralised&fq=state%3A%22" + sName + "%22"
    data, agUrl = download_url(urlprefix, urlsuffix, drId)
    agUrl.url = agUrl.url.replace(apiPrefix, bioPrefix)
    aGenCt = data["totalRecords"][0]

    # Not supplied
    urlsuffix = "&fq=-sensitive%3A*&fq=state%3A%22" + sName + "%22"
    data, nsUrl = download_url(urlprefix, urlsuffix, drId)
    nsUrl.url = nsUrl.url.replace(apiPrefix, bioPrefix)
    nsCt = data["totalRecords"][0]

    # Species count
    urlprefix = (
        "https://api.ala.org.au/occurrences/occurrences/facets?q=species_list_uid%3A"
    )
    urlsuffix = "&facets=species"
    data, spctUrl = download_url(urlprefix, urlsuffix, drId)
    spCt = data["count"][0]

    values = [
        state,
        drId,
        splCt,
        totCt,
        spCt,
        genCt,
        aGenCt,
        nsCt,
        splUrl.url,
        tcUrl.url,
        gUrl.url,
        agUrl.url,
        nsUrl.url,
    ]
    return values


##############################################################################################
# Production Sensitive Lists


drDict = {
    "ACT": "dr2627",
    "NSW": "dr487",
    "NT": "dr492",
    "QLD": "dr493",
    "SA": "dr884",
    "TAS": "dr491",
    "VIC": "dr490",
    "WA": "dr467",
}

# drDict = {"ACT":"dr2627"}

stateNames = {
    "ACT": "Australian+Capital+Territory",
    "NSW": "New+South+Wales",
    "NT": "Northern+Territory",
    "QLD": "Queensland",
    "SA": "South+Australia",
    "TAS": "Tasmania",
    "VIC": "Victoria",
    "WA": "Western+Australia",
}

cols = [
    "State",
    "ListID",
    "#Species in list",
    "Total Occurrences",
    "Unique Species count",
    "Generalised",
    "Already Generalised",
    " Not Supplied",
    "splUrl",
    "tcUrl",
    "gUrl",
    "agUrl",
    "nsUrl",
]

# Create dataframe of summary information
summarydf = pd.DataFrame(columns=cols)
for state, dr in drDict.items():
    sName = stateNames[state]
    row_data = get_sds_info(state, sName, dr)
    summarydf = pd.concat(
        [summarydf, pd.DataFrame([row_data], columns=cols)], ignore_index=True
    )

# Build markdown
mdsdf = build_markdown(summarydf, monthStr)
mfile = outDir + "SDS-Assertions-Information" + ".md"
print(f"Writing report to markdown file: {mfile}")
with open(mfile, "w") as f:
    f.write(mdsdf)
print("Finished Processing")
