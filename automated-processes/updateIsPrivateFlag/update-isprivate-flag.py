import sys
import urllib.request

sys.path.append("../")
import argparse
import json

# import shlex
from pathlib import Path

import functions.list_functions as lf
import pandas as pd
import requests
from functions.ingest_lists import ingest_lists
from functions.vocab import get_listsProd, get_listsTest


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
        self.list_file = None

    def parse_arguments(self):
        """
        Parse configuration parameters

        :return: Arguments

        """

        parser = argparse.ArgumentParser()
        parser.add_argument("--input", required=True)
        parser.add_argument("--output", required=True)
        parser.add_argument("--infile", required=True)
        parser.add_argument("--env", required=True)
        parser.add_argument("--client_ids", required=True)
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

    def get_metadata(self, druid):
        # need to do this via API
        # token = "Bearer " + self.accessToken["access_token"]
        headers1 = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.accessToken["access_token"]),
        }
        lUrl = (
            f"https://lists-ws.test.ala.org.au/v2/speciesList/{druid}"  # 200
            # "https://lists-ws.test.ala.org.au/v2/speciesList/68b694704bfbd22e5d7e1643" # 200
            # "https://lists-develop.dev.ala.org.au/list/68bf92db938493273171ce8d" # 200
            # "https://lists-develop-ws.dev.ala.org.au/v2/speciesList/dr13397"       # 403
            # "https://lists-develop-ws.dev.ala.org.au/v2/speciesList/dr22808"  # 403
        )
        response = requests.get(
            lUrl,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.accessToken["access_token"]),
            },
        )

        # Check if the request was successful
        if response.status_code == 200:
            metadata = response.json()
            # data = pd.json_normalize(data)  # If the response is JSON
            print(metadata)
        else:
            print(f"Request failed with status code {response.status_code}")
        return metadata

    # def update_list_metadata(self, row):
    def update_list_metadata(self):
        # Get metadata (using API for now)
        # Update list
        self.metadata = self.get_metadata("dr22808")
        # Change the isPrivate flag
        self.metadata["isPrivate"] = True
        # Send the mutation using requests
        response = requests.post(
            self.graphql_url,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.accessToken["access_token"]),
            },
            json={
                "query": self.mutation_query,
                "operationName": "update",
                "variables": self.metadata,
            },
        )

        print("Status:", response.status_code)
        print("Response:", response.json())
        print(json.dumps(response.json(), indent=2))

        data = response.json()
        if "errors" in data:
            raise Exception("GraphQL query error: " + str(data["errors"]))
        print(f"Updated is Private flag for xx")

    def run(self):
        args = self.parse_arguments()
        inputFile = Path(args.infile)
        # Read file of lists to update
        # drList_df = pd.read_csv(inputFile, encoding="utf-8", dtype="str")
        self.graphql_url = (
            "https://lists-ws.test.ala.org.au/graphql"  # Set URL for list update
        )
        # Get access token
        # self.accessToken = self.get_access_token()
        self.accessToken = lf.get_authentication_info(args=args, test=True)
        # Prepare the mutation query
        self.mutation_query = self.prepare_mutation_query()
        self.update_list_metadata()
        # For each list in file
        # drList_df["retcode"] = drList_df.apply(self.update_list_metadata, axis=1)

        print(f"\n Start processing")


if __name__ == "__main__":
    Update_flag = Update_flag()
    Update_flag.run()
