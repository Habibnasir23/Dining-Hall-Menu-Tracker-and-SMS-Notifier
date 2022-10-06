# Author: Habib Nasir

# importing relevant libraries
import requests, bs4, os
from twilio.rest import Client
import time, datetime

try:  # try block to catch any exceptions while loading the page
    '''
    This function is used to scrape the website and form a list with the menu items for the day. 
    The list is passed to appropriate functions during specific times of the day. 
    Returns the new id.
    '''
    def getMenu():
        print("Starting...")
        # url of the website to scrape
        url = 'https://menus.sodexomyway.com/BiteMenu/Menu?menuId=14928&locationId=94118004&whereami' \
              '=https://truman.sodexomyway.com/dining-near-me/ryle-dining-hall'

        # use the get method to scrape the website
        res = requests.get(url)
        # checking if the scraping was successful
        res.raise_for_status()
        # parsing the html content
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        # getting the elements with the specific id
        item = soup.select(make_url_id())
        menu_item = item[0].getText()
        print(len(menu_item))
        newItem = " "  # initializing a string variable to be used to store the value of items
        demoArr = []  # an empty list to store the menu

        # separating all menu items and adding them to the list variable
        for i in range(21, len(menu_item)):
            if menu_item[i] != '\n':
                newItem = newItem + menu_item[i]
            else:
                demoArr.append(newItem)
                newItem = " "

        print(len(demoArr))
        # removing whitespaces from the string
        while ' ' in demoArr:
            demoArr.remove(' ')

        for elem in demoArr:
            print(elem)

        # if the program is run between 12 am and 9 am, the program will check the breakfast menu
        if 0 <= check_hour() <= 8:
            breakfast_menu = breakfast(demoArr)
            print(breakfast_menu)
            temp_list = check_menu(breakfast_menu)
            form_message(temp_list, breakfast_menu)

        # if the program is run between 9 am and 2 pm, the program will check the lunch menu
        elif 9 <= check_hour() <= 13:
            lunch_menu = lunch(demoArr)
            print(lunch_menu)
            temp_list = check_menu(lunch_menu)
            form_message(temp_list, lunch_menu)

        # if the program is run between 2 pm and 8 pm, the program will check the dinner menu
        elif 14 <= check_hour() <= 19:
            dinner_menu = dinner(demoArr)
            print(dinner_menu)
            temp_list = check_menu(dinner_menu)
            form_message(temp_list, dinner_menu)

# exception block to catch any exception related to page not loading
except Exception as exc:
    print('There was a problem loading the page..')

'''
This function is used to a unique id of the url for everyday.
Returns the new id.
'''


def make_url_id():
    dt = datetime.datetime.now()  # getting the datetime object for today
    link_id = '#menuid-' + str(dt.day) + '-day'  # concatenating the strings to make a unique id
    return link_id


'''
This function is used to create a list that contains the menu for breakfast.
It takes the full menu list as the parameter.
Returns the new breakfast list.
'''


def breakfast(full_menu):
    bf_list = []  # an empty list to store breakfast menu
    for elem in full_menu:  # loops through the entire list until stopping condition is met
        if elem != ' LUNCH':  # stops when encounters the 'LUNCH' keyword
            bf_list.append(elem.strip())
        else:
            break
    return bf_list


'''
This function is used to create a list that contains the menu for lunch.
It takes the full menu list as the parameter.
Returns the new lunch list.
'''


def lunch(full_menu):
    lunch_list = []  # an empty list to store lunch menu
    for i in range(len(full_menu)):  # loops through the full menu until stopping condition is met
        if full_menu[i] == ' LUNCH':
            j = i  # index for the lunch list
            while full_menu[j] != ' DINNER':  # loop ends if the value ' DINNER' is encountered
                # using strip function to get rid of whitespaces in the string
                # appending the new string to the lunch list
                lunch_list.append(full_menu[j].strip())
                j += 1
            break
    return lunch_list


'''
This function is used to create a list that contains the menu for dinner.
It takes the full menu list as the parameter.
Returns the new dinner list.
'''


