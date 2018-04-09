
# coding: utf-8

# # 2016 US Bike Share Activity Snapshot
# 
# ## Table of Contents
# - [Introduction](#intro)
# - [Posing Questions](#pose_questions)
# - [Data Collection and Wrangling](#wrangling)
#   - [Condensing the Trip Data](#condensing)
# - [Exploratory Data Analysis](#eda)
#   - [Statistics](#statistics)
#   - [Visualizations](#visualizations)
# - [Performing Your Own Analysis](#eda_continued)
# - [Conclusions](#conclusions)
# 
# <a id='intro'></a>
# ## Introduction
# 
# > **Tip**: Quoted sections like this will provide helpful instructions on how to navigate and use a Jupyter notebook.
# 
# Over the past decade, bicycle-sharing systems have been growing in number and popularity in cities across the world. Bicycle-sharing systems allow users to rent bicycles for short trips, typically 30 minutes or less. Thanks to the rise in information technologies, it is easy for a user of the system to access a dock within the system to unlock or return bicycles. These technologies also provide a wealth of data that can be used to explore how these bike-sharing systems are used.
# 
# In this project, you will perform an exploratory analysis on data provided by [Motivate](https://www.motivateco.com/), a bike-share system provider for many major cities in the United States. You will compare the system usage between three large cities: New York City, Chicago, and Washington, DC. You will also see if there are any differences within each system for those users that are registered, regular users and those users that are short-term, casual users.

# <a id='pose_questions'></a>
# ## Posing Questions
# 
# Before looking at the bike sharing data, you should start by asking questions you might want to understand about the bike share data. Consider, for example, if you were working for Motivate. What kinds of information would you want to know about in order to make smarter business decisions? If you were a user of the bike-share service, what factors might influence how you would want to use the service?
# 
# **Question 1**: Write at least two questions related to bike sharing that you think could be answered by data.
# 
# **Answer**: 1. What is the average number of people per day using this service? 2. How many docks are available near the prime locations?
# 
# > **Tip**: If you double click on this cell, you will see the text change so that all of the formatting is removed. This allows you to edit this block of text. This block of text is written using [Markdown](http://daringfireball.net/projects/markdown/syntax), which is a way to format text using headers, links, italics, and many other options using a plain-text syntax. You will also use Markdown later in the Nanodegree program. Use **Shift** + **Enter** or **Shift** + **Return** to run the cell and show its rendered form.

# <a id='wrangling'></a>
# ## Data Collection and Wrangling
# 
# Now it's time to collect and explore our data. In this project, we will focus on the record of individual trips taken in 2016 from our selected cities: New York City, Chicago, and Washington, DC. Each of these cities has a page where we can freely download the trip data.:
# 
# - New York City (Citi Bike): [Link](https://www.citibikenyc.com/system-data)
# - Chicago (Divvy): [Link](https://www.divvybikes.com/system-data)
# - Washington, DC (Capital Bikeshare): [Link](https://www.capitalbikeshare.com/system-data)
# 
# If you visit these pages, you will notice that each city has a different way of delivering its data. Chicago updates with new data twice a year, Washington DC is quarterly, and New York City is monthly. **However, you do not need to download the data yourself.** The data has already been collected for you in the `/data/` folder of the project files. While the original data for 2016 is spread among multiple files for each city, the files in the `/data/` folder collect all of the trip data for the year into one file per city. Some data wrangling of inconsistencies in timestamp format within each city has already been performed for you. In addition, a random 2% sample of the original data is taken to make the exploration more manageable. 
# 
# **Question 2**: However, there is still a lot of data for us to investigate, so it's a good idea to start off by looking at one entry from each of the cities we're going to analyze. Run the first code cell below to load some packages and functions that you'll be using in your analysis. Then, complete the second code cell to print out the first trip recorded from each of the cities (the second line of each data file).
# 
# > **Tip**: You can run a code cell like you formatted Markdown cells above by clicking on the cell and using the keyboard shortcut **Shift** + **Enter** or **Shift** + **Return**. Alternatively, a code cell can be executed using the **Play** button in the toolbar after selecting it. While the cell is running, you will see an asterisk in the message to the left of the cell, i.e. `In [*]:`. The asterisk will change into a number to show that execution has completed, e.g. `In [1]`. If there is output, it will show up as `Out [1]:`, with an appropriate number to match the "In" number.

