class TransitSchedule:
    def __init__(self, stop_names_to_ids, stop_ids, applicable_trip_stop_list):
        self._stop_names_to_ids = stop_names_to_ids
        self._stop_ids = stop_ids
        self._applicable_trip_stop_list = applicable_trip_stop_list

    def get_applicable_trip_stop_list(self):
        return self._applicable_trip_stop_list
    
    def get_stop_ids(self):
        return self._stop_ids
    
    def get_stop_names_to_ids(self):
        return self._stop_names_to_ids