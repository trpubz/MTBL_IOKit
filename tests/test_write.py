import os
import tempfile
import json
import pytest
import pandas as pd

import write
from mtbl_playerkit import Player


class TestWrite:
    df = None
    full_path = ""

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        self.df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
        yield

    @pytest.fixture
    def temp_dir(self):
        with tempfile.TemporaryDirectory() as dir_path:
            yield dir_path

    def test_write_out_player_serialized(self, temp_dir):
        plyr1 = Player(name="Corbin Carrol", team="ARI")
        plyr2 = Player(name="Zac Gallen", team="ARI")

        # Use the temporary directory
        write.write_out([plyr1, plyr2], temp_dir, "player_data", ".json")

        # Verify file presence
        file_path = os.path.join(temp_dir, "player_data.json")
        assert os.path.exists(file_path)

        # Verify content (Pydantic serialization)
        with open(file_path, 'r') as f:
            data = json.load(f)
            assert len(data) == 2
            assert data[0]['name'] == "Corbin Carrol"

    def test_write_out_non_pydantic_model(self, temp_dir):
        csv = """
        name, team
        corbin carrol, ARI
        """

        write.write_out(csv, temp_dir, "player_data", ".csv")
        # Verify file presence
        file_path = os.path.join(temp_dir, "player_data.csv")
        assert os.path.exists(file_path)

    def test_export_dataframe_to_csv(self):
        write.export_dataframe(self.df, "test", ".csv", "./temp")
        self.full_path = "./temp/test.csv"

        assert os.path.exists(self.full_path)

    def test_export_dataframe_to_json(self):
        write.export_dataframe(self.df, "test", ".json", "./temp")
        self.full_path = "./temp/test.json"

        assert os.path.exists(self.full_path)

    def test_export_dataframe_to_json_without_schema(self):
        write.export_dataframe(self.df, "test", ".json", "./temp", schema=False)
        self.full_path = "./temp/test.json"

        assert os.path.exists(self.full_path)

    def test_export_dataframe_without_proper_file_type(self):
        write.export_dataframe(self.df, "test", "json", "./temp")
        self.full_path = "./temp/test.json"

        assert os.path.exists(self.full_path)
