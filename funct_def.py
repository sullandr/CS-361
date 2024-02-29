from class_def import *

import os
import datetime
import requests

def home_screen(member=None):
    """main menu of program, has two modes, regular menu or member menu. logging into an account will bring up the member menu, otherwise loads
        the regular menu.
    Args:
        member (class object, optional): loads a member into the menu if logged in. Defaults to None.

    Returns:
        if not logged in, can log in to an account, create a new account, input an unsaveable entry, or exit
        if logged in, can make a new entry, print all entries, print one entry at a time, delete all entries, log out and go back to menu, or
        just exit
    """
    os.system('cls')
    if member == None: #display for not being logged in
        print('Pool Table Practice Log')
        print('WELCOME!')
        print('Input a selection from the options below:')
        print("'1' Log in to an existing account (saves log entries & stores basic personal information.")
        print("'2' Create a new account with a unique username (an account is required for saving log entries. This only takes a few moments.)")
        print("'3' Type an entry without logging in (Member log in required to save log entry.)")
        print("'4' Exit")
        print('*** Any invalid entry will reload the current page ***\n\n\n')
        print("'5' BONUS (generates a random city and state in json format and prints it)")
        while True: #endless loop waiting for valid input
            choice = int(input('Input your selection here: '))
            if choice == 1: #if they choose 1, go to log in page
                return log_in_screen()
            elif choice == 2: #if the choose 2, load create_account screen
                return create_account()
            elif choice == 3: #if they choose 3, load journal_entry screen.
                return journal_entry()
            elif choice == 4: #if they choose 4, exit program without saving anything, close all connections, etc.
                return
            elif choice == 5:#if they choose 5, make get request to the server and print the result
                micro_server = 'http://127.0.0.1:5000/cities'
                response = requests.get(micro_server)
                code = response.json()
                print(code)
                input("Press any key to return to the main menu")
                return home_screen()
            else:
                return home_screen()
    else: #display if member logged in
        os.system('cls')
        print('Pool Table Practice Log')
        print('WELCOME {0}!'.format(member.username))
        print('Input a selection from the options below:')
        print("'1' Add a new entry.")
        print("'2' Show all previous entries at once.")
        print("'3' Show all entries one at a time.")
        print("'4' Delete all entries. (This cannot be undone.)")
        print("'5' Log out and return to the main menu.")
        print("'6' Log out and exit")
        print('*** Any invalid entry will reload the current page ***\n\n\n')
        while True: #endless loop waiting for valid entry
            choice = int(input('Input your selection here: '))
            if choice == 1: #if they choose 1, go to journal_entry page
                return journal_entry(member)
            elif choice == 2: #if the choose 2, load print_all_entries screen
                return print_all_entries(member)
            elif choice == 3: #if they choose 3, load print_one_at_a_time screen.
                return print_one_at_a_time(member)
            elif choice == 4: #if they choose 4, run delete_all
                return delete_all(member)
            elif choice == 5:
                return home_screen()
            elif choice == 6:
                return 0
            else:
                return home_screen(member)

def create_account():
    """creates a new member account, checks username input against list of usernames, only accepts a username that is unique, then accepts a 
       password to go along with it and write them into the users text file.

    Returns:
        unless they return to the main menu or quit, will not leave this screen unless they successfully create a new account. then will return
        to main menu
    """
    os.system('cls') #clear the screen so it gives appearance of loading new screen.
    with open("users.txt", "r+") as logins:
        print("Let's create a new account!")
        username = input("Create a unique username: ")
        line = logins.readline()
        while line:
            user_info = line.split()
            user = Users(user_info[0],user_info[1])
            if user.username == username:
                key = input("This username already exists! Press any key to try again, 'm' to return to the main menu, or 'q' to quit. ")
                if key == 'm':
                    logins.close()
                    return home_screen()
                elif key == 'q':
                    logins.close()
                    return
                else:
                    logins.close()
                    return create_account()
            else:
                line = logins.readline()
        password = input("Now create a password: ")
        new_user = Users(username, password)
        input_string = new_user.username + " " + new_user.password
        logins.close()
    with open("users.txt", "a+") as logins:
        logins.write(input_string)
        logins.write("\n")
    return home_screen(new_user)

