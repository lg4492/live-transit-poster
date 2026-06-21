from src.config import Config
from src.schedule_builder import _date_string_time_to_datetime, ScheduleBuilder
from datetime import datetime, date, timedelta, time
from freezegun import freeze_time
import test_constants


class TestScheduleBuilderClass:
    def test_date_string_time_to_datetime_normal(self):
        comparison = datetime.combine(date.today(), time(7, 0, 0))

        ret = _date_string_time_to_datetime(date.today(), "07:00:00")

        assert ret == comparison
    
    def test_date_string_time_to_datetime_next_day(self):
        comparison = datetime.combine(date.today() + timedelta(days=1), time(2, 0, 0))

        ret = _date_string_time_to_datetime(date.today(), "26:00:00")

        assert ret == comparison

    # test that schedule builder includes trips that end
    # past 24:00:00 on the previous day if they end after
    # the current time
    def test_schedule_builder_trips_past_24h(self):
        config = Config(".env.test")
        with freeze_time("2026-06-19 01:00:00"):
            sb = ScheduleBuilder(config, test_constants.PROJECT_ROOT_DIR / "tests" / "test_gtfs_data")
            sb.build_schedule()

            ret = sb.get_applicable_trips()

            assert "T_5" in ret
            assert ret["T_5"] == "S_A"

    # test that schedule builder includes all trips from today 
    # after the current time
    def test_schedule_builder_todays_trips(self):
        config = Config(".env.test")

        with freeze_time("2026-06-19 01:00:00"):
            sb = ScheduleBuilder(config, test_constants.PROJECT_ROOT_DIR / "tests" / "test_gtfs_data")
            sb.build_schedule()

            ret = sb.get_applicable_trips()

            for trip in ["T_6", "T_7", "T_8", "T_9", "T_10"]:
                assert trip in ret
                assert ret[trip] == "S_B"

    # test that schedule builder includes all trips from tomorrow
    # (LOOK_AHEAD_DAYS = 1)
    def test_schedule_builder_tomorrows_trips(self):
        config = Config(".env.test")
        with freeze_time("2026-06-19 01:00:00"):
            sb = ScheduleBuilder(config, test_constants.PROJECT_ROOT_DIR / "tests" / "test_gtfs_data")
            sb.build_schedule()

            ret = sb.get_applicable_trips()

            for trip in ["T_11", "T_12", "T_13", "T_14", "T_15"]:
                assert trip in ret
                assert ret[trip] == "S_C"
            
    # test that schedule builder includes no extra trips
    def test_schedule_builder_no_extra_trips(self):
        config = Config(".env.test")
        with freeze_time("2026-06-19 01:00:00"):
            sb = ScheduleBuilder(config, test_constants.PROJECT_ROOT_DIR / "tests" / "test_gtfs_data")
            sb.build_schedule()

            ret = sb.get_applicable_trips()

            assert len(ret) == 11

    def test_schedule_builder_stop_times(self):
        config = Config(".env.test")
        with freeze_time("2026-06-19 01:00:00"):
            sb = ScheduleBuilder(config, test_constants.PROJECT_ROOT_DIR / "tests" / "test_gtfs_data")
            sb.build_schedule()

            ret = sb.get_applicable_stop_times()

            assert ret["T_5"][0][0] == "ST_A"