from datetime import datetime
from exceptions import NoTrainError

class ShortestPathGetter:
    def __init__(self, station_graph, home_station_id):
        self._station_graph = station_graph
        self._home_station_id = home_station_id
        self._station_shortest_times = {}

    def recursive_shortest_path(self, station, arrival_time, first_node):
        if station.stop_id == self._home_station_id and (not first_node):
            return
        else:
            connections = station.connections

            for connection_id in connections:
                connection_station = station.connections[connection_id][0]

                try:
                    earliest_arrival_at_connection = station.get_time_of_earliest_train_to_station_leaving_after(connection_id, arrival_time)
                except NoTrainError:
                    earliest_arrival_at_connection = datetime.max

                if connection_id in self._station_shortest_times:
                    existing_time = self._station_shortest_times[connection_id]

                    if existing_time > earliest_arrival_at_connection:
                        self._station_shortest_times[connection_id] = earliest_arrival_at_connection
                        self.recursive_shortest_path(connection_station, earliest_arrival_at_connection, False)
                else:
                    self._station_shortest_times[connection_id] = earliest_arrival_at_connection
                    self.recursive_shortest_path(connection_station, earliest_arrival_at_connection, False)


    def get_shortest_paths(self, arrival_time):
        home_station = self._station_graph.get_station(self._home_station_id)
        self._station_shortest_times[self._home_station_id] = arrival_time
        self.recursive_shortest_path(home_station, arrival_time, True)





    