def log_in_screen():
    """log in screen allows a user to input a username and password to log in to their account, if the user list is empty, will send them to 
       create a new account, won't accept invalid credentials.

    Returns:
        if there is an empty user list, returns them to account creation. otherwise sits in a loop until valid credentials have been entered,
        then will load member home screen
    """
    os.system('cls') #clear the screen so it gives appearance of loading new screen.
    try:
        with open("users.txt", 'r') as logins:    
            username = input("Please input your username: ")
            line = logins.readline()
            while line:
                user_info = line.split()
                user = Users(user_info[0],user_info[1])
                if user.username == username:
                    password = input("Please input your password: ")
                    if user.password == password:
                        logins.close()
                        return home_screen(user)
                    else:
                        key = input("Invalid password, press any key to input credentials again, 'm' to return to main menu, 'q' to quit: ")
                        if key == 'm':
                            logins.close()
                            return home_screen()
                        elif key == 'q':
                            logins.close()
                            return
                        else:
                            logins.close()
                            return log_in_screen()
                else:
                    line = logins.readline()
        key = input("Invalid username, to try again press any key, to return to main menu press 'm', to quit press 'q': ")
        if key == 'm':
            return home_screen()
        elif key == 'q':
            return
        else:
            return log_in_screen()
    except:
        print("There are no users yet, you must create a new account first.")
        return create_account()          

def journal_entry(member=None):
    """allows a user to input journal entries based on responses to prompts. only a logged in member can save the entry, otherwise it only gets
       printed, then deleted.

    Args:
        member (class object, optional): if a member is logged in. Defaults to None.

    Returns:
        if not logged in, will print out the journal entry to view once completed, then will delete it and return to the main menu or quit.
        if logged in, will still print out the journal entry, but will prompt to save the entry or delete it and return to the menu.
    """
    os.system('cls') #clear screen to give appearance of laoding new screen
    if member == None: #non member journal entry
        print("Let's create a new journal entry!")
        print("The date and time will automatically be attached to the entry.")
        print("Please use '_' in place of ' '.")
        table_type = input("What type of table did you play on? ")
        racks = input("How many racks did you play? ")
        ballcount = input("What is the ballcount of balls made this practice session? ")
        practice_type = input("What type of practice did you do? (i.e drills or regular) ")
        current = str(datetime.datetime.now())
        date_time = current.split()
        entry = Entries(date_time[0], date_time[1], table_type, racks, ballcount, practice_type)
        os.system('cls')
        print("Below is your journal entry:")
        print("Date of practice: {0}".format(entry.date))
        print("Time of practice: {0}".format(entry.time))
        print("Type of table played on: {0}".format(entry.table_type))
        print("Number of racks played: {0}".format(entry.racks))
        print("Number of balls made: {0}".format(entry.ballcount))
        print("Type of practice completed: {0}".format(entry.practice_type))
        key = input("To save future log entries, create an account.")
        return home_screen()
    else: #member journal entry
        print("Let's create a new journal entry!")
        print("The date and time will automatically be attached to the entry.")
        print("Please use '_' in place of ' '.")
        table_type = input("What type of table did you play on? ")
        racks = input("How many racks did you play? ")
        ballcount = input("What is the ballcount of balls made this practice session? ")
        practice_type = input("What type of practice did you do? (i.e drills or regular) ")
        current = str(datetime.datetime.now())
        date_time = current.split()
        entry = Entries(date_time[0], date_time[1], table_type, racks, ballcount, practice_type)
        entry_input = str(entry.date) + " " + str(entry.time) + " " + entry.table_type + " " + entry.racks + " " 
        entry_input = entry_input + entry.ballcount + " " + entry.practice_type #creates entry input in preparation for saving it
        os.system('cls') #clear screen for appearance of fresh screen
        print("Below is your journal entry:")
        print("Date of practice: {0}".format(entry.date))
        print("Time of practice: {0}".format(entry.time))
        print("Type of table played on: {0}".format(entry.table_type))
        print("Number of racks played: {0}".format(entry.racks))
        print("Number of balls made: {0}".format(entry.ballcount))
        print("Type of practice completed: {0}".format(entry.practice_type))
        key = input("Press any key to save this entry and return to the menu. ")
        filename = member.username + ".txt"
        with open(filename, 'a+') as entries:
            entries.write(entry_input)
            entries.write("\n")
            entries.close()
            key = input("Entry saved, press any key to return to the menu. ")
        return home_screen(member)

