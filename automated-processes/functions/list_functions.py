# Common functions for Authoritative Lists
#
import json
import ssl
import time
import urllib.request
import json
import io

import certifi
import pandas as pd
import requests

# from .vocab import upload_listsTest,ingest_listsTest,progress_listsTest
from bs4 import BeautifulSoup

from .vocab import (
    api_values,
    conservation_list_urls,
    conservation_lists,
    get_listsProd,
    get_listsTest,
    list_names_conservation_test,
    list_names_sensitive_test,
    sensitive_lists,
    token_url,
    urlSuffix,
    list_names_all_species_state_test,
    upload_listsTest,
    ingest_listsTest,
    progress_listsTest,
)


def download_ala_specieslist(url: str):
    """
    Download ALA species list.  Returns error if list isn't right, returns dataframe if list is correct
    """

    with urllib.request.urlopen(
        url, context=ssl.create_default_context(cafile=certifi.where())
    ) as url:
        if url.status == 200:
            data = json.loads(url.read().decode())
            data = pd.json_normalize(data)
        else:
            # Handle the error
            print("Error in download_ala_list:", url.status)
    return data


def kvp_to_columns(df):
    """
    All data is in the KVP for lists.  Make sure the KVP data is in a pandas dataframe by itself.
    """
    d0 = pd.DataFrame()
    for i in df.index:
        if len(df["kvpValues"][i]) > 0:
            kvpdf = pd.json_normalize(df.kvpValues[i])
            kvpdf = kvpdf.transpose()
            kvpdf.columns = kvpdf.loc["key"]  # rename columns to the keys
            kvpdf.drop(["key"], inplace=True)  # drop the keys row
            kvpdf["id"] = df.id[i]
            kvpdf = pd.merge(df, kvpdf, "inner", on="id")
            d0 = pd.concat([d0, kvpdf])
    return d0


def get_changelist(testdr: str, proddr: str, ltype: str):
    """
    Determines changes between current lists in production ("old") and the lists we uploaded
    to test ("new").  Returns a pandas dataframe with all the changes
    """

    # get old and new list urls
    oldListUrl = get_listsProd + proddr + urlSuffix
    newListUrl = get_listsTest.replace("{speciesListID}", testdr)

    # download old list and turn it into pandas dataframe
    oldList = download_ala_specieslist(oldListUrl)
    oldList = kvp_to_columns(oldList)
    oldList = oldList.add_suffix("_old")
    columns_to_strip = ["name_old", "scientificName_old"]
    oldList[columns_to_strip] = oldList[columns_to_strip].apply(lambda x: x.str.strip())
    oldList = oldList.fillna(
        value=""
    )  # fill all None values since it's the new default

    # download new list and turn it into pandas dataframe
    newList = pd.read_csv(newListUrl)
    newList = newList.add_suffix("_new")
    columns_to_strip = ["verbatimScientificName_new", "scientificName_new"]
    newList[columns_to_strip] = newList[columns_to_strip].apply(lambda x: x.str.strip())
    newList = newList.fillna(value="")

    # check for new  and old names - left join new to old, drop any columns in names_old if they are na
    # conservation lists keep track of changes
    newVsOld = pd.merge(  # was just scientificName
        newList,
        oldList,
        how="left",
        left_on=["verbatimScientificName_new"],
        right_on=["name_old"],
    )
    columns = ["verbatimScientificName_new", "scientificName_new"]
    if ltype == "C":
        columns = columns + ["sourceStatus_new"] # was status_new
    additions = newVsOld[newVsOld["name_old"].isna()][columns]
    if ltype == "C":
        additions["sourceStatus_old"] = "" # was status_old
    additions["listUpdate"] = "added"

    # removed names - left join old to new, drop na new
    oldVsNew = pd.merge(  # was just scientificName
        oldList,
        newList,
        how="left",
        left_on=["name_old"],
        right_on=["verbatimScientificName_new"],
    )

    # temp check before switching over
    if "verbatimScientificName_old" not in oldVsNew.columns:
        columns = ["name_old", "scientificName_old"]
    else:
        columns = ["verbatimScientificName_old", "scientificName_old"]

    # add status_old for conservation list
    if ltype == "C":
        columns = columns + ["status_old"]

    # add empty status
    removals = oldVsNew[oldVsNew["scientificName_new"].isna()][columns]
    if ltype == "C":
        removals["sourceStatus_new"] = "" # was status_new
    removals["listUpdate"] = "removed"

    # status changes - only check status changes for conservation list
    if ltype == "C":
        statusChanges = pd.merge(
            newList,
            oldList,
            how="inner",
            left_on=["scientificName_new", "vernacularName_new"],
            right_on=[
                "name_old",
                "vernacularName_old",
            ],  # will be scientificName_old eventually
        )
        statusChanges = statusChanges[
            statusChanges["sourceStatus_new"] != statusChanges["sourceStatus_old"] # status_new,status_old
        ][
            [
                "scientificName_new",
                "vernacularName_new",
                "sourceStatus_new", # status_new
                "sourceStatus_old", # status_old
            ]
        ]
        statusChanges["listUpdate"] = "status change"

    # union and display in alphabetical order and save locally
    additions = additions.rename(
        columns={
            "verbatimScientificName_new": "verbatimScientificName",
            "scientificName_new": "scientificName",
        }
    )

    if "verbatimScientificName_old" in removals.columns:
        removals = removals.rename(
            columns={
                "verbatimScientificName_old": "verbatimScientificName",
                "scientificName_old": "scientificName",
            }
        )
    else:
        removals = removals.rename(
            columns={
                "name_old": "verbatimScientificName",
                "scientificName_old": "scientificName",
            }
        )

    if ltype == "C":
        changeList = pd.concat([additions, removals, statusChanges])
    else:
        changeList = pd.concat([additions, removals])

    # return changelist
    changeList = changeList.sort_values("scientificName", ascending=True)
    return changeList


