from station_graph import StationGraph
from transit_schedule import TransitSchedule
from transit_schedule_adjustment import TransitScheduleAdjustment
from datetime import datetime


class StationGraphBuilder:
    def __init__(self, schedule, schedule_adjustment):
        self.station_graph = StationGraph()
        self.schedule = schedule
        self.schedule_adjustment = schedule_adjustment

    def build_station_graph(self):
        trips = self.schedule.get_applicable_trip_stop_list()
        adjustments = self.schedule_adjustment.get_adjusted_stop_times_by_trip()

        for trip in trips:
            last_stop = None
            for tup in trips[trip]:
                stop = tup[0]
                arrival_time = tup[1]


                if last_stop != None:
                    updated_arrival_time = arrival_time
                    if trip in adjustments and stop in adjustments[trip]:
                        updated_arrival_time = adjustments[trip][stop]
                    
                    if updated_arrival_time >= datetime.now():
                        self.station_graph.add_connection(last_stop, stop, updated_arrival_time)
                last_stop = stop
        
        return self.station_graph


