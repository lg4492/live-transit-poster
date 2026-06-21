from datetime import datetime
from transit_schedule_adjustment import TransitScheduleAdjustment

NO_ARRIVAL = 0


class ScheduleAdjustmentBuilder:
    def __init__(self, trip_updated_entities):
        self.trip_updated_entities = trip_updated_entities
    
    # build a dict of trip updates by stop and trip
    def build_schedule_adjustment(self):
        self._adjusted_stop_times_by_trip = {}

        for entity in self.trip_updated_entities:
            trip_id = entity.trip_update.trip.trip_id

            if not (trip_id in self._adjusted_stop_times_by_trip):
                self._adjusted_stop_times_by_trip[trip_id]= {}

            for stop_update in entity.trip_update.stop_time_update:
                stop_id = stop_update.stop_id
                updated_arrival_time = stop_update.arrival.time

                if updated_arrival_time == NO_ARRIVAL:
                    updated_arrival_time = stop_update.departure.time
                    
                # only take into account arrival times, not
                # delayed departures
                if updated_arrival_time != NO_ARRIVAL:
                    # but ignore trip updates from the past
                    updated_arrival_datetime = datetime.fromtimestamp(updated_arrival_time)

                    if updated_arrival_datetime >= datetime.now():
                        self._adjusted_stop_times_by_trip[trip_id][stop_id] = updated_arrival_datetime

        return TransitScheduleAdjustment(self._adjusted_stop_times_by_trip)