import logging
import sys

def setup_logging(log_file_name):
    # create a global file handler
    file_handler = logging.FileHandler(log_file_name, mode="a")
    file_handler.setLevel(logging.DEBUG)

    # define a clean formatting layout
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    # attach it globally to the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)  # High level constraint must match lowest expected log
    root_logger.addHandler(file_handler)

    # take out the terminal logging
    for handler in root_logger.handlers[:]:
        if isinstance(handler, logging.StreamHandler) and handler.stream in (sys.stdout, sys.stderr):
            root_logger.removeHandler(handler)
