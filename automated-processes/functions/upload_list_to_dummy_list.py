from datetime import datetime

import numpy as np
import pandas as pd
from functions import list_functions as lf
from functions.vocab import (
    all_species_ste_terr_column_names,
    all_species_ste_terr_column_names_use,
    all_species_ste_terr_column_rename,
    all_species_urls,
    list_ids_species_dummy_test,
)

# set this option
pd.set_option("future.no_silent_downcasting", True)


def upload_list_to_dummy_list(ste_terr=None, args=None):

    # TODO: replace "FAMILY NOT ASSIGNED" in SA with empty string

    # first, get the url for the list
    list_of_urls = all_species_urls[ste_terr]

    # now, consider all the cases
    dataFrame = pd.DataFrame()

    # define column names we want
    col_names = [
        "verbatimScientificName",
        "verbatimVernacularName",
        "verbatimRank",
        "verbatimFamily",
        "verbatimScientificNameAuthorship",
    ]
    all_col_names = col_names + all_species_ste_terr_column_names_use[ste_terr]

    # loop over all urls to get a dataframe
    for url in list_of_urls:

        if "xls" in url:
            if ste_terr == "SA":
                xls = pd.ExcelFile(url)
                temp_df = pd.read_excel(xls, sheet_name=xls.sheet_names[1])
            else:
                temp_df = pd.read_excel(url)

            if ste_terr == "SA":
                # print(temp_df['FAMILYNAME'])
                temp_df["FAMILYNAME"] = temp_df["FAMILYNAME"].str.lower()
                temp_df["FAMILYNAME"] = temp_df["FAMILYNAME"].str.capitalize()

                if "SPECIES AUTHOR" not in temp_df.columns:
                    temp_df = temp_df.rename(
                        columns={"SPECIES with AUTHOR": "SPECIES AUTHOR"}
                    )

            # print(temp_df[['SPECIES', 'SPECIES_NAME', 'CURRENT_SPECIES_NAME','PREFERRED_COMMON_NAMES', 'SPECIES_AUTHORITY', 'SPECIES_PUBLICATION','INFRASPECIES_RANK', 'INFRASPECIES',]].head())

            # if ste_terr == "TAS":
            #     test = temp_df[temp_df['CURRENT_SPECIES_NAME'].notnull()]
            #     print(test[['SPECIES', 'SPECIES_NAME', 'CURRENT_SPECIES_NAME','PREFERRED_COMMON_NAMES', 'SPECIES_AUTHORITY', 'SPECIES_PUBLICATION','INFRASPECIES_RANK', 'INFRASPECIES',]])
            #     import sys
            #     sys.exit()

        elif "csv" in url:

            # read it into a data frame
            temp_df = pd.read_csv(url)

            if ste_terr == "WA":
                temp_df["rank"] = temp_df["rank"].str.lower()

        else:
            # get the data from the url
            temp_df = lf.webscrape_list_url(state=ste_terr, url=url)

            # check for this for NSW
            if ste_terr in ["NSW"]:

                # only select current names
                temp_df = temp_df[temp_df["isCurrent"] == "true"]

        # copy all of these values to their verbatim cousins to preserve the original naming; create empty strings if not
        for name in col_names:
            if all_species_ste_terr_column_names[ste_terr][name] is not None:
                temp_df[name] = temp_df[
                    all_species_ste_terr_column_names[ste_terr][name]
                ].copy()
            else:
                temp_df[name] = ""

        # only for testing purposes
        temp_df = temp_df.head(n=100)

        # concatenate the processed dataframe onto the overall one
        dataFrame = pd.concat([dataFrame, temp_df])

    # remove any white spaces and NaNs
    dataFrame = dataFrame.replace(r"^ +| +$", r"", regex=True)
    dataFrame = dataFrame.replace(np.nan, "")

    # select only the columns we want
    dataFrame = dataFrame[all_col_names]

    # rename columns if necessary
    dataFrame = dataFrame.rename(columns=all_species_ste_terr_column_rename[ste_terr])

    columns_to_check = [
        "scientificName",
        "vernacularName",
        "rank",
        "family",
        "scientificNameAuthorship",
    ]
    if any(x not in dataFrame.columns for x in columns_to_check):
        for x in columns_to_check:
            if x not in dataFrame.columns:
                dataFrame[x] = ""

    # for Victoria, make sure to update the rank for better identification
    if ste_terr == "VIC":
        dataFrame["rank"] = dataFrame["rank"].replace("spec", "species")

    # write the dummy list to a csv
    dataFrame.to_csv(
        "data/new-lists/all-species-{}-{}.csv".format(
            ste_terr, datetime.now().strftime("%Y-%m-%d")
        ),
        index=False,
    )

    # # only choose which columns to upload
    # lf.post_list_to_test(
    #     list_data=dataFrame,
    #     state=ste_terr,
    #     druid=list_ids_species_dummy_test[ste_terr],
    #     list_type="ALL",
    #     args=args,
    # )
