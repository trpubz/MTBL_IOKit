import os
import tempfile
import json
import pytest
import pandas as pd

from mtbl_iokit import read, write
from mtbl_playerkit import Player


class TestRead:
    df = None
    players = []
    temp_dir = None

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        plyr1 = Player(name="Corbin Carrol", team="ARI")
        plyr2 = Player(name="Zac Gallen", team="ARI")
        self.players = [plyr1, plyr2]
        csv = "name,team\r\n" + \
              "corbin carrol,ARI\r\n" + \
              "zac gallen,ARI\r\n"

        with tempfile.TemporaryDirectory() as dir_path:
            write.write_out([plyr1, plyr2], dir_path, "player_data", ".json")
            write.write_out(csv, dir_path, "player_data", ".csv")
            self.temp_dir = dir_path
            yield

    def test_read_in_json_as_player(self):
        data = read.read_in_as(self.temp_dir, "player_data", ".json", read.IOKitDataTypes.PLAYER)
        assert len(data) == 2
        assert isinstance(data[0], Player)

    def test_read_in_csv_as_player(self):
        data = read.read_in_as(self.temp_dir, "player_data", ".csv", read.IOKitDataTypes.PLAYER)
        assert len(data) == 2
        assert isinstance(data[0], Player)

    def test_read_in_json_as_dataframe(self):
        data = read.read_in_as(self.temp_dir, "player_data", ".json", read.IOKitDataTypes.DATAFRAME)
        assert len(data) == 2
        assert data.shape == (2, 2)

    def test_read_in_csv_as_dataframe(self):
        data = read.read_in_as("./tests/fixtures", "bats_savant", ".csv",
                               read.IOKitDataTypes.DATAFRAME)
        assert isinstance(data.iloc[0]["player_id"], str)

    def test_read_in_and_return_data(self):
        data = read.read_in_as(self.temp_dir, "player_data", ".json", read.IOKitDataTypes.JSON)
        assert len(data) == 2
        assert isinstance(data[0], dict)

    def test_read_in_html_as_string(self):
        fixture_dir = "tests/fixtures"
        file = "temp_espn_player_universe"
        ext = ".html"
        data = read.read_in_as(fixture_dir, file, ext, read.IOKitDataTypes.STR)
        assert len(data) > 0
        assert isinstance(data, str)

    def test_bad_file_path(self):
        with pytest.raises(FileNotFoundError):
            read.read_in_as("/path/to/file", "test", ".json", read.IOKitDataTypes.JSON)

    @pytest.fixture
    def mock_open(self, monkeypatch):
        def mock_open_fn(*args, **kwargs):
            raise OSError("Simulated OSError for testing")

        monkeypatch.setattr("builtins.open", mock_open_fn)

    def test_os_error(self, mock_open):
        result = read.read_in_as("/path", "some_file.txt")

        # Assert that the function returns None as expected
        assert result is None
