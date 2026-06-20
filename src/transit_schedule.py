class TransitSchedule:
    def __init__(self, stop_names_to_ids, stop_ids, applicable_trip_service_ids):
        self.stop_names_to_ids = stop_names_to_ids
        self.stop_ids = stop_ids
        self.applicable_trip_service_ids = applicable_trip_service_ids