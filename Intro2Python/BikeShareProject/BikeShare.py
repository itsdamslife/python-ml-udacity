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

# Condense data


def condense_data(in_file, out_file, city):
    """
    This function takes full data from the specified input file
    and writes the condensed data to a specified output file. The city
    argument determines how the input file will be parsed.
    
    HINT: See the cell below to see how the arguments are structured!
    """

    with open(out_file, 'w') as f_out, open(in_file, 'r') as f_in:
        # set up csv DictWriter object - writer requires column names for the
        # first row as the "fieldnames" argument
        out_colnames = ['duration', 'month',
                        'hour', 'day_of_week', 'user_type']
        trip_writer = csv.DictWriter(f_out, fieldnames=out_colnames)
        trip_writer.writeheader()

        ## TODO: set up csv DictReader object ##
        trip_reader = csv.DictReader(f_in)

        # collect data from and process each row
        for row in trip_reader:
            # set up a dictionary to hold the values for the cleaned and trimmed
            # data point
            new_point = {}
            
            ## TODO: use the helper functions to get the cleaned data from  ##
            ## the original data dictionaries.                              ##
            ## Note that the keys for the new_point dictionary should match ##
            ## the column names set in the DictWriter object above.         ##
            month_hour_day = time_of_trip(row, city)
            new_point['duration'] = duration_in_mins(row, city)
            new_point['month'] = month_hour_day[0]
            new_point['hour'] = month_hour_day[1]
            new_point['day_of_week'] = month_hour_day[2]
            new_point['user_type'] = type_of_user(row, city)
            
            ## TODO: write the processed information to the output file.     ##
            ## see https://docs.python.org/3/library/csv.html#writer-objects ##
            trip_writer.writerow(new_point)
        
        f_out.close()

# Run this to check your work
city_info = {'Washington': {'in_file': './data/Washington-CapitalBikeshare-2016.csv',
                            'out_file': './data/Washington-2016-Summary.csv'},
             'Chicago': {'in_file': './data/Chicago-Divvy-2016.csv',
                         'out_file': './data/Chicago-2016-Summary.csv'},
             'NYC': {'in_file': './data/NYC-CitiBike-2016.csv',
                     'out_file': './data/NYC-2016-Summary.csv'}}

for city, filenames in city_info.items():
    condense_data(filenames['in_file'], filenames['out_file'], city)
    print_first_point(filenames['out_file'])

# Exploratory Data Analysis


def number_of_trips(filename):
    """
    This function reads in a file with trip data and reports the number of
    trips made by subscribers, customers, and total overall.
    """
    with open(filename, 'r') as f_in:
        # set up csv reader object
        reader = csv.DictReader(f_in)

        # initialize count variables
        n_subscribers = 0
        n_customers = 0

        total_duration_of_all_rides = 0.0
        long_duration = 30.0
        number_of_longer_duration_trips = 0
        # tally up ride types
        for row in reader:
            total_duration_of_all_rides += float(row['duration'])
            if float(row['duration']) > long_duration:
                number_of_longer_duration_trips += 1

            if row['user_type'] == 'Subscriber':
                n_subscribers += 1
            else:
                n_customers += 1

        # compute total number of rides
        n_total = n_subscribers + n_customers

        # return tallies as a tuple
        return(n_subscribers, n_customers, n_total, total_duration_of_all_rides, number_of_longer_duration_trips)

# testing functions
def largest_among(washington, chicago, nyc):
    print("W={}; C={}; NYC={}".format(washington, chicago, nyc))
    if washington > chicago:
        if washington > nyc:
            print("Washington")
        else:
            print("NYC")
    else:
        if chicago > nyc:
            print("Chicago")
        else:
            print("NYC")


washington_summary_file = './data/Washington-2016-Summary.csv'
w_trip_details = number_of_trips(washington_summary_file)

chicago_summary_file = './data/Chicago-2016-Summary.csv'
c_trip_details = number_of_trips(chicago_summary_file)

nyc_summary_file = './data/NYC-2016-Summary.csv'
nyc_trip_details = number_of_trips(nyc_summary_file)

# highest total number of trips
w_trip = w_trip_details[2]
c_trip = c_trip_details[2]
nyc_trip = nyc_trip_details[2]
largest_among(w_trip, c_trip, nyc_trip)

# highest subscribers
w_trip = w_trip_details[0]
c_trip = c_trip_details[0]
nyc_trip = nyc_trip_details[0]
largest_among(w_trip, c_trip, nyc_trip)

# highest customers
w_trip = w_trip_details[1]
c_trip = c_trip_details[1]
nyc_trip = nyc_trip_details[1]
largest_among(w_trip, c_trip, nyc_trip)

data_file = './examples/BayArea-Y3-Summary.csv'
print(number_of_trips(data_file))

# Average trip length for each city
average_length_of_trip = w_trip_details[3]/w_trip_details[2]
print(average_length_of_trip)
average_length_of_trip = c_trip_details[3]/c_trip_details[2]
print(average_length_of_trip)
average_length_of_trip = nyc_trip_details[3]/nyc_trip_details[2]
print(average_length_of_trip)

# Longer duration proportion
percentage_of_long_duration_trips = w_trip_details[4]*100/w_trip_details[2]
print("Washington has {} percent of long duration trips".format(percentage_of_long_duration_trips))
percentage_of_long_duration_trips = c_trip_details[4]*100/c_trip_details[2]
print("Chicago has {} percent of long duration trips".format(percentage_of_long_duration_trips))
percentage_of_long_duration_trips = nyc_trip_details[4]*100/nyc_trip_details[2]
print("NYC has {} percent of long duration trips".format(percentage_of_long_duration_trips))

# condensing data based on user type
def condense_data_for_long_rides(filename, usr_type):
    """
    This function reads in a file with trip data and reports the number of
    trips made by subscribers, customers, and total overall.
    """
    with open(filename, 'r') as f_in:
        # set up csv reader object
        reader = csv.DictReader(f_in)

        # initialize count variables
        total_long_ride_duration = 0.0
        total_long_rides = 0

        long_duration = 30.0
        # tally up ride types
        for row in reader:
            if row['user_type'] == usr_type:
                ride_duration = float(row['duration'])
                if ride_duration > long_duration:
                    total_long_rides += 1
                    total_long_ride_duration += ride_duration

        # return tallies as a tuple
        return(total_long_ride_duration, total_long_rides)


# for Subscriber
nyc_summary_file = './data/NYC-2016-Summary.csv'
long_ride_analysis_for_subscriber = condense_data_for_long_rides(nyc_summary_file, 'Subscriber')
avg_long_ride_duration_by_subscriber = long_ride_analysis_for_subscriber[0]/long_ride_analysis_for_subscriber[1]

# for Customer
long_ride_analysis_for_customer = condense_data_for_long_rides(nyc_summary_file, 'Customer')
avg_long_ride_duration_by_customer = long_ride_analysis_for_customer[0] / long_ride_analysis_for_customer[1]

print("In NYC the average Subscriber trip duration to be {} minutes and the average Customer trip duration to be {} minutes.".format(avg_long_ride_duration_by_subscriber, avg_long_ride_duration_by_customer))
if avg_long_ride_duration_by_subscriber > avg_long_ride_duration_by_customer:
    print("In NYC, Subscribers do more longer rides than Customers")
else:
    print("In NYC, Customers do more longer rides than Subscribers")