# In[11]:


## import all necessary packages and functions.
import csv # read and write csv files
from datetime import datetime # operations to parse dates
from pprint import pprint # use to print data structures like dictionaries in
                          # a nicer way than the base print function.


# In[12]:


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
data_files = ['./data/NYC-CitiBike-2016.csv',
              './data/Chicago-Divvy-2016.csv',
              './data/Washington-CapitalBikeshare-2016.csv',]

# print the first trip from each file, store in dictionary
example_trips = {}
for data_file in data_files:
    city, first_trip = print_first_point(data_file)
    example_trips[city] = first_trip


# If everything has been filled out correctly, you should see below the printout of each city name (which has been parsed from the data file name) that the first trip has been parsed in the form of a dictionary. When you set up a `DictReader` object, the first row of the data file is normally interpreted as column names. Every other row in the data file will use those column names as keys, as a dictionary is generated for each row.
# 
# This will be useful since we can refer to quantities by an easily-understandable label instead of just a numeric index. For example, if we have a trip stored in the variable `row`, then we would rather get the trip duration from `row['duration']` instead of `row[0]`.
# 
# <a id='condensing'></a>
# ### Condensing the Trip Data
# 
# It should also be observable from the above printout that each city provides different information. Even where the information is the same, the column names and formats are sometimes different. To make things as simple as possible when we get to the actual exploration, we should trim and clean the data. Cleaning the data makes sure that the data formats across the cities are consistent, while trimming focuses only on the parts of the data we are most interested in to make the exploration easier to work with.
# 
# You will generate new data files with five values of interest for each trip: trip duration, starting month, starting hour, day of the week, and user type. Each of these may require additional wrangling depending on the city:
# 
# - **Duration**: This has been given to us in seconds (New York, Chicago) or milliseconds (Washington). A more natural unit of analysis will be if all the trip durations are given in terms of minutes.
# - **Month**, **Hour**, **Day of Week**: Ridership volume is likely to change based on the season, time of day, and whether it is a weekday or weekend. Use the start time of the trip to obtain these values. The New York City data includes the seconds in their timestamps, while Washington and Chicago do not. The [`datetime`](https://docs.python.org/3/library/datetime.html) package will be very useful here to make the needed conversions.
# - **User Type**: It is possible that users who are subscribed to a bike-share system will have different patterns of use compared to users who only have temporary passes. Washington divides its users into two types: 'Registered' for users with annual, monthly, and other longer-term subscriptions, and 'Casual', for users with 24-hour, 3-day, and other short-term passes. The New York and Chicago data uses 'Subscriber' and 'Customer' for these groups, respectively. For consistency, you will convert the Washington labels to match the other two.
# 
# 
# **Question 3a**: Complete the helper functions in the code cells below to address each of the cleaning tasks described above.

# In[13]:


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
tests = {'NYC': 13.9833,
         'Chicago': 15.4333,
         'Washington': 7.1231}

for city in tests:
    assert abs(duration_in_mins(example_trips[city], city) - tests[city]) < .001


# In[14]:


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
tests = {'NYC': (1, 0, 'Friday'),
         'Chicago': (3, 23, 'Thursday'),
         'Washington': (3, 22, 'Thursday')}

for city in tests:
    assert time_of_trip(example_trips[city], city) == tests[city]


# In[15]:


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
    assert type_of_user(example_trips[city], city) == tests[city]


# **Question 3b**: Now, use the helper functions you wrote above to create a condensed data file for each city consisting only of the data fields indicated above. In the `/examples/` folder, you will see an example datafile from the [Bay Area Bike Share](http://www.bayareabikeshare.com/open-data) before and after conversion. Make sure that your output is formatted to be consistent with the example file.

# In[16]:


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
        out_colnames = ['duration', 'month', 'hour', 'day_of_week', 'user_type']        
        trip_writer = csv.DictWriter(f_out, fieldnames = out_colnames)
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
            


# In[17]:


