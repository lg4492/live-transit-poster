from config import Config
from gtfs_getter import GTFSGetter
from logging_setup import setup_logging

def main():
    # set up logging for the program
    setup_logging("transit.log")

    # config manager
    config = Config()

    # getting and validating gtfs
    gtfs_getter = GTFSGetter(config)
    gtfs_getter.download_and_validate_gtfs("schedule.zip")


    


# This guard ensures the code only runs if the file is executed directly
if __name__ == "__main__":
    main()