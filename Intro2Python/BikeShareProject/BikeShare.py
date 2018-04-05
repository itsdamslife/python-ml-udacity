import csv
from datetime import datetime
from pprint import pprint


def print_first_point(filename):
    """
    This function prints and returns the first data point (second row) from
    a csv file that includes a header row.
    """
    # print city name for reference
    city = filename.split('-')[0].split('/')[-1]
    print('\nCity: {}'.format(city))

    with open(filename, 'r') as f_in:
        ## TODO: Use the csv library to set up a DictReader object. ##
        ## see https://docs.python.org/3/library/csv.html           ##
        trip_reader = csv.DictReader(f_in)

        ## TODO: Use a function on the DictReader object to read the     ##
        ## first trip from the data file and store it in a variable.     ##
        ## see https://docs.python.org/3/library/csv.html#reader-objects ##
        for row in trip_reader:
            first_trip = row
            break

        ## TODO: Use the pprint library to print the first trip. ##
        ## see https://docs.python.org/3/library/pprint.html     ##
        pprint(first_trip)

    # output city name and first trip for later testing
    return (city, first_trip)


# list of files for each city
data_files = [
    './data/NYC-CitiBike-2016.csv',
    './data/Chicago-Divvy-2016.csv',
    './data/Washington-CapitalBikeshare-2016.csv',
]

# print the first trip from each file, store in dictionary
example_trips = {}
for data_file in data_files:
    city, first_trip = print_first_point(data_file)
    example_trips[city] = first_trip

# Condensing the Trip Data


def duration_in_mins(datum, city):
    """
    Takes as input a dictionary containing info about a single trip (datum) and
    its origin city (city) and returns the trip duration in units of minutes.
    
    Remember that Washington is in terms of milliseconds while Chicago and NYC
    are in terms of seconds. 
    
    HINT: The csv module reads in all of the data as strings, including numeric
    values. You will need a function to convert the strings into an appropriate
    numeric type when making your transformations.
    see https://docs.python.org/3/library/functions.html
    """
    duration_in_secs = 0.0
    if datum.get("tripduration") is not None:
        duration_in_secs = float(datum["tripduration"])
    elif datum.get("Duration (ms)") is not None:
        duration_in_secs = float(datum["Duration (ms)"])/1000

    return duration_in_secs/60


# Some tests to check that your code works. There should be no output if all of
# the assertions pass. The `example_trips` dictionary was obtained from when
# you printed the first trip from each of the original data files.
tests = {'NYC': 13.9833, 'Chicago': 15.4333, 'Washington': 7.1231}

for city in tests:
    duration_in_min = duration_in_mins(example_trips[city], city)
    print("{} duration in mins : {}".format(city, duration_in_min))
    assert abs(duration_in_min - tests[city]) < .001


def time_of_trip(datum, city):
    """
    Takes as input a dictionary containing info about a single trip (datum) and
    its origin city (city) and returns the month, hour, and day of the week in
    which the trip was made.
    
    Remember that NYC includes seconds, while Washington and Chicago do not.
    
    HINT: You should use the datetime module to parse the original date
    strings into a format that is useful for extracting the desired information.
    see https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
    """

    month = 0
    hour = 0
    day_of_week = "Sunday"

    date_string = ""
    if datum.get("starttime") is not None:
        date_string = datum["starttime"]  # 1/1/2016 00:09:55, 3/31/2016 23:30
    elif datum.get("Start date") is not None:
        date_string = datum["Start date"]  # 3/31/2016 22:57

    # if there is no seconds parameter in the string add ':00' to it
    if date_string[-6] is not ':':
        date_string += ":00"
    
    date_time_object = datetime.strptime(date_string, "%m/%d/%Y %H:%M:%S")

    month = int(date_time_object.strftime('%m'))
    hour = int(date_time_object.strftime('%H'))
    day_of_week = date_time_object.strftime('%A')
    
    return (month, hour, day_of_week)


# Some tests to check that your code works. There should be no output if all of
# the assertions pass. The `example_trips` dictionary was obtained from when
# you printed the first trip from each of the original data files.
tests = {
    'NYC': (1, 0, 'Friday'),
    'Chicago': (3, 23, 'Thursday'),
    'Washington': (3, 22, 'Thursday')
}

for city in tests:
    print("========\n{}:\n{}\n==========".format(city, example_trips[city]))  # debug
    m_h_d = time_of_trip(example_trips[city], city)
    print(m_h_d)
    assert m_h_d == tests[city]

# Type of the user - retrieval

def type_of_user(datum, city):
    """
    Takes as input a dictionary containing info about a single trip (datum) and
    its origin city (city) and returns the type of system user that made the
    trip.
    
    Remember that Washington has different category names compared to Chicago
    and NYC. 
    """

    user_type = ""
    # 'usertype'(Subscriber or Customer) or 'Member Type'(Registered or Casual)
    if city is "Washington":
        user_type = "Subscriber" if datum.get("Member Type") == "Registered" else "Customer"
    else:
        user_type = datum.get("usertype")

    return user_type


# Some tests to check that your code works. There should be no output if all of
# the assertions pass. The `example_trips` dictionary was obtained from when
# you printed the first trip from each of the original data files.
tests = {'NYC': 'Customer',
         'Chicago': 'Subscriber',
         'Washington': 'Subscriber'}

for city in tests:
    usr_typ = type_of_user(example_trips[city], city)
    print("============={}".format(usr_typ)) # debug
    assert usr_typ == tests[city]