# Run this cell to check your work
city_info = {'Washington': {'in_file': './data/Washington-CapitalBikeshare-2016.csv',
                            'out_file': './data/Washington-2016-Summary.csv'},
             'Chicago': {'in_file': './data/Chicago-Divvy-2016.csv',
                         'out_file': './data/Chicago-2016-Summary.csv'},
             'NYC': {'in_file': './data/NYC-CitiBike-2016.csv',
                     'out_file': './data/NYC-2016-Summary.csv'}}

for city, filenames in city_info.items():
    condense_data(filenames['in_file'], filenames['out_file'], city)
    print_first_point(filenames['out_file'])


# > **Tip**: If you save a jupyter Notebook, the output from running code blocks will also be saved. However, the state of your workspace will be reset once a new session is started. Make sure that you run all of the necessary code blocks from your previous session to reestablish variables and functions before picking up where you last left off.
# 
# <a id='eda'></a>
# ## Exploratory Data Analysis
# 
# Now that you have the data collected and wrangled, you're ready to start exploring the data. In this section you will write some code to compute descriptive statistics from the data. You will also be introduced to the `matplotlib` library to create some basic histograms of the data.
# 
# <a id='statistics'></a>
# ### Statistics
# 
# First, let's compute some basic counts. The first cell below contains a function that uses the csv module to iterate through a provided data file, returning the number of trips made by subscribers and customers. The second cell runs this function on the example Bay Area data in the `/examples/` folder. Modify the cells to answer the question below.
# 
# **Question 4a**: Which city has the highest number of trips? Which city has the highest proportion of trips made by subscribers? Which city has the highest proportion of trips made by short-term customers?
# 
# **Answer**: NYC has the highest number of trips. NYC has the highest proportion of trips made by subscribers. NYC has the highest proportion of trips made by short-term customers.

# In[18]:


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


# In[19]:


def largest_among(washington, chicago, nyc):
    print("W={}; C={}; NYC={}".format(washington,chicago,nyc))
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


# In[20]:


washington_summary_file = './data/Washington-2016-Summary.csv'
w_trip_details = number_of_trips(washington_summary_file)

chicago_summary_file = './data/Chicago-2016-Summary.csv'
c_trip_details = number_of_trips(chicago_summary_file)

nyc_summary_file = './data/NYC-2016-Summary.csv'
nyc_trip_details = number_of_trips(nyc_summary_file)


# In[21]:


w_trip = w_trip_details[0]
c_trip = c_trip_details[0]
nyc_trip = nyc_trip_details[0]
largest_among(w_trip, c_trip, nyc_trip)


# In[22]:


w_trip = w_trip_details[1]
c_trip = c_trip_details[1]
nyc_trip = nyc_trip_details[1]
largest_among(w_trip, c_trip, nyc_trip)


# In[23]:


w_trip = w_trip_details[2]
c_trip = c_trip_details[2]
nyc_trip = nyc_trip_details[2]
largest_among(w_trip, c_trip, nyc_trip)


# In[24]:


## Modify this and the previous cell to answer Question 4a. Remember to run ##
## the function on the cleaned data files you created from Question 3.      ##
data_file = './examples/BayArea-Y3-Summary.csv'
print(number_of_trips(data_file))


# > **Tip**: In order to add additional cells to a notebook, you can use the "Insert Cell Above" and "Insert Cell Below" options from the menu bar above. There is also an icon in the toolbar for adding new cells, with additional icons for moving the cells up and down the document. By default, new cells are of the code type; you can also specify the cell type (e.g. Code or Markdown) of selected cells from the Cell menu or the dropdown in the toolbar.
# 
# Now, you will write your own code to continue investigating properties of the data.
# 
# **Question 4b**: Bike-share systems are designed for riders to take short trips. Most of the time, users are allowed to take trips of 30 minutes or less with no additional charges, with overage charges made for trips of longer than that duration. What is the average trip length for each city? What proportion of rides made in each city are longer than 30 minutes?
# 
# **Answer**: Average trip length of Washington is 18.93287355913721, Average trip length of Chicago is 16.563629368787335, Average trip length of NYC is 15.81259299802294.
# Washington has 10.83888671109369 percent of long duration trips. Chicago has 8.332062497400562 percent of long duration trips. NYC has 7.3024371563378345 percent of long duration trips.

# In[25]:


