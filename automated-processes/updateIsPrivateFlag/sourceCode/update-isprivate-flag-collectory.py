import argparse
import json
import logging
import time
from pathlib import Path

import pandas as pd
import requests
import upd_config as cfg

log: logging.log = logging.getLogger("isPrivate flag")
log.setLevel(logging.INFO)


class Update_flag:
    """
    Update_flag class to update collectory isPrivate flag on list.

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
        self.headers = None
        self.coll_df = pd.DataFrame()
        self.collectory_url = cfg.collectory_url
        self.collectory_api_key = cfg.collectory_api_key

    def parse_arguments(self):
        """
        Parse configuration parameters

        :return: Arguments

        """

        parser = argparse.ArgumentParser()
        parser.add_argument("--input", required=True)
        parser.add_argument("--output", required=True)
        parser.add_argument("--colfile", required=True)
        parser.add_argument("--env", required=True)
        args = parser.parse_args()

        self.input_path = Path(args.input)
        self.input_path.mkdir(parents=True, exist_ok=True)
        self.output_path = Path(args.output)
        self.output_path.mkdir(parents=True, exist_ok=True)

        return args

    def join_url(self, *url_fragments: str) -> str:
        """
        Joins multiple URL fragments into a single URL.

        :param url_fragments: URL fragments to be joined.
        :return: A single URL string.
        """
        return "/".join(fragment.strip("/") for fragment in url_fragments)

    def json_parse(
        self, base_url: str, url_path: str, params=None, headers=None, method="GET"
    ):
        """
        Calls the specified URL and returns the JSON response.
        :param base_url: like https://collections.ala.org.au/ws
        :param url_path: like /dataResource/dr000
        :param params: is a dictionary of parameters to be passed to the API
        :return: is the json response from the URL
        """
        dr = url_path.rsplit("/", 1)[-1]

        try:
            full_url = self.join_url(base_url, url_path)
            print(f"    {dr} - {full_url}")
            if method == "GET":
                with requests.get(
                    full_url, params, headers=headers, timeout=60
                ) as response:
                    response.raise_for_status()
                    json_result = json.loads(response.content)
                    return json_result
            elif method == "POST":
                with requests.post(
                    full_url, json=params, headers=headers, timeout=60
                ) as response:
                    response.raise_for_status()
                    return response.content
        except requests.exceptions.HTTPError as err:
            # logging.error(
            logging.error(
                "Error encountered during request %s with params %s",
                full_url,
                params,
                exc_info=err,
            )
            raise IOError(err)

    def update_registry_metadata(self, registry_base_url, uid, ala_api_key, metadata):
        """
        Updates metadata for a dataset in the registry (Collectory) using the API key.

        Args:
            registry_base_url (str): The base URL of the registry (Collectory).
            uid (str): The unique identifier of the dataset.
            ala_api_key (str): The API key for authentication.
            metadata (dict): The metadata to update.

        Returns:
            dict: The updated metadata of the dataset, or an error message if not found.
        """
        if uid.startswith("dr"):
            resource_path = f"dataResource/{uid}"
        elif uid.startswith("dp"):
            resource_path = f"dataProvider/{uid}"
        else:
            raise ValueError("Not a valid dataset or data provider uid: %s", uid)

        try:
            jresponse = self.json_parse(
                registry_base_url,
                resource_path,
                headers={"Authorization": ala_api_key},
                method="POST",
                params=metadata,
            )
            return jresponse
        except Exception as e:
            print(f"Error fetching metadata for {uid}: {str(e)}")

    def run(self):
        args = self.parse_arguments()
        colfile = Path(args.colfile)
        # List of DataResources in collectory to update
        coll_df = pd.read_csv(colfile, encoding="utf-8", dtype="str").fillna("")
        metadata = {"isPrivate": "true"}
        print(f"Updating {coll_df.shape[0]} collectory dataresources: ")
        response = coll_df.apply(
            lambda row: self.update_registry_metadata(
                self.collectory_url,
                row["dataResourceUid"],
                self.collectory_api_key,
                metadata,
            ),
            axis=1,
        )
        print(f"\n All collectory dataresources updated")


if __name__ == "__main__":
    start = time.perf_counter()
    Update_flag = Update_flag()
    Update_flag.run()
    elapsed = time.perf_counter() - start

    # Output Elapsed time information
    hours, rem = divmod(elapsed, 3600)
    minutes, seconds = divmod(rem, 60)

    print(
        f"\033[1mTime for Update Collectory isPrivate\n\033 flag script to run\033[0m"
    )
    print(
        f"    \033[1m[1mElapsed time\033[0m - {int(hours):02}{int(minutes):02}{seconds:06.3f}"
    )
    print(
        f"    \033[1mHH:\033[0m {int(hours):02}\n\033[1mMM:\033[0m {int(minutes):02}\n\033[1mSS:\033[0m {seconds:06.3f}"
    )
