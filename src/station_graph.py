from exceptions import NoTrainError
import bisect


class Station:
    def __init__(self, stop_id):
        self.stop_id = stop_id
        self.connections = {}

    def add_connection(self, to_stop_id, arrival_time_to_stop, departure_time_this_stop, station_object):
        if to_stop_id in self.connections:
            bisect.insort(self.connections[to_stop_id][1], (departure_time_this_stop, arrival_time_to_stop))
        else:
            self.connections[to_stop_id] = (station_object, [(departure_time_this_stop, arrival_time_to_stop)])

    def get_time_of_earliest_train_to_station_leaving_after(self, other_station, time):
        # get the train that arrives at station "other_station"
        # after time "time" that departs from this station also after 
        # time "time"
        
        index = bisect.bisect_right(self.connections[other_station][1], (time, time))

        list_len = len(self.connections[other_station][1])

        if index < list_len:
            (dept, arr) = self.connections[other_station][1][index]
            if arr >= time and dept >= time:
                return arr
        
        raise NoTrainError(f"No connection to {other_station} from {self.stop_id} found that leaves after {time}")
    
class StationGraph:
    def __init__(self):
        self.station_objects = {}

    def _create_station_if_missing(self, stop_id):
        if not (stop_id in self.station_objects):
            self.station_objects[stop_id] = Station(stop_id)
    
    def add_connection(self, stop_id_from, stop_id_to, arrival_time_at_to_stop, departure_time_at_from_stop):
        self._create_station_if_missing(stop_id_from)
        self._create_station_if_missing(stop_id_to)
        self.station_objects[stop_id_from].add_connection(stop_id_to, arrival_time_at_to_stop, departure_time_at_from_stop, self.station_objects[stop_id_to])

    def get_station(self, stop_id):
        if stop_id in self.station_objects:
            return self.station_objects[stop_id]
        
        raise LookupError(f"No station with id {stop_id} found")