## Use this and additional cells to answer Question 4b.                 ##
##                                                                      ##
## HINT: The csv module reads in all of the data as strings, including  ##
## numeric values. You will need a function to convert the strings      ##
## into an appropriate numeric type before you aggregate data.          ##
## TIP: For the Bay Area example, the average trip length is 14 minutes ##
## and 3.5% of trips are longer than 30 minutes.                        ##


average_length_of_trip = w_trip_details[3]/w_trip_details[2]
print("Average trip length of Washington is {}".format(average_length_of_trip))
average_length_of_trip = c_trip_details[3]/c_trip_details[2]
print("Average trip length of Chicago is {}".format(average_length_of_trip))
average_length_of_trip = nyc_trip_details[3]/nyc_trip_details[2]
print("Average trip length of NYC is {}".format(average_length_of_trip))


# Longer duration proportion
percentage_of_long_duration_trips = w_trip_details[4]*100/w_trip_details[2]
print("Washington has {} percent of long duration trips".format(percentage_of_long_duration_trips))
percentage_of_long_duration_trips = c_trip_details[4]*100/c_trip_details[2]
print("Chicago has {} percent of long duration trips".format(percentage_of_long_duration_trips))
percentage_of_long_duration_trips = nyc_trip_details[4]*100/nyc_trip_details[2]
print("NYC has {} percent of long duration trips".format(percentage_of_long_duration_trips))


# **Question 4c**: Dig deeper into the question of trip duration based on ridership. Choose one city. Within that city, which type of user takes longer rides on average: Subscribers or Customers?
# 
# **Answer**: In NYC the average Subscriber trip duration to be 63.474524661742294 minutes and the average Customer trip duration to be 84.55745393634842 minutes.
# In NYC, Customers do more longer rides than Subscribers

# In[26]:


## Use this and additional cells to answer Question 4c. If you have    ##
## not done so yet, consider revising some of your previous code to    ##
## make use of functions for reusability.                              ##
##                                                                     ##
## TIP: For the Bay Area example data, you should find the average     ##
## Subscriber trip duration to be 9.5 minutes and the average Customer ##
## trip duration to be 54.6 minutes. Do the other cities have this     ##
## level of difference?                                                ##
import csv
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
nyc_summary_file = './data/Chicago-2016-Summary.csv'
long_ride_analysis_for_subscriber = condense_data_for_long_rides(nyc_summary_file, 'Subscriber')
avg_long_ride_duration_by_subscriber = long_ride_analysis_for_subscriber[0]/long_ride_analysis_for_subscriber[1]

# for Customer
long_ride_analysis_for_customer = condense_data_for_long_rides(nyc_summary_file, 'Customer')
avg_long_ride_duration_by_customer = long_ride_analysis_for_customer[0] / long_ride_analysis_for_customer[1]

print("In Chicago the average Subscriber trip duration to be {} minutes and the average Customer trip duration to be {} minutes.".format(avg_long_ride_duration_by_subscriber, avg_long_ride_duration_by_customer))
if avg_long_ride_duration_by_subscriber > avg_long_ride_duration_by_customer:
    print("In Chicago, Subscribers do more longer rides than Customers")
else:
    print("In Chicago, Customers do more longer rides than Subscribers")


# <a id='visualizations'></a>
# ### Visualizations
# 
# The last set of values that you computed should have pulled up an interesting result. While the mean trip time for Subscribers is well under 30 minutes, the mean trip time for Customers is actually _above_ 30 minutes! It will be interesting for us to look at how the trip times are distributed. In order to do this, a new library will be introduced here, `matplotlib`. Run the cell below to load the library and to generate an example plot.

# In[27]:


# load library
import matplotlib.pyplot as plt

# this is a 'magic word' that allows for plots to be displayed
# inline with the notebook. If you want to know more, see:
# http://ipython.readthedocs.io/en/stable/interactive/magics.html
get_ipython().run_line_magic('matplotlib', 'inline')

