from src.station_graph import Station, StationGraph
from datetime import date, datetime, time
from src.exceptions import NoTrainError
import pytest

class TestStationGraph:


    def test_connection(self):
        station_graph = StationGraph()

        test_time = datetime.combine(date(2026, 1, 1), time(0, 00, 0))

        departure_time_from_A = datetime.combine(date(2026, 1, 1), time(1, 00, 0))
        arrival_time_at_B = datetime.combine(date(2026, 1, 1), time(1, 30, 0))

        station_graph.add_connection("A", "B", arrival_time_at_B, departure_time_from_A)

        # assume we walk up to station A at 12:00 AM, the next train
        # we take to B should be the one that leaves at 1:00 AM and
        # arrives at 1:30
        arr = station_graph.get_station("A").get_time_of_earliest_train_to_station_leaving_after("B", test_time)

        assert arr == arrival_time_at_B
    
    def test_non_existent_connection(self):
        station_graph = StationGraph()

        test_time = datetime.combine(date(2026, 1, 1), time(1, 15, 0))

        departure_time_from_A = datetime.combine(date(2026, 1, 1), time(1, 00, 0))
        arrival_time_at_B = datetime.combine(date(2026, 1, 1), time(1, 30, 0))

        station_graph.add_connection("A", "B", arrival_time_at_B, departure_time_from_A)

        with pytest.raises(NoTrainError):
            # assume we walk up to station A at 1:15 AM, we are not
            # able to get a train to station B
            arr = station_graph.get_station("A").get_time_of_earliest_train_to_station_leaving_after("B", test_time)
    
    def test_getting_earlier_connection(self):
        station_graph = StationGraph()

        test_time = datetime.combine(date(2026, 1, 1), time(0, 00, 0))

        departure_time_from_A = datetime.combine(date(2026, 1, 1), time(1, 00, 0))
        arrival_time_at_B = datetime.combine(date(2026, 1, 1), time(1, 30, 0))

        # this trip arrives later than the other one (even though it leaves earlier)
        # so should be ignored
        departure_time_from_A_2 = datetime.combine(date(2026, 1, 1), time(0, 50, 0))
        arrival_time_at_B_2 = datetime.combine(date(2026, 1, 1), time(1, 45, 0))

        station_graph.add_connection("A", "B", arrival_time_at_B_2, departure_time_from_A_2)
        station_graph.add_connection("A", "B", arrival_time_at_B, departure_time_from_A)

        # assume we walk up to station A at 12:00 AM, the next train
        # we take to B should be the one that leaves at 1:00 AM and
        # arrives at 1:30
        arr = station_graph.get_station("A").get_time_of_earliest_train_to_station_leaving_after("B", test_time)

        assert arr == arrival_time_at_B