def read_list_url(url=None, state=None):
    """
    Determine what type of parsing is needed for each URL
    """

    if ".xls" in url.lower() or ".xlsx" in url.lower():
        # check for skipping lines for the NT
        if state == "NT":
            xls = pd.ExcelFile(url)  # ,skiprows = [0,1,2,3])
            sheet_names = xls.sheet_names[:-1]
            df = pd.DataFrame()
            for name in sheet_names:
                df = pd.concat(
                    [df, pd.read_excel(xls, sheet_name=name, skiprows=[0, 1, 2, 3])]
                )
            if "Fauna" in url:
                df = df[
                    [
                        "FAMILY",
                        "GENUS",
                        "SPECIES",
                        "COMMON NAME",
                        "TERRITORY PARKS AND WILDLIFE ACT CLASSIFICATION",
                    ]
                ]  # 'INTRODUCED STATUS'
                df["scientificName"] = df["SPECIES"].copy()
            else:
                df = df.rename(columns={"TAXON NAME": "scientificName"})
                df = df[
                    [
                        "FAMILY",
                        "GENUS",
                        "SPECIES",
                        "scientificName",
                        "COMMON NAME",
                        "TERRITORY PARKS AND WILDLIFE ACT CLASSIFICATION",
                    ]
                ]  # 'INTRODUCED STATUS'
        else:
            xls = pd.ExcelFile(url)  # ,engine='openpyxl')
            if state == "TAS":
                df = pd.read_excel(xls)  # ,sheet_name=xls.sheet_names[0])
            else:
                raise ValueError(
                    "{} not taken into account:\n\n{}\n".format(state, url)
                )
    elif ".csv" in url:
        # if state == "WA":
        #     df = pd.read_csv(url,dtype=str) # dtype=str
        #     df = format_statuses_WA(df=df)
        # else:
        df = pd.read_csv(url)
    elif any(x in url for x in ["json", "/api/"]):
        # this is for ACT and QLD
        response = requests.get(url)
        response_json = response.json()
        df = pd.DataFrame.from_records(
            response_json, index=[i for i in range(len(response_json))]
        )
    elif "https" in url:
        return webscrape_list_url(url=url, state=state)
    else:
        response = requests.get(url)
        response_json = response.json()
        df = pd.DataFrame(response_json[api_values[state]])

    return df


