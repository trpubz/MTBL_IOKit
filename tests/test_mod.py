import tempfile
import os
import pytest

from mtbl_iokit import mod


class TestMod:
    @pytest.fixture
    def test_setup(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            yield temp_dir, "original_name", "new_name"

    def test_file_rename(self, test_setup):
        download_dir, original_file, new_file = test_setup

        # Create a dummy file in the temporary directory
        with open(os.path.join(download_dir, original_file + ".csv"), "w") as f:
            f.write("Sample Content")

        mod.rename_file(download_dir, original_file, new_file, ".csv")

        # Assertions
        assert not os.path.exists(os.path.join(download_dir, original_file + ".csv"))
        assert os.path.exists(os.path.join(download_dir, new_file + ".csv"))

    def test_file_name_with_removal_of_old_file(self, test_setup):
        download_dir, original_file, new_file = test_setup

        # Create a dummy file in the temporary directory
        with open(os.path.join(download_dir, original_file + ".csv"), "w") as f:
            f.write("Sample Content")

        # simulate old file still there
        with open(os.path.join(download_dir, new_file + ".csv"), "w") as f:
            f.write("Sample Content")

        assert os.path.exists(os.path.join(download_dir, new_file + ".csv"))

        mod.rename_file(download_dir, original_file, new_file, ".csv")

        # Assertions
        assert not os.path.exists(os.path.join(download_dir, original_file + ".csv"))
        assert os.path.exists(os.path.join(download_dir, new_file + ".csv"))