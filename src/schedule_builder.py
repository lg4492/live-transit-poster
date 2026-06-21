from datetime import datetime, date, timedelta, time
from transit_schedule import TransitSchedule
import csv

STOP_INFO_FILE = "stops.txt"
CALENDAR_DATES_FILE = "calendar_dates.txt"
TRIPS_FILE = "trips.txt"
STOP_TIMES_INFO_FILE = "stop_times.txt"

STATION_LOCATION_TYPE = '1'


def _date_string_time_to_datetime(date, time_string):
    date_to_use = date

    split_time_string = time_string.split(':')
    hour = int(split_time_string[0])
    minute = int(split_time_string[1])
    second = int(split_time_string[2])

    if hour >= 24:
        date_to_use = date_to_use + timedelta(days=1)
        hour = hour - 24

    return datetime.combine(date_to_use, time(hour, minute, second))

    


class ScheduleBuilder:
    def __init__(self, config, folder_path):
        self._folder_path = folder_path
        self._look_ahead_days = int(config.get_value("LOOK_AHEAD_DAYS"))

    
    def build_schedule(self):
        self._get_stops()
        self._get_applicable_service_ids()
        self._get_trips()
        self._prune_past_trips()
        self._get_stop_times()
        return TransitSchedule(self._stop_names_to_ids,
                        self._stop_ids,
                        self._applicable_trip_stop_list)


    def _get_stops(self):
        self._stop_names_to_ids = {}
        self._stop_ids = []

        with open(self._folder_path/STOP_INFO_FILE) as stops_file:
            dict_reader = csv.DictReader(stops_file)

            for row in dict_reader:
                if row['location_type'] == STATION_LOCATION_TYPE:
                    self._stop_names_to_ids[row['stop_name']] = row['stop_id']
                    self._stop_ids.append(row['stop_id'])

    def _get_applicable_service_ids(self):
        # TODO: This works for the "alternative" format for
        # calendar_dates.txt (i.e. the one used by WMATA), update
        # to work with the recommended format
        self._service_ids = []
        self._service_id_dates = {}

        with open(self._folder_path/CALENDAR_DATES_FILE) as calendar_dates_file:
            dict_reader = csv.DictReader(calendar_dates_file)

            today = date.today()
            upper_bound_date = today + timedelta(days=self._look_ahead_days)
            yesterday = today - timedelta(days=1)

            for row in dict_reader:
                date_string = row['date']
                date_object = datetime.strptime(date_string, "%Y%m%d").date()

                if date_object == today or date_object == yesterday or date_object <= upper_bound_date:
                    self._service_id_dates[row['service_id']] = date_object
                    self._service_ids.append(row['service_id'])
    
    def _get_trips(self):
        self._applicable_trip_service_ids = {}

        with open(self._folder_path/TRIPS_FILE) as trips_file:
            dict_reader = csv.DictReader(trips_file)

            for row in dict_reader:
                service_id = row['service_id']
                trip_id = row['trip_id']

                if service_id in self._service_ids:
                    self._applicable_trip_service_ids[trip_id] = service_id


    def _prune_past_trips(self):
        with open(self._folder_path/STOP_TIMES_INFO_FILE) as stop_times_info_file:
            dict_reader = csv.DictReader(stop_times_info_file)

            last_trip_id = None
            last_arrival_time = None

            # first, get first arrival, last arrival time
            # for each applicable trip (trips from yesterday, today, up to look-ahead-days)
            for row in dict_reader:
                # loop through stop times
                trip_id = row['trip_id']
                arrival_time = row['arrival_time']

                # if a trip is from today/tomorrow/yesterday
                if trip_id in self._applicable_trip_service_ids:
                    # if the last stop encounterd was the last stop of its trip
                    # or if this is the first stop of the file
                    if last_trip_id != trip_id and last_trip_id != None:
                        # if the last stop encountered was the last stop of its trip
                        # get its end time in datetime
                        trip_date = self._service_id_dates[self._applicable_trip_service_ids[last_trip_id]]
                        trip_endtime = last_arrival_time

                        # if a trip ends before now, discard it
                        trip_enddatetime = _date_string_time_to_datetime(trip_date, trip_endtime)
                        if trip_enddatetime < datetime.now():
                            self._applicable_trip_service_ids.pop(last_trip_id)
                    
                    last_trip_id = trip_id
                    last_arrival_time = arrival_time

            # edge case: the last stop of the last trip of the file
            if last_trip_id in self._applicable_trip_service_ids:
                # discard if it's before now
                trip_date = self._service_id_dates[self._applicable_trip_service_ids[last_trip_id]]
                trip_endtime = row['arrival_time']

                # if a trip ends before now, discard it
                trip_enddatetime = _date_string_time_to_datetime(trip_date, trip_endtime)
                if trip_enddatetime < datetime.now():
                    self._applicable_trip_service_ids.pop(last_trip_id)

    def _get_stop_times(self):
        self._applicable_trip_stop_list = {}

        # get arrival times of non-pruned trips in the schedule
        with open(self._folder_path/STOP_TIMES_INFO_FILE) as stop_times_info_file:
            dict_reader = csv.DictReader(stop_times_info_file)

            for row in dict_reader:
                trip_id = row['trip_id']

                if trip_id in self._applicable_trip_service_ids:
                    if not (trip_id in self._applicable_trip_stop_list):
                        self._applicable_trip_stop_list[trip_id] = []

                    arrival_time = row['arrival_time']
                    arrival_date = self._service_id_dates[self._applicable_trip_service_ids[trip_id]]

                    arrival_datetime = _date_string_time_to_datetime(arrival_date, arrival_time)
                    self._applicable_trip_stop_list[trip_id].append((row['stop_id'], arrival_datetime))



    def get_applicable_trips(self):
        return self._applicable_trip_service_ids
    
    def get_applicable_stop_times(self):
        return self._applicable_trip_stop_list



                        

                


                
    

    

    




        