def get_conservation_codes(state=None):
    """
    Gets conservation codes for relevant states
    """

    if state is None:
        raise ValueError("Please provide a state for specific conservation codes.")

    if state == "NT":

        # get codes, rename and drop anything with NaNs
        xls = pd.ExcelFile(conservation_list_urls[state][0])
        codes = pd.read_excel(
            xls, sheet_name="CLASSIFICATION", skiprows=[x for x in range(13)]
        )
        codes = codes.rename(columns={"Unnamed: 0": "Code"})
        codes = codes.dropna(how="any")

        # remove spaces from Code
        codes["Code"] = codes["Code"].str.replace(" ", "")
        codes["Categories for classification"] = list(
            map(
                lambda x: x.split(" - ")[0] if "-" in x else x,
                codes["Categories for classification"],
            )
        )
        return codes

    elif state == "QLD":

        # get codes form here and turn it into a dataframe
        response = requests.get(
            "https://wildnet-pub.science-data.qld.gov.au/api/v1/status-types"
        )
        all_codes = pd.DataFrame(response.json())

        # only select Queensland codes and Legislation codes
        temp = all_codes[all_codes["stat_ext_code"] == "QLD"]
        qld_codes = temp[temp["stat_cat_code"] == "LEG"]

        # return Queensland codes
        return qld_codes

    elif state == "WA":

        # get the data from the url
        response = requests.get(conservation_list_urls[state][0])

        # parse the html to get the spreadsheets
        soup = BeautifulSoup(response.text, "html.parser")
        strings = list(soup.find_all("a"))
        flora_urls = list(
            set([str(s) for s in strings if "Threatened and Priority Flora" in str(s)])
        )  # .xls
        flora_url = flora_urls[0].split('"')[1]
        flora_excel_data = requests.get(flora_url)
        flora_excel = pd.ExcelFile(io.BytesIO(flora_excel_data.content))
        df = pd.read_excel(
            flora_excel,
            sheet_name=flora_excel.sheet_names.index("Conservation Codes"),
            skiprows=[1, 2, 3, 4, 5, 6, 7, 8, 9],
        )[["Unnamed: 1", "Unnamed: 2"]]
        df = df[~df["Unnamed: 2"].isna()]
        return df.rename(
            columns={"Unnamed: 1": "Code", "Unnamed: 2": "Category"}
        ).reset_index(drop=True)

    else:

        return None


def format_statuses_WA(df=None):

    # remove all empty statuses
    df = df[~df["conscodelist"].isna()].reset_index(drop=True)

    # initialise sourceStatus column
    df["sourceStatus"] = ""

    # loop over all rows (change this to function and df.apply)
    for i, row in df.iterrows():
        statuses = row["conscodelist"].strip("[]").replace("'", '"')
        if len(statuses.split("}, {")) > 1:
            temp = statuses.split(", ")
            first_status = ", ".join([temp[0], temp[1]])
            second_status = ", ".join([temp[2], temp[3]])
            first_status = json.loads(first_status)
            second_status = json.loads(second_status)
            print(f"first: {first_status}\tsecond: {second_status}")
            if first_status["conscode"] != second_status["conscode"]:
                if (
                    first_status["authority"] == "State"
                    and second_status["authority"] != "State"
                ):
                    df.at[i, "sourceStatus"] = first_status["conscode"]
                elif (
                    first_status["authority"] != "State"
                    and second_status["authority"] == "State"
                ):
                    df.at[i, "sourceStatus"] = second_status["conscode"]
                else:
                    df.at[i, "sourceStatus"] = " & ".join(
                        [first_status["conscode"], second_status["conscode"]]
                    )
            else:
                df.at[i, "sourceStatus"] = first_status["conscode"]
        else:
            json_statuses = json.loads(statuses)
            df.at[i, "sourceStatus"] = json_statuses["conscode"]

    # get all statuses that species inherit from the parent
    inherited_from_parent = df[df["sourceStatus"] == "Cons code inherited from parent"]
    for i, row in inherited_from_parent.iterrows():

        # get name to search by
        canonical_name_array = row["canonical_name"].split(" ")
        canonical_name_species = " ".join(canonical_name_array[:-1])

        # get parent and replace status
        parent = df[df["canonical_name"] == canonical_name_species]
        if not parent.empty:
            parent_index = parent.index[0]
            if parent.shape[0] > 1:
                print("yes, need to figure this out")
                print(parent)
                import sys

                sys.exit()
            else:
                df.at[i, "sourceStatus"] = parent["sourceStatus"][parent_index]
        else:
            print(f"could not find {canonical_name_species}")

    print(list(set(df["sourceStatus"])))
    print()
    import sys

    sys.exit()