# example histogram, data taken from bay area sample
data = [ 7.65,  8.92,  7.42,  5.50, 16.17,  4.20,  8.98,  9.62, 11.48, 14.33,
        19.02, 21.53,  3.90,  7.97,  2.62,  2.67,  3.08, 14.40, 12.90,  7.83,
        25.12,  8.30,  4.93, 12.43, 10.60,  6.17, 10.88,  4.78, 15.15,  3.53,
         9.43, 13.32, 11.72,  9.85,  5.22, 15.10,  3.95,  3.17,  8.78,  1.88,
         4.55, 12.68, 12.38,  9.78,  7.63,  6.45, 17.38, 11.90, 11.52,  8.63,]
plt.hist(data)
plt.title('Distribution of Trip Durations')
plt.xlabel('Duration (m)')
plt.show()


# In the above cell, we collected fifty trip times in a list, and passed this list as the first argument to the `.hist()` function. This function performs the computations and creates plotting objects for generating a histogram, but the plot is actually not rendered until the `.show()` function is executed. The `.title()` and `.xlabel()` functions provide some labeling for plot context.
# 
# You will now use these functions to create a histogram of the trip times for the city you selected in question 4c. Don't separate the Subscribers and Customers for now: just collect all of the trip times and plot them.

# In[28]:


## Use this and additional cells to collect all of the trip times as a list ##
## and then use pyplot functions to generate a histogram of trip times.     ##

# load library
import matplotlib.pyplot as plt
import csv
# this is a 'magic word' that allows for plots to be displayed
# inline with the notebook. If you want to know more, see:
# http://ipython.readthedocs.io/en/stable/interactive/magics.html
get_ipython().run_line_magic('matplotlib', 'inline')

def get_ride_time_date(filename):
    """
    This function reads in a file with trip data and reports the number of
    trips made by subscribers, customers, and total overall.
    """
    with open(filename, 'r') as f_in:
        # set up csv reader object
        reader = csv.DictReader(f_in)
        ride_time_list = []

        for row in reader:
            ride_time_list.append(row['duration'])

        return ride_time_list


# for Subscriber
summary_file = './data/Chicago-2016-Summary.csv'
ride_times = get_ride_time_date(summary_file)

plt.hist(ride_times)
plt.title('Distribution of Trip Durations in Chicago')
plt.xlabel('Duration (m)')
plt.show()


# If you followed the use of the `.hist()` and `.show()` functions exactly like in the example, you're probably looking at a plot that's completely unexpected. The plot consists of one extremely tall bar on the left, maybe a very short second bar, and a whole lot of empty space in the center and right. Take a look at the duration values on the x-axis. This suggests that there are some highly infrequent outliers in the data. Instead of reprocessing the data, you will use additional parameters with the `.hist()` function to limit the range of data that is plotted. Documentation for the function can be found [[here]](https://matplotlib.org/devdocs/api/_as_gen/matplotlib.pyplot.hist.html#matplotlib.pyplot.hist).
# 
# **Question 5**: Use the parameters of the `.hist()` function to plot the distribution of trip times for the Subscribers in your selected city. Do the same thing for only the Customers. Add limits to the plots so that only trips of duration less than 75 minutes are plotted. As a bonus, set the plots up so that bars are in five-minute wide intervals. For each group, where is the peak of each distribution? How would you describe the shape of each distribution?
# 
# **Answer**: Replace this text with your response!

# In[29]:


## Use this and additional cells to answer Question 5. ##
import matplotlib.pyplot as plt
import csv
get_ipython().run_line_magic('matplotlib', 'inline')

def get_ride_time_date(filename):
    """
    This function reads in a file with trip data and reports the number of
    trips made by subscribers, customers, and total overall.
    """
    with open(filename, 'r') as f_in:
        # set up csv reader object
        reader = csv.DictReader(f_in)
        
        customer_data = []
        substriber_data = []
        
        for row in reader:
            if row['user_type'] == 'Subscriber':
                substriber_data.append(float(row['duration']))
            else:
                customer_data.append(float(row['duration']))
                
        return (substriber_data, customer_data)
    
summary_file = './data/Chicago-2016-Summary.csv'
bins =[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75]

subscriber_data = get_ride_time_date(summary_file)[0]
plt.hist(subscriber_data,bins,histtype='bar',rwidth=0.8)
plt.title('Distribution of Chicago Subscriber Trip Durations')
plt.xlabel('Duration (m)')
plt.legend()
plt.show()

