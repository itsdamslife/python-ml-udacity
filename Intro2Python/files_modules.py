def hours2days(hours):
    days = hours // 24
    hrs = hours % 24
    return (days, hrs)


print(hours2days(24))
print(hours2days(25))
print(hours2days(10000))


def print_list(l, numbered=True, bullet_character='-'):
    """Prints a list on multiple lines, with numbers or bullets
    
    Arguments:
    l: The list to print
    numbered: set to True to print a numbered list
    bullet_character: The symbol placed before each list element. This is
                      ignored if numbered is True.
    """
    for index, element in enumerate(l):
        if numbered:
            print("{}: {}".format(index + 1, element))
        else:
            print("{} {}".format(bullet_character, element))


print_list(["one", "two", "three"], False, '=')


def buy_eggs(count):
    return count + 12  # purchase a dozen eggs

egg_count = 0
egg_count = buy_eggs(12)
print(egg_count)


def create_cast_list(filename):
    cast_list = []
    #use with to open the file filename
    with open(filename, 'r') as cast:
        #use the for loop syntax to process each line
        for line in cast:
            #and add the actor name to cast_list
            cast_list.append(line.split(',')[0])

    return cast_list
print(create_cast_list("flying_circus_cast.txt"))

import math
print(math.exp(3))

# Python module of the week :: https://pymotw.com/3/

#STANDARD LIBRARY IMPORTS

# Use an import statement at the top
import random

word_file = "words.txt"
word_list = []

#fill up the word_list
with open(word_file, 'r') as words:
    for line in words:
        # remove white space and make everything lowercase
        word = line.strip().lower()
        # don't include words that are too long or too short
        if 3 < len(word) < 8:
            word_list.append(word)


# Add your function generate_password here
# It should return a string consisting of three random words
# concatenated together without spaces
def generate_password():
    w1 = random.choice(word_list)
    w2 = random.choice(word_list)
    w3 = random.choice(word_list)
    pswd = w1 + w2 + w3
    return pswd  # CAN ALSO BE WRITTEN AS  str().join(random.sample(word_list,3))


# test your function
print(generate_password())

# requirements.txt
#     beautifulsoup4==4.5.1
#     bs4==0.0.1
#     pytz==2016.7
#     requests==2.11.1
# USE --> pip3 install -r requirements.txt
