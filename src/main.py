from config import Config
from gtfs_getter import GTFSGetter
from schedule_builder import ScheduleBuilder
from schedule_adjustment_builder import ScheduleAdjustmentBuilder
from gtfsr_getter import GTFSRGetter
from logging_setup import setup_logging
from transit_schedule_adjustment import TransitScheduleAdjustment
from station_graph_builder import StationGraphBuilder
from pathlib import Path


PROJECT_ROOT_DIR = Path(__file__).resolve().parent.parent

def main():
    # set up logging for the program
    setup_logging(PROJECT_ROOT_DIR / "transit.log")

    # config manager
    config = Config()

    # getting and validating gtfs
    gtfs_getter = GTFSGetter(config)
    gtfs_getter.get_gtfs_files(PROJECT_ROOT_DIR / "schedule.zip",  PROJECT_ROOT_DIR / "schedule")

    # get the transit schedule from the GTFS zip
    schedule_builder = ScheduleBuilder(config, PROJECT_ROOT_DIR / "schedule")
    schedule = schedule_builder.build_schedule()

    # get schedule adjustments from gtfsr api
    gtfsr_getter = GTFSRGetter(config)
    schedule_adjustment_builder = ScheduleAdjustmentBuilder(gtfsr_getter.get_trip_updates(), schedule)
    schedule_adjustment = schedule_adjustment_builder.build_schedule_adjustment()

    station_graph_builder = StationGraphBuilder(schedule, schedule_adjustment)
    station_graph = station_graph_builder.build_station_graph()

    breakpoint()





    


# This guard ensures the code only runs if the file is executed directly
if __name__ == "__main__":
    main()