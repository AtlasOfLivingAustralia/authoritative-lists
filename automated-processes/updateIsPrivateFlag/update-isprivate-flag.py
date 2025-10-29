import argparse
import ast
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
        self.headers = None
        self.all_df = pd.DataFrame()
        self.upd_df = pd.DataFrame()
        self.collectory_url = cfg.collectory_url
        self.list_url = cfg.list_url
        self.list_info_url = cfg.list_info_url
        self.graphql_url = cfg.graphql_url
        self.graphql_keys_to_keep = cfg.graphql_keys_to_keep

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
        all_data = []
        print("Downloading list info: ")
        while True:
            url = f"{self.list_info_url}&page={page}&pageSize={limit}"
            print(f".... list: {url}")
            response = requests.get(url, self.header_auth)
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

    def get_list_metadata(self):
        metadata = ""
        metadata_df = pd.DataFrame(columns=["dataResourceUid", "metadata"])
        for druid in self.upd_df["dataResourceUid"]:
            lUrl = self.list_url + druid
            response = requests.get(lUrl, self.header_noauth)
            if response.status_code == 200:
                metadata = None
                try:
                    metadata = response.json()
                    if metadata:
                        for key in list(
                            metadata.keys()
                        ):  # remove key values not used in update
                            if key not in self.graphql_keys_to_keep:
                                metadata.pop(key)
                        print(f"{druid} -  List metadata extracted, {lUrl}")
                        metadata["isPrivate"] = True
                        metadata_json = json.dumps(metadata)
                        metadata_df.loc[len(metadata_df)] = {
                            "dataResourceUid": druid,
                            "metadata": metadata_json,
                        }
                    else:
                        print(f"{druid} - No ist metadata")
                except ValueError:
                    # Happens when response is not valid JSON (e.g., HTML error page or plain text)
                    print(f"{druid} - Not valid JSON")
            else:
                print(
                    f"{druid} - List metadata request for failed with status code {response.status_code}, {lUrl}"
                )
        return metadata_df

    def get_collectory_metadata(self):
        metadata = ""
        metadata_df = pd.DataFrame()
        for druid in self.upd_df["dataResourceUid"]:
            lUrl = self.collectory_url + druid
            response = requests.get(lUrl, self.header_noauth)
            if response.status_code == 200:
                metadata = None
                try:
                    metadata = response.json()
                    print(f"{druid} -  Collectory metadata extracted, {lUrl}")
                except ValueError:
                    # Happens when response is not valid JSON (e.g., HTML error page or plain text)
                    print(f"{druid} - Not valid JSON")
            else:
                print(
                    f"{druid} - Collectory metadata request for failed with status code {response.status_code}, {lUrl}"
                )
            # metadata_df.append(metadata)  # Append the returned DataFrame
            if metadata:
                metadata_df = pd.concat(
                    [metadata_df, pd.DataFrame([metadata])], ignore_index=True
                )
            else:
                print(f"{druid} - No metadata")
        return metadata_df

    def update_list_metadata(self):
        # Get metadata (using API for now)
        # Update list
        # self.metadata = self.get_metadata("dr22808")
        # Change the isPrivate flag
        # self.metadata["isPrivate"] = True
        # Send the mutation using requests
        druid = "dr22810"
        df = self.list_meta_df
        # # parse string to dict

        # metadata_dict = json.loads(
        #     df.loc[df["dataResourceUid"] == druid, "metadata"].iloc[0]
        # )

        # # optionally update something, e.g., isPrivate = true
        # metadata_dict["isPrivate"] = True
        # # convert back to JSON string
        # metadata_json = json.dumps(metadata_dict)

        # Assume df is your DataFrame and you want the row where df['id']=='xxxx'
        # value_str = df.loc[df['id']=='xxxx', 'metadata'].iloc[0]
        value_str = df.loc[df["dataResourceUid"] == druid, "metadata"].iloc[0]

        # If it’s already a JSON string, you can parse it to a dict
        metadata_dict = json.loads(value_str)
        metadata_dict["isPrivate"] = True
        # Then convert back to a JSON string (this ensures valid formatting)
        json_str = json.dumps(metadata_dict)

        print(json_str)

        for druid in self.upd_df["dataResourceUid"]:
            druid = "dr22810"
            print(f"Updating list metadata: {druid}")
            metadata_dict = json.loads(
                self.list_meta_df.loc[
                    self.list_meta_df["dataResourceUid"] == druid, "metadata"
                ].iloc[0]
            )
            metadata_dict["isPrivate"] = True
            payload = {
                "query": self.mutation_query,
                "operationName": "update",
                "variables": metadata_dict,
            }
            response = requests.post(
                self.graphql_url, headers=self.header_auth, json=payload
            )
            # print(response.status_code, response.text)

            # Inspect what was sent
            print(f"Request URL:      {response.request.url}")
            print(f"Request Headers:  {response.request.headers} \n")
            # Inspect response
            print(f"Response Status:  {response.status_code}")
            print(f"Response text: {response.text}")
            print(f"Request Body:\n     {response.request.body}")
            print("\n")

            if response.status_code != 200:
                print(f"Metadata: \n {metadata_dict}")
                raise Exception(
                    f"GraphQL update query error: {response.status_code} for DR: {druid} - ID: {metadata_dict['id']}"
                )
            else:
                data = response.json()
                if "errors" in data:
                    raise Exception(f"GraphQL query data error: " + str(data["errors"]))
                print(f"Updated isPrivate flag for list: {druid}")

        return ()

    def update_collectory_dr(self, row, collectory_url) -> str:
        """
        Update list - set isPrivate flag in collectory DR

        :param row: list information from dataframe
        :return str: Update request response code
        """

        # drID = row['dataResourceUid']
        jstr = row.to_dict()
        print("POST to %s", collectory_url)
        # headers = {
        #     "Content-Type": "application/json",
        #     "Accept": "application/json",
        #     "Authorization": authorization,
        # }
        try:
            with requests.post(
                collectory_url,
                json=jstr,
                headers=self.header_auth,
            ) as response:
                if response.status_code == 200 or response.status_code == 201:
                    return str(response.status_code)
                else:
                    response.raise_for_status()
        except Exception as e:
            print("Error in creating %s: %s for %s", collectory_url, jstr, e)
            response.raise_for_status()

    # def update_collectory_dr(self, row) -> str:
    #     """
    #     Update list - set isPrivate flag in collectory DR

    #     :param row: list metadata from dataframe
    #     :return str: Update request response code
    #     """

    #     # url = self.collectory_url + row["dataResourceUid"]
    #     url = self.collectory_url + row["uid"]
    #     jstr = row.to_dict()
    #     print("POST to %s", url)
    #     try:
    #         with requests.post(url, json=jstr, headers=self.header_auth) as response:
    #             if response.status_code == 200 or response.status_code == 201:
    #                 return str(response.status_code)
    #             else:
    #                 response.raise_for_status()
    #     except Exception as e:
    #         print("Error in creating %s: %s for %s", url, jstr, e)
    #         response.raise_for_status()

    #     return ()

    def run(self):
        args = self.parse_arguments()
        # Get access token
        self.accessToken = lf.get_authentication_info(args=args, test=True)
        authorization_jwt = f"Bearer {self.accessToken}"
        self.header_noauth = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        self.header_auth = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": authorization_jwt,
        }

        # Get lists to update or read file of lists to update
        if args.getListInfo == "True":
            self.all_df = (
                self.download_list_info_ws()
            )  # get all non-authoritative, non-private lists
            self.upd_df = self.filter_lists(args)  # filter based on criteria
            self.coll_df = self.get_collectory_metadata()
            self.list_meta_df = (
                self.get_list_metadata()
            )  # isPrivate will be set to true in here

            # Write downloaded to CSV
            self.all_df.to_csv(args.allfile, encoding="utf-8", index=False)
            self.upd_df.to_csv(args.updfile, encoding="utf-8", index=False)
            self.coll_df.to_csv(args.colfile, encoding="utf-8", index=False)
            self.list_meta_df.to_csv(args.list_metafile, encoding="utf-8", index=False)
        else:
            self.all_df = pd.read_csv(
                args.allfile, encoding="utf-8", dtype="str"
            ).fillna("")
            self.upd_df = pd.read_csv(
                args.updfile, encoding="utf-8", dtype="str"
            ).fillna("")
            self.list_meta_df = pd.read_csv(
                args.list_metafile, encoding="utf-8", dtype="str"
            ).fillna("")
            self.coll_df = pd.read_csv(
                args.colfile, encoding="utf-8", dtype="str"
            ).fillna("")

        # Set up query for list metadata update via graphql
        self.mutation_query = self.prepare_mutation_query()  # Prepare mutation query
        # self.upd_df.apply(self.update_list_metadata, axis=1)
        self.update_list_metadata()
        self.coll_df["upd_status_code"] = self.coll_df.apply(
            lambda row: self.update_collectory_dr(row, self.collectory_url), axis=1
        )

        print(f"\n All lists and collectory dataresources updated")


if __name__ == "__main__":
    Update_flag = Update_flag()
    Update_flag.run()
