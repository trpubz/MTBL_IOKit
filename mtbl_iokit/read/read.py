"""
Read files and put in memory
"""
import csv
import os
import json
from enum import Enum

import pandas as pd

from mtbl_playerkit import Player


class IOKitDataTypes(Enum):
    DATAFRAME = "dataframe"
    PLAYER = "player"
    JSON = "json"
    CSV = "csv"
    STR = "str"


def read_in_as(
        directory: str,
        file_name: str,
        file_type: str = "json",
        as_type: IOKitDataTypes = IOKitDataTypes.PLAYER) -> any:
    """
    Read in data as specified by filename and return it as specified by as_type
    :param directory: location of file, relative or absolute path
    :param file_name: name of file
    :param file_type: file extension
    :param as_type: DataTypes enum; PLAYER -- mtbl_playerkit type, JSON, CSV
    :return: in-memory file IO for specified data type
    """
    full_path = os.path.join(directory, file_name + file_type)
    full_path = os.path.abspath(full_path)
    try:
        with open(full_path, "r") as blob:
            match file_type:
                case ".json":
                    # .load Expects a file-like object that supports text reading
                    structured_blob = json.load(blob)
                case ".csv":
                    structured_blob = csv.DictReader(blob)
                    # structured_blob_headers = next(structured_blob)
                    structured_blob = list(structured_blob)
                case ".html":
                    structured_blob = blob.read()

    except FileNotFoundError:
        raise FileNotFoundError(f"File not found at '{full_path}'")
    except OSError as e:
        print(f"Error opening '{full_path}': {e}")
        return None

    match as_type:
        case IOKitDataTypes.PLAYER:
            # return Player objects
            players = [Player.model_validate(p) for p in structured_blob]
            return players
        case IOKitDataTypes.DATAFRAME:
            # return a pandas dataframe
            return pd.DataFrame.from_dict(structured_blob, orient="columns")
        case _:
            # return the original data structure, e.g. json -> json
            return structured_blob
