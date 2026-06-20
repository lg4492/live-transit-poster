from google.transit import gtfs_realtime_pb2
from config import Config
import requests


class GTFSRGetter:
    def __init__(self, config: Config):
        self.api_key = config.get_value("API_KEY")
        self.gtfsr_url = config.get_value("GTFSR_URL")
        self.api_key_header_name = config.get_value("API_KEY_HEADER")

    def get_trip_updates(self):
        trip_updated_entities = []

        feed = gtfs_realtime_pb2.FeedMessage()
        response = requests.get(self.gtfsr_url, headers={self.api_key_header_name: self.api_key})
        feed.ParseFromString(response.content)
        for entity in feed.entity:
            if entity.HasField('trip_update'):
                trip_updated_entities.append(entity)
        
        return trip_updated_entities
