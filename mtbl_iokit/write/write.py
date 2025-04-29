"""
Write out data to file + export dataframes
"""
import os
import json
import pandas as pd

from mtbl_playerkit import Player


def write_out(data: any, directory: str, file_name: str, ext: str):
    """
    Write files + create directories if not yet present
    :param data: any type of data to write
    :param directory: str directory to write to
    :param file_name: str name of file to write
    :param ext: str extension of file to write
    :return: None
    """
    # w+: Opens a file for both writing and reading. Overwrites the existing file if the file exists
    # If the file does not exist, creates a new file for reading and writing.
    with open(os.path.join(directory, (file_name + ext)), mode='w+', encoding='utf-8') as f:
        try:
            if isinstance(data[0], Player):
                # Pydantic's 'dict()' method for each object
                serialized = [x.model_dump() for x in data]
                json.dump(serialized, f, indent=2)
                return

        except KeyError:
            pass

        f.write(data)
        f.close()


def export_dataframe(
        df,
        filename,
        file_type,
        directory="/Users/Shared/BaseballHQ/resources/extract/",
        **kwargs):
    """
    Export dataframe to specified file type/location;
    storage to raw files -- either after or before transformations.
    :param df: pandas dataframe object
    :param filename: desired file name
    :param file_type: desired file type [should come in with '.' dot]; typically .csv or .json
    :param directory: ETL data directory
    :param kwargs: json file schema options; e.g. {schema: True, index: False}
    :return: None
    """
    # check to make sure the directory exists; if not, create it
    os.makedirs(directory, exist_ok=True)
    # check to make sure file_type has a '.' dot
    if not file_type.startswith("."):
        file_type = "." + file_type

    full_path = os.path.join(directory, filename + file_type)

    match file_type:
        case ".csv":
            export_to_csv(df, full_path, kwargs.get("index", False))
        case ".json":
            export_to_json(df, full_path, kwargs.get("index", False), kwargs.get("schema", True))


def export_to_csv(df: pd.DataFrame, full_path, index=False):
    """
    Export dataframe to csv file
    :param df: pandas dataframe object
    :param full_path: location and filename
    :param index: dataframe index option
    :return: None
    """
    df.to_csv(full_path, index=index)


def export_to_json(df: pd.DataFrame, full_path, index=False, with_schema=True):
    """
    Export dataframe to json file
    :param df: pandas dataframe object
    :param full_path: file location and filename
    :param index: pandas dataframe index option
    :param with_schema: pandas dataframe schema option
    :return: None
    """
    # orienting on table adds schema information to the json file
    if with_schema:
        df.to_json(full_path, index=index, orient="table", indent=2)
    else:
        df.to_json(full_path, index=index, orient="records", indent=2)
    # print("JSON file created successfully...")