customer_data = get_ride_time_date(summary_file)[1]
plt.hist(customer_data,bins,histtype='bar',rwidth=0.8)
plt.title('Distribution of Chicago Customer Trip Durations')
plt.xlabel('Duration (m)')
plt.legend()
plt.show()


# <a id='eda_continued'></a>
# ## Performing Your Own Analysis
# 
# So far, you've performed an initial exploration into the data available. You have compared the relative volume of trips made between three U.S. cities and the ratio of trips made by Subscribers and Customers. For one of these cities, you have investigated differences between Subscribers and Customers in terms of how long a typical trip lasts. Now it is your turn to continue the exploration in a direction that you choose. Here are a few suggestions for questions to explore:
# 
# - How does ridership differ by month or season? Which month / season has the highest ridership? Does the ratio of Subscriber trips to Customer trips change depending on the month or season?
# - Is the pattern of ridership different on the weekends versus weekdays? On what days are Subscribers most likely to use the system? What about Customers? Does the average duration of rides change depending on the day of the week?
# - During what time of day is the system used the most? Is there a difference in usage patterns for Subscribers and Customers?
# 
# If any of the questions you posed in your answer to question 1 align with the bullet points above, this is a good opportunity to investigate one of them. As part of your investigation, you will need to create a visualization. If you want to create something other than a histogram, then you might want to consult the [Pyplot documentation](https://matplotlib.org/devdocs/api/pyplot_summary.html). In particular, if you are plotting values across a categorical variable (e.g. city, user type), a bar chart will be useful. The [documentation page for `.bar()`](https://matplotlib.org/devdocs/api/_as_gen/matplotlib.pyplot.bar.html#matplotlib.pyplot.bar) includes links at the bottom of the page with examples for you to build off of for your own use.
# 
# **Question 6**: Continue the investigation by exploring another question that could be answered by the data available. Document the question you want to explore below. Your investigation should involve at least two variables and should compare at least two groups. You should also use at least one visualization as part of your explorations.
# 
# Q1: Explore the ridership in all seasons and get the numbers for season with highest ridership.
# 
# Q2: Which season has the ratio of Subscriber trips to Customer trips? Give a visualisation of the same.
# 
# **Answer**: 
# 
# Answer1: Chicago ridership is highest in Summer, which is 29890, and in Summer subscriber ridership is highest, which is 21198.
# 
# Answer2: Chicago has highest subscriber to customer trips ratio in Summer compared to others.

# In[30]:



import csv
import matplotlib.pyplot as plt

def condense_season_data(city_data):
  
    with open(city_data, 'r') as f_in:
        # set up csv reader object
        reader = csv.DictReader(f_in)
         # Define the variable for each days
        winter =[12,1,2]
        spring =[3,4,5]
        summer =[6,7,8]
        fall = [9,10,11]
        
        n_winter_subscriber = 0
        n_spring_subscriber = 0
        n_summer_subscriber = 0
        n_fall_subscriber = 0
        
        n_winter_customer = 0
        n_spring_customer = 0
        n_summer_customer = 0
        n_fall_customer = 0
        
        #convert the data 
        for row in reader:
            if row['user_type'] == 'Subscriber':
                if  int(row['month']) in  winter:
                    n_winter_subscriber += 1
                elif int(row['month']) in  spring:
                    n_spring_subscriber += 1
                elif int(row['month']) in  summer:
                    n_summer_subscriber += 1
                else:
                    n_fall_subscriber += 1
            else: 
                if  int(row['month']) in  winter:
                    n_winter_customer += 1
                elif int(row['month']) in  spring:
                    n_spring_customer += 1
                elif int(row['month']) in  summer:
                    n_summer_customer += 1
                else:
                    n_fall_customer += 1
        
        ratio_winter = n_winter_subscriber / n_winter_customer
        ratio_spring = n_spring_subscriber / n_spring_customer
        ratio_summer = n_summer_subscriber / n_summer_customer
        ratio_fall = n_fall_subscriber / n_fall_customer
        
        n_winter = n_winter_subscriber + n_winter_customer
        n_spring = n_spring_subscriber + n_spring_customer
        n_summer = n_summer_subscriber + n_summer_customer
        n_fall = n_fall_subscriber + n_fall_customer
        
        subscriber_season ={"Winter": n_winter_subscriber,"Spring": n_spring_subscriber,"Summer": n_summer_subscriber, "Fall":n_fall_subscriber}
        customer_season = {"Winter": n_winter_customer,"Spring": n_spring_customer,'Summer': n_summer_customer,'Fall': n_fall_customer} 
        ratio = {"Winter":ratio_winter,"Spring":ratio_spring,'Summer': ratio_summer,'Fall':ratio_fall}
        n = {"Winter":n_winter,"Spring":n_spring,'Summer': n_summer,'Fall':n_fall}
        #return dictionaries
        return subscriber_season,customer_season, ratio, n


