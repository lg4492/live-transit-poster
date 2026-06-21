from src.station_graph import Station, StationGraph
from datetime import date, datetime, time

class TestStationGraph:
    def test_connection(self):
        station_graph = StationGraph()

        arrival_time = datetime.combine(date(2026, 1, 1), time(1, 0, 0))

        station_graph.add_connection("A", "B", arrival_time)

        ret = station_graph.get_station("A").get_connection_time("B")

        assert ret == arrival_time

    def test_connection_earlier_time_replacement(self):
        station_graph = StationGraph()

        arrival_time = datetime.combine(date(2026, 1, 1), time(1, 0, 0))

        station_graph.add_connection("A", "B", arrival_time)

        earlier_arrival_time = datetime.combine(date(2026, 1, 1), time(0, 30, 0))

        station_graph.add_connection("A", "B", earlier_arrival_time)
       
        ret = station_graph.get_station("A").get_connection_time("B")

        assert ret == earlier_arrival_time