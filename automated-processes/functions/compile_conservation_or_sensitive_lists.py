import math
from datetime import datetime

import pandas as pd

from . import list_functions as lf
from .vocab import (
    get_listsTest,
    all_conservation_druid_test,
    all_conservation_lists,
    list_ids_conservation_test,
    all_sensitive_druid_test,
    all_sensitive_lists,
    list_ids_sensitive_test,
)


def compile_conservation_or_sensitive_lists(args=None, list_type=None):

    # check if correct list type is specified
    if list_type not in ["C", "S"]:
        raise ValueError('Only "C" and "S" are accepted values')

    # specify all variables
    list_info_dict = {
        "C": {
            "long_list_type": "conservation",
            "status_or_gen": "sourceStatus",
            "all_state_terr_names": all_conservation_lists,
            "all_list_ids_test": list_ids_conservation_test,
            "all_list_id": all_conservation_druid_test,
        },
        "S": {
            "long_list_type": "sensitive",
            "status_or_gen": "generalisation",
            "all_state_terr_names": all_sensitive_lists,
            "all_list_ids_test": list_ids_sensitive_test,
            "all_list_id": all_sensitive_druid_test,
        },
    }

    # let user know if they are compiling conservation or sensitive lists
    print(f"compiling {list_info_dict[list_type]["long_list_type"]} lists")

    # initialise the dataframe and column names for all conservation lists compilation
    status_or_gen_array = [
        f"{list_info_dict[list_type]["status_or_gen"]}_{state}"
        for state in list_info_dict[list_type]["all_state_terr_names"]
    ]
    columns = [
        "verbatimScientificName",
        "scientificName",
        "rank",
    ] + status_or_gen_array
    compiled_lists = pd.DataFrame(columns=columns)

    # initialise common columns for each list
    columns_list_df = [
        "scientificName",
        "verbatimScientificName",
        "rank",
    ]

    # loop over all conservation lists
    for i, state in enumerate(list_info_dict[list_type]["all_state_terr_names"]):

        # download state/territory/birds sensitive
        url = get_listsTest.replace(
            "{speciesListID}", list_info_dict[list_type]["all_list_ids_test"][state]
        )  # + urlSuffix
        list_df = pd.read_csv(url)

        # add temporary change to change raw to verbatim; also check if there are supplied names
        if "verbatimScientificName" not in list_df.columns:
            list_df["verbatimScientificName"] = list_df["scientificName"].copy()

        # add this for BirdLIfe
        if state == "BirdLife":
            list_df["generalisation_BirdLife"] = "10km"
        
        # rename columns to ensure each state and territory has their own status
        list_df = list_df.rename(
            columns={
                f"{list_info_dict[list_type]["status_or_gen"]}": f"{list_info_dict[list_type]["status_or_gen"]}_{state}"
            }
        )

        # add rank
        if "rank" not in list_df.columns:
            list_df["rank"] = ""

        # drop duplicate columns
        if "family.1" in list_df.columns:
            list_df = list_df.drop(columns=["family.1"])
        if "vernacularName.1" in list_df.columns:
            list_df = list_df.drop(columns=["vernacularName.1"])

        # get matching and nonmatching rows
        if i != 0:

            # get matching indices for the whole conservation list
            matching_indices_compiled_lists = compiled_lists[
                compiled_lists["verbatimScientificName"].isin(
                    list_df["verbatimScientificName"]
                )
            ].index.tolist()

            # get matching rows with indices
            matching_indices_list_df = list_df[
                list_df["verbatimScientificName"].isin(
                    compiled_lists["verbatimScientificName"]
                )
            ].index.tolist()
            matching_rows = list_df.iloc[matching_indices_list_df]

            # get nonmatching rows to concatenate
            nonmatching_rows = list_df.drop(matching_indices_list_df)

            # if there are matching rows, go through and add sourceStatus to extant row
            if len(matching_indices_compiled_lists) > 0:
                for j in matching_indices_compiled_lists:
                    name = compiled_lists["verbatimScientificName"][j]
                    index = list_df[list_df["verbatimScientificName"] == name].index[0]
                    compiled_lists.at[
                        j, f"{list_info_dict[list_type]["status_or_gen"]}_{state}"
                    ] = matching_rows[matching_rows["verbatimScientificName"] == name][
                        f"{list_info_dict[list_type]["status_or_gen"]}_{state}"
                    ][
                        index
                    ]

        else:

            # otherwise, the list hasn't been initialised and we will concatenate all the species
            nonmatching_rows = list_df

        # concatenate the nonmatching rows onto the all_conservation list
        compiled_lists = pd.concat(
            [
                compiled_lists,
                nonmatching_rows[
                    columns_list_df
                    + [f"{list_info_dict[list_type]["status_or_gen"]}_{state}"]
                ],
            ]
        ).reset_index(drop=True)

    # how to replace all NaNs with empty strings
    compiled_lists = compiled_lists.replace(math.nan, "")

    # write list to csv for upload (may change this later)
    temp_filename = f"all-{list_info_dict[list_type]["long_list_type"]}-{datetime.now().strftime("%Y-%m-%d")}.csv"
    compiled_lists.to_csv("data/temp-new-lists/{}".format(temp_filename), index=False)

    # post list to test
    lf.post_list_to_test(
        druid=list_info_dict[list_type]["all_list_id"], args=args, filename=temp_filename
    )
