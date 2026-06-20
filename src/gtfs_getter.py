from config import Config
import zipfile
import requests
import os


class GTFSGetter:
    # TODO: Add GTFS validation, skipping errors that we can
    # work with

    def __init__(self, config: Config):
        self.api_key = config.get_value("API_KEY")
        self.gtfs_url = config.get_value("GTFS_URL")
        self.api_key_header_name = config.get_value("API_KEY_HEADER")

    def _get_gtfs_zip(self, file_path):
        # Fetch the file content from the URL
        response = requests.get(self.gtfs_url, headers={self.api_key_header_name: self.api_key})

        # Save the content as a binary file locally
        with open(file_path, "wb") as file:
            file.write(response.content)

    def _unzip_gtfs_zip(self, file_path, folder_name):
        # Open the zip file in read mode
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            # Extract all contents into the specified directory
            zip_ref.extractall(folder_name)

    def _delete_gtfs_zip(self, file_path):
        os.remove(file_path)

    def get_gtfs_files(self, file_path, folder_name):
        self._get_gtfs_zip(file_path)
        self._unzip_gtfs_zip(file_path, folder_name)
        self._delete_gtfs_zip(file_path)

