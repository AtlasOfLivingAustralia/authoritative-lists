from datetime import datetime
import math

import pandas as pd
from . import list_functions as lf
from .vocab import (
    all_conservation_lists,
    get_listsTest,
    list_ids_conservation_test,
    urlSuffix,
    all_conservation_druid,
)


def compile_conservation_lists(args=None):

    # initialise the dataframe and column names for all conservation lists compilation
    sourceStatus = ["sourceStatus_{}".format(state) for state in all_conservation_lists]
    columns = (
        ["verbatimScientificName", "scientificName"]
        + sourceStatus
        + ["family", "rank", "commonName"]
    )
    all_conservation = pd.DataFrame(columns=columns)

    # initialise common columns for each list
    columns_list_df = [
        "scientificName",
        "verbatimScientificName",
        "family",
        "rank",
        "commonName",
    ]

    # loop over all conservation lists
    for i, state in enumerate(all_conservation_lists):

        # download state/territory/birds conservation
        url = get_listsTest + list_ids_conservation_test[state] + urlSuffix
        kvps_conservation = lf.download_ala_specieslist(url=url)
        list_df = lf.kvp_to_columns(kvps_conservation).reset_index(drop=True)

        # add temporary change to change raw to verbatim; also check if there are supplied names
        if all(
            x not in list_df.columns
            for x in ["raw_scientificName", "verbatimScientificName"]
        ):
            list_df["verbatimScientificName"] = list_df["scientificName"].copy()
        elif "raw_scientificName" in list_df.columns:
            list_df = list_df.rename(
                columns={"raw_scientificName": "verbatimScientificName"}
            )

        # rename columns for
        list_df = list_df.rename(
            columns={"sourceStatus": "sourceStatus_{}".format(state)}
        )

        # add rank
        if "rank" not in list_df.columns:
            list_df["rank"] = ""

        # get matching and nonmatching rows
        if i != 0:

            # get matching indices for the whole conservation list
            matching_indices_all_conservation = all_conservation[
                all_conservation["verbatimScientificName"].isin(
                    list_df["verbatimScientificName"]
                )
            ].index.tolist()

            # get matching rows with indices
            matching_indices_list_df = list_df[
                list_df["verbatimScientificName"].isin(
                    all_conservation["verbatimScientificName"]
                )
            ].index.tolist()
            matching_rows = list_df.iloc[matching_indices_list_df]

            # get nonmatching rows to concatenate
            nonmatching_rows = list_df.drop(matching_indices_list_df)

            # if there are matchign rows, go through and add sourceStatus to extant row
            if len(matching_indices_all_conservation) > 0:
                for j in matching_indices_all_conservation:
                    name = all_conservation["verbatimScientificName"][j]
                    index = list_df[list_df["verbatimScientificName"] == name].index[0]
                    all_conservation.at[j, "sourceStatus_{}".format(state)] = (
                        matching_rows[matching_rows["verbatimScientificName"] == name][
                            "sourceStatus_{}".format(state)
                        ][index]
                    )

        else:

            # otherwise, the list hasn't been initialised and we will concatenate all the species
            nonmatching_rows = list_df

        # concatenate the nonmatching rows onto the all_conservation list
        all_conservation = pd.concat(
            [
                all_conservation,
                nonmatching_rows[columns_list_df + ["sourceStatus_{}".format(state)]],
            ]
        ).reset_index(drop=True)

    # how to replace all NaNs with empty strings
    all_conservation = all_conservation.replace(math.nan, "")

    # post list to test
    # TODO: change this
    lf.post_list_to_test(
        list_data=all_conservation,
        state=state,
        druid=all_conservation_druid,
        list_type="C",
        args=args,
    )

    # write list to csv for upload (may change this later)
    temp_filename = "all-conservation-lists-{}.csv".format(
        datetime.now().strftime("%Y-%m-%d")
    )
    all_conservation.to_csv("data/temp-new-lists/{}".format(temp_filename), index=False)