def dinner(full_menu):
    dinner_list = []  # an empty list to store lunch menu

    for i in range(len(full_menu)):  # loops through the full menu until stopping condition is met
        if full_menu[i] == ' DINNER':
            j = i  # to index through the full menu when the value ' DINNER' is encountered

            while j < len(full_menu):  # loop stops when the end of full menu is reached

                # using strip function to get rid of whitespaces in the string
                # appending the new string to the lunch list
                dinner_list.append(full_menu[j].strip())
                j += 1
            break
    return dinner_list


'''
This function is used to extract the current hour of the day and return it's value.
'''


def check_hour():
    dt = datetime.datetime.now()
    return dt.hour


'''
This function is used to compare a menu list with the person's desired items list.
It takes a menu list as the parameter.
Converts the lists into sets
Returns the intersection of menu set and desired items set. 
'''


def check_menu(menu):
    # list of items I would prefer in the menu
    desired_items = ['Blackened Cajun Chicken Breast', 'Jerk Chicken Thigh', 'Chicken Fried Rice', 'Breaded Fish '
                     'Sandwich', 'Buffalo Chicken Quesadilla', 'Grilled Jerk Chicken Breast', 'Bbq Chicken Breast',
                     'Baked Chicken Fried Steak', 'Chicken Patty Sandwich']

    # converting the menu list to a set
    # using the intersection method to find common items in menu and desired_items
    result_items = list(set(menu).intersection(desired_items))
    return result_items


'''
This function is used to form appropriate messages based on the menu and pass them to send_message function
It takes two parameters, result_list and specific_menu list.
result_list contains the list returned from the check_menu function
specific_menu list contains 
'''


def form_message(result_list, specific_menu):
    # a string that contains the message when menu has none of the desired items
    message0 = 'Man the menu sucks today, you should consider eating at the sub. Check it out yourself: '
    # a string that contains the message when menu has 1 desired item.
    message1 = 'There are not many options for you to eat today.'
    # a string that contains the message when menu has 2 or more of the desired items.
    message2 = 'The menu looks good today!'
    # a string that contains the message about desired items in the menu
    message3 = 'Your favorite items in today\'s menu are: '
    # a string that contains the message about the whole menu
    message4 = 'This is the whole menu: '

    # condition to send appropriate message when none of the desired items are on the menu
    if len(result_list) == 0:
        send_message(message0)
        msg = " "

        for elem0 in specific_menu:
            msg = msg + elem0 + ", "

        send_message(msg)
        time.sleep(1)  # to pause for 1 second before sending another message

    # condition to send appropriate message when one of the desired items are on the menu
    if len(result_list) == 1:
        send_message(message1)
        print(message1)

        for elem in result_list:
            message3 = message3 + " " + elem + '\n'

        send_message(message3)
        print(message3)
        time.sleep(1)

        # sending the whole menu to the recipient
        for elem2 in specific_menu:
            message4 = message4 + " " + elem2 + '\n'

        send_message(message4)
        print(message4)

    # condition to send appropriate message when two or more of the desired items are on the menu
    if len(result_list) >= 2:
        send_message(message2)

        for elem in result_list:
            message3 = message3 + " " + elem + '\n'

        send_message(message3)
        time.sleep(1)


'''
This function is used to send messages to the recipient
It takes a string as a parameter that contains the message to be sent
'''


def send_message(msg):
    # account id to verify the recipient
    account_sid = 'AC18f96f58161d0d98e2d8a98771c8567f'
    # authentication token to verify the recipient
    auth_token = 'aceadcacd827d3329d2ff8f2f5f8834a'
    # recipients real number
    my_number = '+14753321424'
    # recipient's twilio number
    twilio_number = '+19705095797'
    # accessing the recipient using ID and token
    twilioCli = Client(account_sid, auth_token)
    # sending the message to the recipient
    twilioCli.messages.create(body=msg, from_=twilio_number, to=my_number)

getMenu()