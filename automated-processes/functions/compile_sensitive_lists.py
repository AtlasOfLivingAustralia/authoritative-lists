import math
from datetime import datetime

import pandas as pd
from functions import list_functions as lf
from .vocab import (
    all_sensitive_druid_test,
    all_sensitive_lists,
    get_listsTest,
    list_ids_sensitive_test,
    urlSuffix,
)


def compile_sensitive_lists(args=None):

    print("compiling sensitive lists")

    # initialise the dataframe and column names for all sensitive lists compilation
    generalisation = [
        "generalisation_{}".format(state) for state in all_sensitive_lists
    ]
    columns = (
        ["verbatimScientificName", "scientificName"]
        + generalisation
        + ["family", "rank", "commonName"]
    )
    all_sensitive = pd.DataFrame(columns=columns)

    # initialise common columns for each list
    columns_list_df = [
        "scientificName",
        "verbatimScientificName",
        "family",
        "rank",
        "commonName",
    ]

    # loop over all sensitive lists
    for i, state in enumerate(all_sensitive_lists):

        # download state/territory/birds sensitive
        url = get_listsTest + list_ids_sensitive_test[state] + urlSuffix
        kvps_sensitive = lf.download_ala_specieslist(url=url)
        list_df = lf.kvp_to_columns(kvps_sensitive).reset_index(drop=True)

        # add temporary change to change raw to verbatim; also check if there are supplied names
        if "verbatimScientificName" not in list_df.columns:
            list_df["verbatimScientificName"] = list_df["scientificName"].copy()

        # rename columns for
        list_df = list_df.rename(
            columns={"generalisation": "generalisation_{}".format(state)}
        )

        # add rank
        if "rank" not in list_df.columns:
            list_df["rank"] = ""

        # add generalisation for BirdLife
        if state == "BirdLife":
            list_df["generalisation_BirdLife"] = "10km"

        # get matching and nonmatching rows
        if i != 0:

            # get matching indices for the whole sensitive list
            matching_indices_all_sensitive = all_sensitive[
                all_sensitive["verbatimScientificName"].isin(
                    list_df["verbatimScientificName"]
                )
            ].index.tolist()

            # get matching rows with indices
            matching_indices_list_df = list_df[
                list_df["verbatimScientificName"].isin(
                    all_sensitive["verbatimScientificName"]
                )
            ].index.tolist()
            matching_rows = list_df.iloc[matching_indices_list_df]

            # get nonmatching rows to concatenate
            nonmatching_rows = list_df.drop(matching_indices_list_df)

            # if there are matching rows, go through and add generalisation to extant row
            if len(matching_indices_all_sensitive) > 0:
                for j in matching_indices_all_sensitive:
                    name = all_sensitive["verbatimScientificName"][j]
                    index = list_df[list_df["verbatimScientificName"] == name].index[0]
                    all_sensitive.at[j, "generalisation_{}".format(state)] = (
                        matching_rows[matching_rows["verbatimScientificName"] == name][
                            "generalisation_{}".format(state)
                        ][index]
                    )

        else:

            # otherwise, the list hasn't been initialised and we will concatenate all the species
            nonmatching_rows = list_df

        # concatenate the nonmatching rows onto the all_sensitive list
        all_sensitive = pd.concat(
            [
                all_sensitive,
                nonmatching_rows[columns_list_df + ["generalisation_{}".format(state)]],
            ]
        ).reset_index(drop=True)

    # how to replace all NaNs with empty strings
    all_sensitive = all_sensitive.replace(math.nan, "")

    # post list to test
    # lf.post_list_to_test(
    #     list_data=all_sensitive,
    #     state=state,
    #     druid=all_sensitive_druid_test,
    #     list_type="S",
    #     args=args,
    # )

    # write list to csv for upload (may change this later)
    temp_filename = "all-sensitive-{}.csv".format(datetime.now().strftime("%Y-%m-%d"))
    all_sensitive.to_csv("data/temp-new-lists/{}".format(temp_filename), index=False)
