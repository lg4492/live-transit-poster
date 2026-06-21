class TransitSchedule:
    def __init__(self, stop_names_to_ids, top_level_stop_ids, lower_level_stop_ids, applicable_trip_stop_list):
        self._stop_names_to_ids = stop_names_to_ids
        self._top_level_stop_ids = top_level_stop_ids
        self._lower_level_stop_ids = lower_level_stop_ids
        self._applicable_trip_stop_list = applicable_trip_stop_list

    def get_applicable_trip_stop_list(self):
        return self._applicable_trip_stop_list
    
    def get_parent_stop(self, stop_id):
        if stop_id in self._lower_level_stop_ids:
            return self._lower_level_stop_ids[stop_id]
        elif stop_id in self._top_level_stop_ids:
            return stop_id
        else:
            raise LookupError(f"stop_id {stop_id} not a top level stop id")
    
    def get_stop_names_to_ids(self):
        return self._stop_names_to_ids