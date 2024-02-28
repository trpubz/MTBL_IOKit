"""
Modify files
"""
import glob
import os


def rename_file(download_dir: str, downloaded_file: str, new_file_name: str, file_ext: str):
    # get all the .csv files in the download directory
    files = glob.glob(download_dir + "/*" + file_ext)

    for file in files:
        # get the file name without the directory
        file_name = file.rsplit("/", 1)[1]

        if file_name.__eq__(downloaded_file + file_ext):
            # remove old files
            for removable in files:
                if removable.__contains__(new_file_name + file_ext):
                    os.remove(removable)
                    break

            new_download_path = os.path.join(download_dir, new_file_name + file_ext)
            os.rename(file, new_download_path)

            return