def print_all_entries(member):
    """prints all journal entries for the member at one time

    Args:
        member (class object): this allows the logged in member to retrieve their journal entries from their file

    Returns:
        returns a printed list of all entries, numbered.
    """
    filename = member.username + ".txt"
    with open(filename, 'r+') as logins:    
        line = logins.readline()
        if len(line) == 0:
            key = input("No previous entries, press any key to return to menu. ")
            logins.close()
            return home_screen(member)
        else:
            i = 1
            while line:
                entry_info = line.split()
                entry = Entries(entry_info[0], entry_info[1], entry_info[2], entry_info[3], entry_info[4], entry_info[5])
                print("Entry {0}: ".format(i))
                print("Date of practice: {0}".format(entry.date))
                print("Time of practice: {0}".format(entry.time))
                print("Type of table played on: {0}".format(entry.table_type))
                print("Number of racks played: {0}".format(entry.racks))
                print("Number of balls made: {0}".format(entry.ballcount))
                print("Type of practice completed: {0}".format(entry.practice_type))
                i += 1
                line = logins.readline()
            key = input("All entries have been printed, press any key to return to the homescreen. ")
            logins.close()
            return home_screen(member)

def print_one_at_a_time(member):
    """prints one entry at a time, can return to menu or quit at any time.

    Args:
        member (class object): allows a logged in member to retrieve the entries from their own file

    Returns:
        displays one entry at a time, will either return to menu or quit depending on input
    """
    filename = member.username + ".txt"
    with open(filename, 'r+') as logins:    
        line = logins.readline()
        if len(line) == 0:
            key = input("No previous entries, press any key to return to menu. ")
            logins.close()
            return home_screen(member)
        else:
            i = 1
            while line:
                entry_info = line.split()
                entry = Entries(entry_info[0], entry_info[1], entry_info[2], entry_info[3], entry_info[4], entry_info[5])
                print("Entry {0}: ".format(i))
                print("Date of practice: {0}".format(entry.date))
                print("Time of practice: {0}".format(entry.time))
                print("Type of table played on: {0}".format(entry.table_type))
                print("Number of racks played: {0}".format(entry.racks))
                print("Number of balls made: {0}".format(entry.ballcount))
                print("Type of practice completed: {0}".format(entry.practice_type))
                i += 1
                line = logins.readline()
                key = input("Press 'm' to return to menu, 'q' to quit, or any key to continue. ")
                if key == 'm':
                    return home_screen(member)
                elif key == 'q':
                    return
                else:
                    continue
            key = input("All entries have been printed, press any key to return to the homescreen. ")
            logins.close()
            return home_screen(member)

def delete_all(member):
    """deletes all entries with a prompt for verification to avoid accidental deletion.

    Args:
        member (class object): allows a logged in member to delete all entries from their file

    Returns:
        with confirmation, deletes all entries and returns to menu, otherwise will just return to menu.
    """
    filename = member.username + ".txt"
    print("Are you sure you want to delete all entries? ")
    key = input("Press 'y' to confirm deleting all entries and return to menu, any other key will only return to menu. ")
    if key == 'y':
        with open(filename, 'w') as logins:
            logins.close()
        key = input("Log deleted, press any key to return to the menu. ")
        return home_screen(member)
    else:
        return home_screen(member)

if __name__ == "__main__":
    home_screen()