def webscrape_list_url(url=None, state=None):
    """
    Webscrape for new list files for certain states
    """

    if state == "EPBC":
        # get the data from the url
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        strings = list(soup.stripped_strings)
        test = list(set([s for s in strings if ".csv" in s]))
        if len(test) > 1:
            raise ValueError(
                "There are more than one list - check that you have the correct one"
            )
        else:
            return pd.read_csv(test[0])

    elif state == "WA":

        # get the data from the url
        response = requests.get(url)

        # parse the html to get the spreadsheets
        soup = BeautifulSoup(response.text, "html.parser")
        strings = list(soup.find_all("a"))

        # initialise WA dataframe
        df_wa = pd.DataFrame()

        #####################
        # process flora list
        #####################

        # get the urls and excel data
        flora_urls = list(
            set([str(s) for s in strings if "Threatened and Priority Flora" in str(s)])
        )  # .xls
        flora_url = flora_urls[0].split('"')[1]
        flora_excel_data = requests.get(flora_url)
        flora_excel = pd.ExcelFile(io.BytesIO(flora_excel_data.content))

        # read two sheets in the Excel file
        temp_flora_df = pd.read_excel(
            flora_excel, sheet_name=flora_excel.sheet_names[0], skiprows=[0, 1]
        )[["Taxon", "Family", "WA Rank"]]
        temp1_flora_df = pd.read_excel(
            flora_excel, sheet_name=flora_excel.sheet_names[1], skiprows=[0, 1]
        )[["Taxon", "Family", "WA Status"]]

        # rename columns and add empty columns
        temp1_flora_df = temp1_flora_df.rename(columns={"WA Status": "WA Rank"})
        flora = pd.concat([temp_flora_df, temp1_flora_df])
        flora["status"] = flora["WA Rank"].copy()
        flora["vernacularName"] = ""
        flora = flora.rename(
            columns={
                "Family": "family",
                "WA Rank": "sourceStatus",
                "Taxon": "scientificName",
            }
        )

        # concatenate all flora to the overall dataframe
        df_wa = pd.concat([df_wa, flora])

        #####################
        # process fauna list
        #####################

        # get the urls and excel data
        fauna_urls = list(
            set([str(s) for s in strings if "Threatened and Priority Fauna" in str(s)])
        )  # .xls
        fauna_url = fauna_urls[0].split('"')[1]
        fauna_excel_data = requests.get(fauna_url)
        fauna_excel = pd.ExcelFile(io.BytesIO(fauna_excel_data.content))

        # read data from the Excel file
        fauna_df = pd.read_excel(fauna_excel, sheet_name=fauna_excel.sheet_names[0])

        # rename columns and add empty columns
        fauna_df["family"] = ""
        fauna_df["status"] = fauna_df["WA listing"].copy()
        fauna_df = fauna_df.rename(
            columns={"WA listing": "sourceStatus", "Scientific name": "scientificName"}
        )

        # concatenate all flora to the overall dataframe
        df_wa = pd.concat([df_wa, fauna_df]).reset_index(drop=True)

        # get codes and ensure correct codes are in place
        codes = get_conservation_codes(state=state)
        codes = codes.replace({"Code": {1: "P1", 2: "P2", 3: "P3", 4: "P4"}})

        # replace numbers with correct codes
        df_wa = df_wa.replace({"status": {1: "P1", 2: "P2", 3: "P3", 4: "P4"}})

        # return dataframe
        return df_wa[
            [
                "scientificName",
                "vernacularName",
                "family",
                "status",
                "sourceStatus",
            ]
        ]

    elif state == "NSW":

        # initialise data, then go through all the links to get all the data
        all_data = pd.DataFrame()
        another_url = True
        while another_url:
            data = requests.get(url).json()
            all_data = pd.concat(
                [all_data, pd.json_normalize(data, record_path=["value"])]
            )
            if "@odata.nextLink" not in data.keys():
                another_url = False
            else:
                url = data["@odata.nextLink"]

        return all_data

    elif state == "VIC":

        return pd.read_csv(url)  # data, sep=",")

    elif state == "SA":

        # get the data from the url
        response = requests.get(url)

        # parse the html to get the spreadsheets
        soup = BeautifulSoup(response.text, "html.parser")
        strings = list(soup.find_all("a"))
        urls = list(set([str(s) for s in strings if ".xls" in str(s)]))

        for url in urls:
            xls = pd.ExcelFile(url.split('"')[1])
            # second sheet name is titled 'Taxonomic List DEC 25'
            return pd.read_excel(xls, sheet_name=xls.sheet_names[1], skiprows=[0, 1])

    else:

        # need to write a new loop
        print("do separate webscrape function for {} for now".format(state))
        import sys

        sys.exit()


