import argparse
import datetime
import json
import sys
from pathlib import Path

import archive_functions as afn
import pandas as pd
import requests
import upd_config as cfg

sys.path.append("../")
import functions.list_functions as lf

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
        self.all_df = pd.DataFrame()
        self.upd_df = pd.DataFrame()

        self.collectory_url = cfg.collectory_url
        self.list_url = cfg.list_url
        self.list_info_url = cfg.list_info_url
        self.graphql_url = cfg.graphql_url

    def parse_arguments(self):
        """
        Parse configuration parameters

        :return: Arguments

        """

        parser = argparse.ArgumentParser()
        parser.add_argument("--input", required=True)
        parser.add_argument("--output", required=True)
        parser.add_argument("--infile", required=True)
        parser.add_argument("--outfile", required=True)
        parser.add_argument("--env", required=True)
        parser.add_argument("--client_ids", required=True)
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
        offset = 0
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.accessToken["access_token"]),
        }
        all_data = []
        print(f"Downloading list info: ")
        while True:
            url = f"{self.list_info_url}&page={page}&pageSize={limit}"
            print(f".... list: {url}")
            response = requests.get(
                url,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": "Bearer {}".format(
                        self.accessToken["access_token"]
                    ),
                },
            )
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
        # cols_to_keep = [
        #     "id",
        #     "title",
        #     "description",
        #     "listType",
        #     "licence",
        #     "authority",
        #     "region",
        #     "wkt",
        #     "isAuthoritative",
        #     "isPrivate",
        #     "isInvasive",
        #     "isThreatened",
        #     "isBIE",
        #     "isSDS",
        #     "tags",
        # ]
        # df = df[cols_to_keep]
        return df

    def download_list_info_api(self):
        """
        Download Species list metadata for:
        non-private and non-authoritative lists

        :return: dataframe of lists
        """

        limit = 1000
        offset = 0
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.accessToken["access_token"]),
        }
        all_data = []
        print(f"Downloading list info: ")
        while True:
            url = f"{self.list_info_url}&offset={offset}&limit={limit}"
            print(f".... list: {url}")
            response = requests.get(
                url,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": "Bearer {}".format(
                        self.accessToken["access_token"]
                    ),
                },
            )
            # Check if the request was successful
            if response.status_code == 200:
                data = response.json()
                if len(data["lists"]) == 0:
                    break
                data = pd.json_normalize([data])  # If the response is JSON
                all_data.extend(data["lists"][0])
                offset += limit
            else:
                print(f"Error downloading: {url} Status: {response.status_code}")

        df = pd.DataFrame(all_data)
        return df

    def filter_lists(self, args):
        """ """
        ##Criteria for list selection for update
        # List must be `non-authoritative` and meet the following criteria:

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

        # write lists info to csv - just for reference or ease of testing
        archivedf.to_csv(args.outfile, encoding="utf-8", index=False)

        archivedf["isPrivate"] = True  # set isPrivate flag to true for update

        # output list record counts
        nonauthct = len(notauthdf)
        lt1rec = (notauthdf["rowCount"] <= 1).sum()
        typetest = (
            notauthdf["listType"].str.contains("test", case=False, na=False)
        ).sum()
        nametest = (notauthdf["title"].str.contains("test", case=False, na=False)).sum()

        print(f"  ")
        print(f"Number non-authoritative lists: {nonauthct}")
        print(f"    - # Lists with less than 2 records: {lt1rec}")
        print(f"    - # List type value contains text test: {typetest}")
        print(f"    - # List name value contains text test: {nametest}")

        print(f"Number of lists to archive: {len(archivedf)}")

        return archivedf

    def update_list_metadata(self, row):
        # Get metadata (using API for now)
        # Update list
        # self.metadata = self.get_metadata("dr22808")
        # Change the isPrivate flag
        # self.metadata["isPrivate"] = True
        # Send the mutation using requests

        print(f"Updating list: {row['dataResourceUid']}")
        metadata = self.get_list_metadata(row["dataResourceUid"])
        metadata["isPrivate"] = True
        response = requests.post(
            self.graphql_url,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.accessToken["access_token"]),
            },
            json={
                "query": self.mutation_query,
                "operationName": "update",
                "variables": metadata,
            },
        )
        # print("Status:", response.status_code)
        # print("Response:", response.json())
        data = response.json()
        if "errors" in data:
            raise Exception("GraphQL query error: " + str(data["errors"]))
        print(f"Updated isPrivate flag for list: {row['dataResourceUid']}")

    def get_list_metadata(self, druid):
        # need to do this via API   - put the keys to keep in config
        keys_to_keep = [
            "id",
            "authority",
            "description",
            "isAuthoritative",
            "isInvasive",
            "isPrivate",
            "isBIE",
            "isSDS",
            "isThreatened",
            "licence",
            "listType",
            "region",
            "title",
            "wkt",
            "tags",
        ]
        lUrl = self.list_url + druid
        response = requests.get(lUrl)
        if response.status_code == 200:
            metadata = response.json()

            for key in list(metadata.keys()):  # remove key values not used in update
                if key not in keys_to_keep:
                    metadata.pop(key)
            print(f"Extracted metadata {metadata}")
            print(f"Updated metadata: {metadata}")
        else:
            print(f"Request failed with status code {response.status_code}")
        return metadata

    def run(self):
        args = self.parse_arguments()
        # Get access token
        self.accessToken = lf.get_authentication_info(args=args, test=True)
        # Get lists to update or read file of lists to update

        if args.getListInfo == "True":
            self.all_df = self.download_list_info_ws()
            self.all_df.to_csv(args.infile, encoding="utf-8", index=False)
            self.upd_df = self.filter_lists(args)
        else:
            self.all_df = pd.read_csv(args.infile, encoding="utf-8", dtype="str")
            self.upd_df = pd.read_csv(args.outfile, encoding="utf-8", dtype="str")

        # Set up query for list metadata update via graphql
        self.mutation_query = self.prepare_mutation_query()  # Prepare mutation query
        self.upd_df["retcode"] = self.upd_df.apply(self.update_list_metadata, axis=1)

        # Get collectory DR for list if it exists
        # collectory_df = self.get_collectory_to_update()
        # update collectory DR metadata
        # archivedf["cUpdStatus"] = collectory_df.apply(
        #     lambda row: update_collectory_dr(row), axis=1
        # )
        # coll_url = f"{self.collectory_url}dr22808"
        # status = afn.update_collectory_dr(coll_url)

        print(f"\n All lists and collectory dataresources updated")


if __name__ == "__main__":
    Update_flag = Update_flag()
    Update_flag.run()
