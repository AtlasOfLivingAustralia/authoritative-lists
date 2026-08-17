import math

import pandas as pd
from functions import list_functions as lf
from datetime import datetime
import requests

from .vocab import all_species_urls,all_species_ste_terr,all_species_ste_terr_druid_test,list_ids_species_dummy_test


def compile_all_species_lists(args=None):

    # initialise the columns and the dataframe
    presence_states = [
        "presence_{}".format(state) for state in all_species_ste_terr
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

    ### Upload all overall species list to their respective "dummy" lists for namematching
    for state in all_species_ste_terr:
        response = requests.get(all_species_urls[state])

    ### Download all lists from namematching and check which species are present in which state
    for state in all_species_ste_terr:
        n=1

    ### Write list to disk and upload to ALA

    


    #     # if the overall dataframe
    #     if overall_df.empty:
    #         nonmatching_rows = oldList
    #         nonmatching_rows["presence_{}".format(state)] = "Yes"

    #     else:

    #         # get matching indices for the whole conservation list
    #         matching_indices_all_conservation = overall_df[
    #             overall_df["verbatimScientificName"].isin(
    #                 oldList["verbatimScientificName"]
    #             )
    #         ].index.tolist()

    #         # get matching rows with indices
    #         matching_indices_list_df = oldList[
    #             oldList["verbatimScientificName"].isin(
    #                 overall_df["verbatimScientificName"]
    #             )
    #         ].index.tolist()

    #         # get nonmatching rows to concatenate
    #         nonmatching_rows = oldList.drop(matching_indices_list_df)

    #         # if there are matching rows, go through and add sourceStatus to extant row
    #         if len(matching_indices_all_conservation) > 0:
    #             for j in matching_indices_all_conservation:
    #                 overall_df.at[j, "presence_{}".format(state)] = "Yes"

    #     # concatenate the nonmatching rows onto the all_conservation list
    #     overall_df = pd.concat(
    #         [
    #             overall_df,
    #             nonmatching_rows[columns_list + ["presence_{}".format(state)]],
    #         ]
    #     ).reset_index(drop=True)

    # # how to replace all NaNs with empty strings
    # compiled_lists = compiled_lists.replace(math.nan, "")

    # # write list to csv for upload (may change this later)
    # temp_filename = f"all-{list_info_dict[state]["long_list_type"]}-{datetime.now().strftime("%Y-%m-%d")}.csv"
    # compiled_lists.to_csv("data/temp-new-lists/{}".format(temp_filename), index=False)

    # # post list to test
    # lf.post_list_to_test(
    #     druid=list_info_dict[state]["all_list_id"], args=args, filename=temp_filename
    # )

