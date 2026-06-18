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
        # self.collectory_headers = None  # Uses API Key
        self.all_df = pd.DataFrame()
        self.upd_df = pd.DataFrame()
        # self.collectory_url = cfg.collectory_url
        # self.collectory_api_key = cfg.collectory_api_key
        self.list_url = cfg.list_url
        self.list_info_url = cfg.list_info_url
        self.graphql_url = cfg.graphql_url
        self.keys_to_keep = cfg.graphql_keys_to_keep

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
        # parser.add_argument("--colfile", required=True)
        # parser.add_argument("--list_metafile", required=True)
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
                # page += limit
                page += 1
            else:
                print(f"Error downloading: {url} Status: {response.status_code}")

        df = pd.DataFrame(all_data)
        print(f"List info download complete: {len(df)} records downloaded")
        return df

    def filter_lists(self, args):
        """ """
        ##Criteria for list selection for update
        # List must be `non-authoritative`, and meet the following criteria:

        #    1. Lists with zero records - rowCount
        #    2. Lists with only 1 record -rowCount
        #    3. Lists marked with list type – “Test%”
        #    4. Lists with list name contains "test%"
        #    4. Lists with list name contains "My Species list"
        # Note: BioCollect DRs to be excluded from update

        notauthdf = self.all_df.copy()
        notauthdf["rowCount"] = pd.to_numeric(notauthdf["rowCount"], errors="coerce")
        archivedf = notauthdf[
            (notauthdf["listType"].str.contains("test", case=False, na=False))
            | (notauthdf["title"].str.contains("test", case=False, na=False))
            | (notauthdf["title"].str.contains("My Species list", case=False, na=False))
            | (notauthdf["rowCount"] <= 1)
        ]
        archivedf.loc[:, "isPrivate"] = True
        # Capture record counts
        nonauthct = len(notauthdf)
        lt1rec = (notauthdf["rowCount"] <= 1).sum()
        typetest = (
            notauthdf["listType"].str.contains("test", case=False, na=False)
        ).sum()
        nametest = (notauthdf["title"].str.contains("test", case=False, na=False)).sum()
        namemyspec = (
            notauthdf["title"].str.contains("My Species list", case=False, na=False)
        ).sum()
        numbc = archivedf["dataResourceUid"].isin(cfg.drExclude).sum()
        bcfound = archivedf.loc[
            archivedf["dataResourceUid"].isin(cfg.drExclude), "dataResourceUid"
        ].unique()
        # Exclude BioCollect dataResources
        archivedf = archivedf[~archivedf["dataResourceUid"].isin(cfg.drExclude)]
        print("  ")
        print(f"Number non-authoritative lists: {nonauthct}")
        print(f"    - # Lists with less than 2 records: {lt1rec}")
        print(f"    - # List type value contains text test: {typetest}")
        print(f"    - # List name value contains text test: {nametest}")
        print(f"    - # List name value contains text My Species list: {namemyspec}")
        print(f"    - # Biocollect lists found: {numbc}")
        print(f"Number of lists to archive: {len(archivedf)}")
        print(f"Biocollect DRs found and excluded: {bcfound}")

        return archivedf


    class update_metadata:
        # Get metadata (using API for now)
        # Update list
        # Set isPrivate flag to True
        # Send the mutation using requests

        def __init__(self):
            self.rec_count = 0
            self.list_url = cfg.list_url
            self.list_info_url = cfg.list_info_url
            self.graphql_url = cfg.graphql_url
            self.keys_to_keep = cfg.graphql_keys_to_keep

        def get_list_metadata(self, druid):

            lUrl = self.list_url + druid
            headers = {"Content-Type": "application/json"}
            response = requests.get(lUrl, headers=headers)
            if response.status_code == 200:
                metadata = response.json()
                for key in list(
                    metadata.keys()
                ):  # remove key values not used in update
                    if key not in self.keys_to_keep:
                        metadata.pop(key)
            else:
                print(
                    f"List metadata request failed with status code {response.status_code}"
                )
            return metadata

        def update_list_metadata(self, row, mutation_query, list_headers):

            self.rec_count += 1
            druid = row["dataResourceUid"]
            print(f"Rec {self.rec_count}: updating {druid}")
            metadata = self.get_list_metadata(druid)
            metadata["isPrivate"] = True
            # metadata["isPrivate"] = False
            jsonStr = {
                "query": mutation_query,
                "operationName": "update",
                "variables": metadata,
            }
            response = requests.post(
                self.graphql_url,
                headers=list_headers,
                json=jsonStr,
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
        obj = self.update_metadata()

        args = self.parse_arguments()
        # Get access token - needs further testing
        # self.accessToken = lf.get_authentication_info(args=args, test=True)
        self.listaccessToken = "<hard code here if needed>"
        self.list_headers = {
            "Content-Type": "application/json",
            # "Authorization": "Bearer {}".format(self.accessToken["access_token"]),
            "Authorization": "Bearer {}".format(self.listaccessToken),
        }
        print("Update species lists `isPrivate` flag")
        print("List must be `non-authoritative`, and meet the following criteria:")
        print("      1. Lists with zero records")
        print("      2. Lists with only 1 record")
        print("      3. Lists marked with list type – “Test”")
        print('      4. Lists with list name contains "test"')
        print("      5. Exclude BioCollect lists")
        if args.getListInfo == "True":
            self.all_df = (
                self.download_list_info_ws()
            )  # get all non-authoritative, non-private lists
            self.upd_df = self.filter_lists(args)  # filter based on criteria
            # Write downloaded to CSV
            print("\nWrite lists to file:")
            self.all_df.to_csv(args.allfile, encoding="utf-8", index=False)
            self.upd_df.to_csv(args.updfile, encoding="utf-8", index=False)
            print(f" .... All lists written to: {args.allfile}")
            print(f" .... Lists to update written to: {args.updfile}")
        else:
            self.upd_df = pd.read_csv(args.updfile, encoding="utf-8", dtype="str")

        # Set up query for list metadata update via graphql
        print(f"\n Number of lists to update: {len(self.upd_df)}")
        print("    - Prepare mutation query")
        mutation_query = self.prepare_mutation_query()
        print("    - Updating lists")
        self.upd_df = self.upd_df.apply(
            obj.update_list_metadata,
            axis=1,
            args=(mutation_query, self.list_headers)
        )
        print(f"All lists and collectory dataresources updated successfully")


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
