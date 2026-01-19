import math

import pandas as pd
from functions import list_functions as lf
from datetime import datetime

from .vocab import get_listsTest, list_ids_species_dummy_test, urlSuffix


def compile_all_species_lists(args=None):

    # initialise the dataframe
    presence_states = [
        "presence_{}".format(state) for state in list_ids_species_dummy_test
    ]
    columns_list = [
        "verbatimScientificName",
        "verbatimVernacularName",
        "verbatimRank",
        "verbatimFamily",
        "verbatimScientificNameAuthorship",
        "scientificName",
        "vernacularName",
        "rank",
        "family",
        "scientificNameAuthorship",
    ]
    columns = columns_list + presence_states
    overall_df = pd.DataFrame(columns=columns)

    for state in list_ids_species_dummy_test:
        
        # download the test
        oldListUrl = get_listsTest + list_ids_species_dummy_test[state] + urlSuffix
        oldList = lf.download_ala_specieslist(oldListUrl)
        oldList = lf.kvp_to_columns(oldList)
        oldList["presence_{}".format(state)] = "Yes"
        for col in columns_list:
            if col not in oldList.columns:
                oldList[col] = ""

        # if the overall dataframe
        if overall_df.empty:
            nonmatching_rows = oldList
            nonmatching_rows["presence_{}".format(state)] = "Yes"

        else:

            # get matching indices for the whole conservation list
            matching_indices_all_conservation = overall_df[
                overall_df["verbatimScientificName"].isin(
                    oldList["verbatimScientificName"]
                )
            ].index.tolist()

            # get matching rows with indices
            matching_indices_list_df = oldList[
                oldList["verbatimScientificName"].isin(
                    overall_df["verbatimScientificName"]
                )
            ].index.tolist()

            # get nonmatching rows to concatenate
            nonmatching_rows = oldList.drop(matching_indices_list_df)

            # if there are matching rows, go through and add sourceStatus to extant row
            if len(matching_indices_all_conservation) > 0:
                for j in matching_indices_all_conservation:
                    overall_df.at[j, "presence_{}".format(state)] = "Yes"

        # concatenate the nonmatching rows onto the all_conservation list
        overall_df = pd.concat(
            [
                overall_df,
                nonmatching_rows[columns_list + ["presence_{}".format(state)]],
            ]
        ).reset_index(drop=True)

    # how to replace all NaNs with empty strings
    overall_df = overall_df.replace(math.nan, "")

    # write list to csv for upload (may change this later)
    temp_filename = "all-compiled-species-{}.csv".format(
        datetime.now().strftime("%Y-%m-%d")
    )
    overall_df.to_csv("data/new-lists/{}".format(temp_filename), index=False)