def format_data_for_post(list_data=None, state=None, list_type=None):
    """
    Turn a pandas dataframe into a dictionary for posting to the lists test environment
    """
    # Check which type of list is being passed and create the post_data dict accordingly
    if list_type == "C":
        post_data = {
            "listName": list_names_conservation_test[state],
            "listType": "TEST",
            "listItems": [None for i in range(list_data.shape[0])],
        }
    elif list_type == "S":
        post_data = {
            "listName": list_names_sensitive_test[state],
            "listType": "TEST",
            "listItems": [None for i in range(list_data.shape[0])],
        }
    elif list_type == "ALL":
        post_data = {
            "listName": list_names_all_species_state_test[state],
            "listType": "TEST",
            "listItems": [None for i in range(list_data.shape[0])],
        }
    else:
        raise ValueError(
            "Only two values are needed: 'C' for Conservation, 'S' for Sensitive"
        )

    # get all values needed for posting
    columns = list(list_data.columns)
    columns.remove("scientificName")

    # loop over each row to generate kvp values
    for i, row in list_data.iterrows():
        post_data["listItems"][i] = {"itemName": row["scientificName"], "kvpValues": []}
        for x in columns:
            post_data["listItems"][i]["kvpValues"].append({"key": x, "value": row[x]})

    # return data
    return post_data


def post_list_to_test(
    list_data=None, druid=None, state=None, list_type=None, args=None, filename=None
):
    """
    Posts formatted data to test with authentication checks
    """

    # format your data for posting to test
    auth = get_authentication_info(args=args, test=True)
    # """

    # format headers
    headers = {  #'X-ALA-userId': auth['profile']['email'],
        "Authorization": "Bearer {}".format(auth["access_token"]),
        "Accept": "application/json",
        "user-agent": "authoritative-lists/1.0.0",
    }

    # create a binary string and data for file upload
    with open("data/temp-new-lists/{}".format(filename), "rb") as f:
        files = {"file": (filename, f.read(), "text/csv")}

        data = {"description": "CSV data upload", "format": "csv"}

    # first, upload the list
    try:
        response_upload = requests.post(
            upload_listsTest, data=data, files=files, headers=headers
        )
    except requests.exceptions.RequestException as e:
        print(e)
    finally:
        if response_upload.status_code != 200:
            print("There was an error uploading the csv file.")
            print(response_upload)
            print(response_upload.text)

    # second, trigger an ingestion of a list
    upload_filename = response_upload.json()["localFile"]
    try:
        response_ingest = requests.post(
            "{}{}?file={}".format(ingest_listsTest, druid, upload_filename),
            headers=headers,
        )
    except requests.exceptions.RequestException as e:
        print(e)
    finally:
        if response_ingest.status_code != 200 and response_ingest.status_code != 201:
            print("There was an error uploading the csv file.")
            print(response_ingest)
            print(response_ingest.text)

    # check progress of ingest; exit when done
    id = response_ingest.json()["id"]
    response_test = requests.get(
        progress_listsTest.replace("{speciesListID}", id), headers=headers
    )
    if response_test.status_code != 200 and response_test.status_code != 201:
        raise ValueError(
            "There was an error posting the data.  Error code {}: {}".format(
                response_test.status_code, response_test.text
            )
        )
    completed = response_test.json()["completed"]
    while not completed:
        time.sleep(15)
        response_test = requests.get(
            progress_listsTest.replace("{speciesListID}", id), headers=headers
        )
        completed = response_test.json()["completed"]
    if response_test.status_code != 200 and response_test.status_code != 201:
        raise ValueError(
            "There was an error posting the data.  Error code {}: {}".format(
                response_test.status_code, response_test.text
            )
        )
    return None