subscriber_season1, customer_season1, ratio1,n1 = condense_season_data('./data/Chicago-2016-Summary.csv')
max1 =max(n1, key=n1.get) 
maximum1 = max(subscriber_season1, key=subscriber_season1.get)  
print("Chicago ridership is highest in {}, which is {}, and in {} subscriber ridership is highest, which is {}."
      .format(max1, n1[max1],maximum1, subscriber_season1[maximum1]))

# Subscriber to Customer Ratio
x = [ k for k in ratio1]
y = [v for v in ratio1.values()]
plt.bar(x,y,  alpha=0.5, label ='Ratio')
plt.title('Ratio of Subscriber trips to Customer trips')
plt.legend()
plt.show()

# Ridership bar charts of subscribers and customers
x1 =  [ k for k in subscriber_season1 ]
y1 = [v for v in subscriber_season1.values()]
x_pos = np.arange(len(x1))

x2 = [ k for k in customer_season1]
y2 = [v for v in customer_season1.values()]
x2_pos = np.arange(len(x2))

plt.bar(x1, y1, alpha=0.5, label ='Subscriber', color = 'c')
plt.bar(x2, y2, alpha=0.5, label ='Customer', color ='r')

plt.title('Ridership bar charts of subscribers and customers')
plt.xlabel('Seasons')
plt.ylabel('Number of Trips')
plt.legend()
plt.show()


# <a id='conclusions'></a>
# ## Conclusions
# 
# Congratulations on completing the project! This is only a sampling of the data analysis process: from generating questions, wrangling the data, and to exploring the data. Normally, at this point in the data analysis process, you might want to draw conclusions about the data by performing a statistical test or fitting the data to a model for making predictions. There are also a lot of potential analyses that could be performed on the data which are not possible with only the data provided. For example, detailed location data has not been investigated. Where are the most commonly used docks? What are the most common routes? As another example, weather has potential to have a large impact on daily ridership. How much is ridership impacted when there is rain or snow? Are subscribers or customers affected more by changes in weather?
# 
# **Question 7**: Putting the bike share data aside, think of a topic or field of interest where you would like to be able to apply the techniques of data science. What would you like to be able to learn from your chosen subject?
# 
# **Answer**: I would like to analyze car-pool/sharing data apply data-science techniques on it. I would like to learn which area of the city has more car pool users and what time of the day.
# 
# > **Tip**: If we want to share the results of our analysis with others, we aren't limited to giving them a copy of the jupyter Notebook (.ipynb) file. We can also export the Notebook output in a form that can be opened even for those without Python installed. From the **File** menu in the upper left, go to the **Download as** submenu. You can then choose a different format that can be viewed more generally, such as HTML (.html) or
# PDF (.pdf). You may need additional packages or software to perform these exports.
# 
# > If you are working on this project via the Project Notebook page in the classroom, you can also submit this project directly from the workspace. **Before you do that**, you should save an HTML copy of the completed project to the workspace by running the code cell below. If it worked correctly, the output code should be a 0, and if you click on the jupyter icon in the upper left, you should see your .html document in the workspace directory. Alternatively, you can download the .html copy of your report following the steps in the previous paragraph, then _upload_ the report to the directory (by clicking the jupyter icon).
# 
# > Either way, once you've gotten the .html report in your workspace, you can complete your submission by clicking on the "Submit Project" button to the lower-right hand side of the workspace.

# In[10]:


from subprocess import call
call(['python', '-m', 'nbconvert', 'Bike_Share_Analysis.ipynb'])

