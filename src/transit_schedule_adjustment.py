class TransitScheduleAdjustment:
    def __init__(self, adjusted_stop_times_by_trip):
        self._adjusted_stop_times_by_trip = adjusted_stop_times_by_trip

    def get_adjusted_stop_times_by_trip(self):
        return self._adjusted_stop_times_by_trip
