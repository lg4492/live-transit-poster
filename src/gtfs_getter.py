from config import Config
from gtfs_canonical_validator import CanonicalValidator
import requests


class GTFSGetter:
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


    def _validate_gtfs_zip(self, file_path):
        canonical_validator = CanonicalValidator(zip_file=file_path)

        report = canonical_validator.validate()
        print(report)

    def download_and_validate_gtfs(self, file_path):
        self._get_gtfs_zip(file_path)
        self._validate_gtfs_zip(file_path)


