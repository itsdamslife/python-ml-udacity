# LISTS

def how_many_days(month_number):
    """Returns the number of days in a month.
    WARNING: This function doesn't account for leap years!
    """
    days_in_month = [31,28,31,30,31,30,31,31,30,31,30,31]

    month_index = month_number - 1

    return days_in_month[month_index]

# This test case should print 31, the number of days in the eighth month, August
print(how_many_days(8))

eclipse_dates = ['June 21, 2001', 'December 4, 2002', 'November 23, 2003',
                 'March 29, 2006', 'August 1, 2008', 'July 22, 2009',
                 'July 11, 2010', 'November 13, 2012', 'March 20, 2015',
                 'March 9, 2016']


# TODO: Modify this line so it prints the last three elements of the list
print(eclipse_dates[7:])

def top_three(input_list):
    """Returns a list of the three largest elements input_list in order from largest to smallest.

    If input_list has fewer than three elements, return input_list element sorted largest to smallest/
    """
    sortedList = sorted(input_list, reverse=True)
    return sortedList[:3]

print(top_three([2, 3, 5, 6, 8, 4, 2, 1]))
# [8, 6, 5]

print(top_three([1, 2]))
# [2, 1]

print(top_three(['cat', 'dog', 'python', 'cuttlefish']))
# ['python', 'dog', 'cuttlefish']

def median(numbers):
    numbers.sort() #The sort method sorts a list directly, rather than returning a new sorted list
    middle_index = int(len(numbers)/2)
    if len(numbers)%2 == 0:
        return ((numbers[middle_index] + numbers[middle_index-1])/2)
    else:
        return numbers[middle_index]

test1 = median([1,2,3])
print("expected result: 2, actual result: {}".format(test1))

test2 = median([1,2,3,4])
print("expected result: 2.5, actual result: {}".format(test2))

test3 = median([53, 12, 65, 7, 420, 317, 88])
print("expected result: 65, actual result: {}".format(test3))


# LOOPS

# ### for loop
def list_sum(input_list):
    sum = 0
    for input in input_list:
        sum += input
    return sum



#These test cases check that list_sum works correctly
test1 = list_sum([1, 2, 3])
print("expected result: 6, actual result: {}".format(test1))

test2 = list_sum([-1, 0, 1])
print("expected result: 0, actual result: {}".format(test2))



# """Write a function, `tag_count`, that takes as its argument a list
# of strings. It should return a count of how many of those strings
# are XML tags. You can tell if a string is an XML tag if it begins
# with a left angle bracket "<" and ends with a right angle bracket ">".
# """
# Define the tag_count function
def tag_count(list):
    count = 0
    for str in list:
        if str[0:1] == '<' and str[-1:] == '>':
            count += 1
    return count

# Test for the tag_count function:
list1 = ['<greeting>', 'Hello World!', '</greeting>']
count = tag_count(list1)
print("Expected result: 2, Actual result: {}".format(count))

#define the  html_list function
def html_list(list_of_strings):
    strLine = "<ul>\n"
    for listElement in list_of_strings:
        lineItem = "<li>{}</li>\n".format(listElement)
        strLine += lineItem
    strLine += "</ul>"
    return strLine

result = html_list(['First element', 'Second element', 'Third element'])
print(result)

def starbox(width, height):
    """print a box made up of asterisks.

    width: width of box in characters, must be at least 2
    height: height of box in lines, must be at least 2
    """
    print("*" * width) #print top edge of box

    # print sides of box
    for i in range(height-2):
        print("*" + " " * (width-2) + "*")

    print("*" * width) #print bottom edge of box

# Test Cases
print("Test 1:")
starbox(5, 5) # this prints correctly

print("Test 2:")
starbox(2, 3)  # this currently prints two lines too tall - fix it!

# ### while loop

# Implement the nearest_square function
def nearest_square(limit):
    answer = 0
    while (answer+1)**2 < limit:
        answer += 1
    return answer**2

test1 = nearest_square(35)
print("expected result: 36, actual result: {}".format(test1))

headlines = ["Local Bear Eaten by Man",
             "Legislature Announces New Laws",
             "Peasant Discovers Violence Inherent in System",
             "Cat Rescues Fireman Stuck in Tree",
             "Brave Knight Runs Away",
             "Papperbok Review: Totally Triffic"]

news_ticker = ""
num_of_characters = 0

for headline in headlines:
    news_ticker += headline + " "
    if len(news_ticker) >= 140:
        news_ticker = news_ticker[:140]
        break

print(news_ticker)
print(len(news_ticker))

# Refactoring code

def check_answer(my_answer, answer):
    if my_answer == answer:
        return True
    else:
        return False

def check_answers(my_answers,answers):
    # Checks the five answers provided to a multiple choice quiz
    # and returns the results.
    results = []
    for i in range(len(my_answers)):
        results.append(check_answer(my_answers[i], answers[i]))
    count_correct = 0

    for result in results:
        if result:
            count_correct += 1

    score_string = "You scored " + str(count_correct) + " out of 5."
    if count_correct/len(results) > 0.7:
        return "Congratulations, you passed the test! " + score_string
    elif (len(results) - count_correct)/len(results) >= 0.3:
        return "Unfortunately, you did not pass. " + score_string

# SETS

# Define the remove_duplicates function
def remove_duplicates(list):
    new_list = [list[0]]
    for e in list:
        if e not in new_list:
            new_list.append(e)
    return new_list

setList = remove_duplicates(['Angola', 'Maldives', 'India', 'United States', 'India'])
print(setList)

squares = set()
def nearest_squares(limit):
    answer = 1
    while (answer)**2 <= limit:
        squares.add(answer**2)
        answer += 1


nearest_squares(2000)
print(squares)

# DICTIONARIES

# Define a Dictionary, population,
# that provides information
# on the world's largest cities.
# The key is the name of a city
# (a string), and the associated
# value is its population in
# millions of people.

#   Key     |   Value
# Shanghai  |   17.8
# Istanbul  |   13.3
# Karachi   |   13.0
# Mumbai    |   12.5

population = {'Shanghai': 17.8, 'Istanbul': 13.3, 'Karachi': 13.0, 'Mumbai': 12.5}



from countries import country_list
# Note: since the list is so large, it's tidier
# to put in in a separate file. We'll learn more
# about "import" later on.

country_counts = {}
for country in country_list:
    # insert countries into the country_count dict.
    # If the country isn't in the dict already, add it and set the value to 1
    # If the country is in the dict, increment its value by one to keep count
    if country in country_counts: # if country_counts.get(country) is None:
        country_counts[country] += 1
    else:
        country_counts[country] = 1

print(country_counts)
