import argparse
import datetime
import json
import sys
import time
from pathlib import Path

import archive_functions as afn
import pandas as pd
import requests
import upd_config as cfg

sys.path.append("../..")
# import functions.list_functions as lf

# from functions.ingest_lists import ingest_lists
# from functions.vocab import get_listsProd, get_listsTest


class Update_flag:
    """
    Update_flag class to update isPrivate flag on list.

    Attributes:

    Methods:

        parse_arguments() -> args:
        get_dataset() -> dataframe:

        run():
            Executes the processing of occurrences and site visits data.
    """

    def __init__(self):
        self.input_path = None
        self.output_path = None
        self.metadata = None
        self.graphql_url = None
        self.mutation_query = None
        self.accessToken = None
        self.list_headers = None  # Uses JWT Token
        self.collectory_headers = None  # Uses API Key
        self.all_df = pd.DataFrame()
        self.upd_df = pd.DataFrame()
        self.collectory_url = cfg.collectory_url
        self.collectory_api_key = cfg.collectory_api_key
        self.list_url = cfg.list_url
        self.list_info_url = cfg.list_info_url
        self.graphql_url = cfg.graphql_url
        self.keys_to_keep = cfg.keys_to_keep

    def parse_arguments(self):
        """
        Parse configuration parameters

        :return: Arguments

        """

        parser = argparse.ArgumentParser()
        parser.add_argument("--input", required=True)
        parser.add_argument("--output", required=True)
        parser.add_argument("--allfile", required=True)
        parser.add_argument("--updfile", required=True)
        parser.add_argument("--colfile", required=True)
        parser.add_argument("--list_metafile", required=True)
        parser.add_argument("--env", required=True)
        parser.add_argument("--getListInfo", required=True)
        parser.add_argument("--authentication_test", required=True)
        parser.add_argument("--authentication_prod", required=True)
        args = parser.parse_args()

        self.input_path = Path(args.input)
        self.input_path.mkdir(parents=True, exist_ok=True)
        self.output_path = Path(args.output)
        self.output_path.mkdir(parents=True, exist_ok=True)
        return args

    def prepare_mutation_query(self):
        mutation_query = """
        mutation update(
        $id: String!
        $title: String!
        $description: String
        $licence: String!
        $listType: String!
        $authority: String
        $region: String
        $isAuthoritative: Boolean
        $isPrivate: Boolean
        $isThreatened: Boolean
        $isInvasive: Boolean
        $isSDS: Boolean
        $isBIE: Boolean
        $wkt: String
        $tags: [String]
        ) {
        updateMetadata(
            id: $id
            title: $title
            description: $description
            licence: $licence
            listType: $listType
            authority: $authority
            region: $region
            isAuthoritative: $isAuthoritative
            isPrivate: $isPrivate
            isThreatened: $isThreatened
            isInvasive: $isInvasive
            isSDS: $isSDS
            isBIE: $isBIE
            wkt: $wkt
            tags: $tags
        ) {
            id
        }
        }
        """
        return mutation_query

    def download_list_info_ws(self):
        """
        Download Species list metadata for:
        non-private and non-authoritative lists

        :return: dataframe of lists
        """

        limit = 1000
        page = 1
        headers = {
            "Content-Type": "application/json",
            # "Authorization": "Bearer {}".format(self.accessToken["access_token"]),
            "Authorization": "Bearer {}".format(self.accessToken),
        }
        all_data = []
        print("Downloading list info: ")
        while True:
            url = f"{self.list_info_url}&page={page}&pageSize={limit}"
            print(f".... list: {url}")
            response = requests.get(url, headers)
            # Check if the request was successful
            if response.status_code == 200:
                data = response.json()
                if len(data["lists"]) == 0:
                    break
                data = pd.json_normalize([data])  # If the response is JSON
                all_data.extend(data["lists"][0])
                page += limit
            else:
                print(f"Error downloading: {url} Status: {response.status_code}")

        df = pd.DataFrame(all_data)
        # maybe do keys to keep here not in other function
        # df = df[self.keys_to_keep]

        return df

    def filter_lists(self, args):
        """ """
        ##Criteria for list selection for update
        # List must be `non-authoritative`, and meet the following criteria:

        #    1. Lists with zero records - rowCount
        #    2. Lists with only 1 record -rowCount
        #    3. Lists marked with list type – “Test%”
        #    4. Lists with list name contains "test%"

        notauthdf = self.all_df
        notauthdf["rowCount"] = pd.to_numeric(notauthdf["rowCount"], errors="coerce")
        # Archive non-authoritative records that meet rules criteria
        archivedf = notauthdf[
            (notauthdf["listType"].str.contains("test", case=False, na=False))
            | (notauthdf["title"].str.contains("test", case=False, na=False))
            | (notauthdf["rowCount"] <= 1)
        ]

        archivedf["isPrivate"] = True  # set isPrivate flag to true for update

        # output list record counts
        nonauthct = len(notauthdf)
        lt1rec = (notauthdf["rowCount"] <= 1).sum()
        typetest = (
            notauthdf["listType"].str.contains("test", case=False, na=False)
        ).sum()
        nametest = (notauthdf["title"].str.contains("test", case=False, na=False)).sum()

        print("  ")
        print(f"Number non-authoritative lists: {nonauthct}")
        print(f"    - # Lists with less than 2 records: {lt1rec}")
        print(f"    - # List type value contains text test: {typetest}")
        print(f"    - # List name value contains text test: {nametest}")

        print(f"Number of lists to archive: {len(archivedf)}")

        return archivedf

    def get_list_metadata(self, druid):
        # need to do this via API   - put the keys to keep in config
        lUrl = self.list_url + druid
        # response = requests.get(lUrl, headers=self.headers)
        response = requests.get(
            lUrl, headers={"Authorization": self.collectory_api_key}, timeout=60
        )
        if response.status_code == 200:
            metadata = response.json()
            for key in list(metadata.keys()):  # remove key values not used in update
                if key not in self.keys_to_keep:
                    metadata.pop(key)
            # print(f"Extracted metadata {metadata}")
            # print(f"Updated metadata: {metadata}")
        else:
            print(
                f"List metadata request failed with status code {response.status_code}"
            )
        return metadata

    # def get_collectory_metadata(self):
    #     metadata = ""
    #     metadata_df = pd.DataFrame()
    #     for druid in self.upd_df["dataResourceUid"]:
    #         lUrl = self.collectory_url + druid
    #         try:
    #             with requests.get(
    #                 # lurl, params, headers=headers, timeout=60
    #                 lUrl,
    #                 headers={"Authorization": self.collectory_api_key},
    #                 timeout=60,
    #             ) as response:
    #                 response.raise_for_status()
    #                 json_result = json.loads(response.content)
    #                 return json_result

    #         except Exception as e:
    #             print(f"Error fetching metadata for {uid}: {str(e)}")
    #         # response = requests.get(
    #         #     lUrl, headers={"Authorization": self.collectory_api_key}
    #         # )
    #         # response = requests.get(lUrl, headers=self.collectory_headers)
    #         if response.status_code == 200:
    #             metadata = response.json()
    #             print(f"{druid} -  Collectory metadata extracted, {lUrl}")
    #         else:
    #             print(
    #                 f"{druid} - Collectory metadata request for failed with status code {response.status_code}, {lUrl}"
    #             )
    #         # metadata_df.append(metadata)  # Append the returned DataFrame
    #         metadata_df = pd.concat(
    #             [metadata_df, pd.DataFrame([metadata])], ignore_index=True
    #         )
    #     # metadata_df = pd.concat(list_of_dfs, ignore_index=True)
    #     return metadata_df

    def update_list_metadata(self, row):
        # Get metadata (using API for now)
        # Update list
        # self.metadata = self.get_metadata("dr22808")
        # Change the isPrivate flag
        # self.metadata["isPrivate"] = True
        # Send the mutation using requests

        druid = row["dataResourceUid"]
        print(f"Updating list metadata: {druid}")
        metadata = self.get_list_metadata(druid)
        metadata["isPrivate"] = True
        # metadata["isPrivate"] = False
        jsonStr = {
            "query": self.mutation_query,
            "operationName": "update",
            "variables": metadata,
        }
        response = requests.post(
            self.graphql_url, headers=self.list_headers, json=jsonStr
        )
        if response.status_code != 200:
            print(f"Metadata: {metadata}")
            raise Exception(
                f"GraphQL update query error: {response.status_code} for DR: {druid} - ID: {metadata['id']}"
            )
        else:
            data = response.json()
            if "errors" in data:
                raise Exception(f"GraphQL query data error: " + str(data["errors"]))
            print(f"Updated isPrivate flag for list: {druid}")

        return ()

    def run(self):
        args = self.parse_arguments()
        # Get access token
        # self.accessToken = lf.get_authentication_info(args=args, test=True)
        self.listaccessToken = "<insert JWT Token here>"
        self.listaccessToken = "eyJraWQiOiI2UEpOaFwvdU5EYlBIWlk4Y2xmTHJvMnBKUnJhTFRXTnpaU0tOcVdka3Y0az0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI1MDJkYmE3Yy00YWFjLTQ2ZWMtOGY4Ni0xM2JkZGMxNzgyYjYiLCJjb2duaXRvOmdyb3VwcyI6WyJ1c2VyIiwiZGF0YV9wdWJsaXNoZXIiLCJhZG1pbiIsImNvbGxlY3Rpb25fYWRtaW4iLCJjb2xsZWN0b3JzX2FkbWluIl0sImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC5hcC1zb3V0aGVhc3QtMi5hbWF6b25hd3MuY29tXC9hcC1zb3V0aGVhc3QtMl9PT1hVOUdXMzkiLCJ2ZXJzaW9uIjoyLCJjbGllbnRfaWQiOiI0NjFodDJjOHBxdnVzMGVyNzNmcDBkMWlrMiIsIm9yaWdpbl9qdGkiOiJkYjExODQ3NC03ZDMxLTRhNDItYjIzNS01OGUzY2EyOTExMDgiLCJ0b2tlbl91c2UiOiJhY2Nlc3MiLCJzY29wZSI6ImFsYVwvcm9sZXMgb3BlbmlkIHByb2ZpbGUgZW1haWwiLCJhdXRoX3RpbWUiOjE3Nzc5NDY5MjUsImV4cCI6MTc3ODAzMzMyNSwiaWF0IjoxNzc3OTQ2OTI2LCJqdGkiOiIyNzY0MmExNC02ZDM4LTQ3OTctOTJmNi00MzA1MTljZDI5OTIiLCJ1c2VybmFtZSI6IjU2NTkyIn0.ucdbaK4MgVBloVwhrb9AN_EFM_aT69kb2O3hbSVjNu_NWahHOARD06xFPomKL6iM8iLRsx5-c3Bc2UiOQ2w4GALaDcTuNsJwx_BQ1V8uhxwPsDt0z3OqqBRD4RujC_5Zno8y7TUIf5jUQJT1x8EB9FxP2cJ688-qb4fDEp003t6ALYL3nEDT_B7iGAMmvD4E9qz9m2lWi0Q38NkcRCtx2pJP_gewh4Mq-Y9k_Sgfsh0Fkduil2dwjCjzxBLLYPGFH_z7rkQLjCatMShHwYTPZFyYuyA8_xZzsUiyvC2WcxNI_vSOGJeiDeNye3cGHzCqHODXmUqLKwk5DJqIsLAPYw"
        self.list_headers = {
            "Content-Type": "application/json",
            # "Authorization": "Bearer {}".format(self.accessToken["access_token"]),
            "Authorization": "Bearer {}".format(self.listaccessToken),
        }
        # self.collectory_headers = {
        #     "Content-Type": "application/json",
        #     # "Authorization": "Bearer {}".format(self.accessToken["access_token"]),
        #     "Authorization": "Bearer {}".format(self.listaccessToken),
        # }
        # Get lists to update or read file of lists to update

        if args.getListInfo == "True":
            self.all_df = (
                self.download_list_info_ws()
            )  # get all non-authoritative, non-private lists
            self.upd_df = self.filter_lists(args)  # filter based on criteria
            # self.coll_df = (
            #     self.get_collectory_metadata()
            # )  # only for saving for use later

            # Write downloaded to CSV
            self.all_df.to_csv(args.allfile, encoding="utf-8", index=False)
            self.upd_df.to_csv(args.updfile, encoding="utf-8", index=False)
            # self.coll_df.to_csv(args.colfile, encoding="utf-8", index=False)
        else:
            print("got to here ok to test time output")
            self.all_df = pd.read_csv(args.allfile, encoding="utf-8", dtype="str")
            self.upd_df = pd.read_csv(args.updfile, encoding="utf-8", dtype="str")
            # self.coll_df = pd.read_csv(
            #     args.colfile, encoding="utf-8", dtype="str"
            # )  # not needed for list updates

        # Set up query for list metadata update via graphql
        self.mutation_query = self.prepare_mutation_query()  # Prepare mutation query
        self.upd_df.apply(self.update_list_metadata, axis=1)
        # self.coll_df.apply(self.update_collectory_metadata, axis=1)    -# not to be done here

        print(f"\n Number of lists to update: {self.upd_df.shape[0]}")
        print(f"\n All lists and collectory dataresources updated successfully")


if __name__ == "__main__":
    start = time.perf_counter()
    Update_flag = Update_flag()
    Update_flag.run()
    elapsed = time.perf_counter() - start

    # Output Elapsed time information
    hours, rem = divmod(elapsed, 3600)
    minutes, seconds = divmod(rem, 60)

    print(f"\033[1mTime for Update Lists isPrivate flag script to run\033[0m")
    print(
        f"    \033[1mElapsed time\033[0m - {int(hours):02}{int(minutes):02}{seconds:06.3f}"
    )
    print(
        f"    \033[1mHH:\033[0m {int(hours):02}\n\033[1mMM:\033[0m {int(minutes):02}\n\033[1mSS:\033[0m {seconds:06.3f}"
    )
