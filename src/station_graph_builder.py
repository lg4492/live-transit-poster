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

        # loop thorugh trips
        for trip in trips:
            last_stop = None
            time_train_left_last_stop = None
            for tup in trips[trip]:
                # loop through stops on the trip
                stop = tup[0]
                arrival_time_this_stop = tup[1]

                updated_arrival_time_this_stop = arrival_time_this_stop

                if last_stop != None:
                    # adjust the arrival time if needed                    
                    if trip in adjustments and stop in adjustments[trip]:
                        updated_arrival_time_this_stop = adjustments[trip][stop]
                    
                    if updated_arrival_time_this_stop >= datetime.now():
                        self.station_graph.add_connection(last_stop, 
                                                          stop, 
                                                          updated_arrival_time_this_stop, 
                                                          time_train_left_last_stop)
                
                last_stop = stop

                # assume trains leave as soon as they arrive
                # (correct for WMATA) TODO change this
                time_train_left_last_stop = updated_arrival_time_this_stop

        
        return self.station_graph


