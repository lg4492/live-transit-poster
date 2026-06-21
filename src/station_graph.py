class Station:
    def __init__(self, stop_id):
        self.stop_id = stop_id
        self.connections = {}

    def add_connection_if_earlier(self, stop_id, time, station_object):
        if stop_id in self.connections:
            existing_time = self.connections[stop_id]["time"]
            
            if time < existing_time:
                self.connections[stop_id]["time"] = time
        else:
            self.connections[stop_id] = {"time": time, "object": station_object}

    def get_connection_time(self, stop_id):
        if stop_id in self.connections:
            return self.connections[stop_id]["time"]
        
        raise LookupError(f"Station {self.stop_id} has no connection to {stop_id}")

class StationGraph:
    def __init__(self):
        self.station_objects = {}

    def _create_station_if_missing(self, stop_id):
        if not (stop_id in self.station_objects):
            self.station_objects[stop_id] = Station(stop_id)
    
    def add_connection(self, stop_id_from, stop_id_to, arrival_time):
        self._create_station_if_missing(stop_id_from)
        self._create_station_if_missing(stop_id_to)
        self.station_objects[stop_id_from].add_connection_if_earlier(stop_id_to, arrival_time, self.station_objects[stop_id_to])

    def get_station(self, stop_id):
        if stop_id in self.station_objects:
            return self.station_objects[stop_id]
        
        raise LookupError(f"No station with id {stop_id} found")