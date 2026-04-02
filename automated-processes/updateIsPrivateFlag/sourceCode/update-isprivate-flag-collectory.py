import argparse
import json
import sys
from pathlib import Path

# import archive_functions as afn
import pandas as pd
import requests

# import .collectory as collectory
import upd_config as cfg

sys.path.append("../../")
import functions.list_functions as lfn

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
        self.coll_df = pd.DataFrame()
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
    
    # def __init__(self, token_url="", client_id="", client_secret="") -> None:
        #     if token_url:
        #         self.token_url = token_url
        #     if client_id:
        #         self.client_id = client_id
        #     if client_secret:
        #         self.client_secret = client_secret

    def get_collectory_access_token(self, scope: str) -> str:
        response = requests.post(
            self.token_url,
            data={"grant_type": "client_credentials", "scope": scope},
            auth=(self.client_id, self.client_secret),
        )
        if response.status_code == 200:
            response_text = response.json()
            if "access_token" in response_text:
                log.info(f"Access token is acquired successfully from {self.token_url}, client id {self.client_id} ")
                return response_text["access_token"]

        raise ValueError(f"Error in getting access token from {self.token_url}, client id {self.client_id} ")

    
    # def update_collectory_dr(self, uid: str) -> str:
    #     import ast

    #     """
    #     Update an entity with some data

    #     :param uid: The unique id of the entity being interrogated (eg dr1455)
    #     :param **kwargs: The data to update, as a set of key=value pairs
    #     """
    #     uid = "dr22810"
    #     vals = "{'isPrivate': True}"
    #     kwargs = ast.literal_eval(vals)
    #     kwargs = json.dumps(kwargs)
    #     url = f"{self.collectory_url}/{uid}.json"
    #     url = f"{self.collectory_url}/{uid}"
    #     print("POST %s to %s", str(kwargs), url)
    #     headers = {"Content-Type": "application/json"}
    #     if self.auth_headers is not None:
    #         headers = self.auth_headers
    #     with requests.post(url, json=kwargs, headers=headers) as response:
    #         if response.status_code != 200:
    #             response.raise_for_status()
    #         else:
    #             return response.text
            
    def update_collectory_metadata(self, row):
            print(f"Updating collectory metadata: {row['uid']}")

            # Update collectory metadata
            print(f"Updating collectory metadata: {row['uid']}")
            colUrl = self.collectory_url + row["uid"]
            # colUrl = self.collectory_url + 'dr22810'
            # crow = self.coll_df[self.coll_df["uid"] == row["uid"]]
            # row["isPrivate"] = "True"
            # row["isPrivate"] = "False"
            jstr = row.to_json()
            try:
                with requests.post(colUrl, json=jstr, headers=self.auth_collectory) as response:
                    if response.status_code == 200 or response.status_code == 201:
                        return str(response.status_code)
                    else:
                        response.raise_for_status()
            except Exception as e:
                print("Error in creating %s: %s for %s", colUrl, jstr, e)
                response.raise_for_status()

            print(f"Updated collectory isPrivate flag for list: {druid}")

            return ()
   
    def run(self):
        args = self.parse_arguments()
        self.colaccessToken = self.get_collectory_access_token(scope)
        self.auth_collectory = {
            "Content-Type": "application/json",
            # "Authorization": "Bearer {}".format(self.accessToken["access_token"]),
            "Authorization": "Bearer {}".format(self.colaccessToken),
        }
        self.coll_df = pd.read_csv(
            args.colfile, encoding="utf-8", dtype="str"
        ).fillna("")
        self.coll_df["upd_status_code"] = self.coll_df.apply(
            lambda row: self.update_collectory_metadata(row), axis=1
        )
        print(f"\n All lists and collectory dataresources updated")


if __name__ == "__main__":
    Update_flag = Update_flag()
    Update_flag.run()