def get_authentication_info(args=None, test=False, prod=False):

    # get authentication for server
    auth = read_authentication(args=args, test=test, prod=prod)

    # get client ID and secret ID
    client_id, client_secret = get_client_id_secret(args=args)

    # check if access token is expired
    test = is_access_token_expired(expires_at=auth["expires_at"])

    # if it is expired, run the following loop
    if test is not None:
        if test:

            # refresh tokens
            new_access_token, new_expires_in = refresh_access_token(
                refresh_token=auth["refresh_token"],
                client_id=client_id,
                client_secret=client_secret,
            )
            auth["access_token"] = new_access_token
            auth["expires_at"] = time.time() + new_expires_in

            # Serializing json
            auth_json = json.dumps(auth, indent=4)

            # Writing to sample.json
            if test:
                with open(args.authentication_test, "w") as out_file:
                    out_file.write(auth_json)
                out_file.close()
            if prod:
                with open(args.authentication_test, "w") as out_file:
                    out_file.write(auth_json)
                out_file.close()

    return auth


def read_authentication(args=None, test=False, prod=False):
    """
    Get relevant authentication information from json downloaded from website
    """
    if test:
        with open(args.authentication_test) as f:
            return json.load(f)
    if prod:
        with open(args.authentication_test) as f:
            return json.load(f)
    return None


def get_client_id_secret(args=None):
    """
    Get client ids and secret for posting data
    """

    f = open(args.client_ids)
    for line in f:
        if "client_id" in line:
            client_id = line.strip().split(" = ")[1]
        if "client_secret" in line:
            client_secret = line.strip().split(" = ")[1]

    return client_id, client_secret


def is_access_token_expired(expires_at=None):
    """
    Check if your JWT token is expired
    """
    return expires_at is None or time.time() > expires_at


def refresh_access_token(refresh_token=None, client_id=None, client_secret=None):
    """
    If the JWT token needs to be refreshed, this function refreshes the access token
    """

    # set up payload
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret,
    }

    # get response
    response = requests.post(
        token_url, data=data, headers={"Accept": "application/json"}
    )

    # set new tokens in json
    if response.status_code == 200:
        auth_response = response.json()
        new_access_token = auth_response["access_token"]
        new_expires_in = auth_response["expires_in"]
        return new_access_token, new_expires_in
    else:
        print(response.status_code)
        print(response.text)
        raise ValueError(
            "It is likely you need to manually regenerate JWT token - try this"
        )


def get_s3_information(args=None):

    # initialise dict
    s3_info = {}

    # open file containing s3 bucket information
    f = open(args.s3_info)

    # get all values
    for line in f:
        key, value = line.strip().split(" = ")
        s3_info[key] = value

    return s3_info


def add_change_delete_list_values(list_type=None, list_data=None, state=None):

    if list_data is None:
        raise ValueError("Please provide a list for checking.")

    if list_type is None or list_type not in ["Sensitive", "Conservation"]:
        raise ValueError(
            "Only Sensitive and Conservation are accepted for list_type values"
        )

    if state is None:
        raise ValueError("Please provide a state.")

    # read in additions, changes, deletions
    for dir in ["Changes", "Additions", "Deletions"]:
        df = pd.read_csv("{}/{}-{}-{}.csv".format(dir, state, list_type, dir))
        df = df.fillna("")
        if not df.empty:
            if dir == "Additions":
                list_data = pd.concat([list_data, df]).reset_index(drop=True)
            elif dir == "Changes":
                df = df.set_index("verbatimScientificName")
                for name, row in df.iterrows():
                    if name in list(list_data["verbatimScientificName"]):
                        index = list_data.loc[
                            list_data["verbatimScientificName"] == name
                        ].index[0]
                        list_data.at[index, row["field"]] = row["value"]
            else:
                for i, row in df.iterrows():
                    index = list_data.loc[
                        list_data["verbatimScientificName"]
                        == row["verbatimScientificName"]
                    ].index[0]
                    list_data.drop(index)

    return list_data


def set_bool_argument(arg=None, name_arg=None):
    # set boolean dict for more efficient variable setting
    boolean_dict = {"True": True, "False": False}

    if isinstance(arg, str):
        return boolean_dict[arg]
    elif isinstance(arg, bool):
        return arg
    else:
        raise ValueError(
            "Only True/False or boolean values are accepted for {}".format(name_arg)
        )


def set_lists_to_run(lists=None, C=False, S=False):
    if lists != "all" and lists != "None":
        temp_list = lists.split(",")
        for i, t in enumerate(temp_list):
            if "_" in t:
                temp_list[i] = t.replace("_", " ")
        return temp_list
    elif lists == "None":
        return []
    else:
        if C:
            return conservation_lists
        if S:
            return sensitive_lists
