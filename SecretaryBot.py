# Standard modules
import random
import time
import os
import json

# SBot modules
import calculator
import users
import notes

# Defines possible opening lines
greetings = ["Well hi there, {user}.", "Hi, {user}!", "{user}. Welcome.", "A pleasure to see you again, {user}.",
             "HOW DARE YOU I HAVE A KNIFE--Oh wait it's just you. *Ahem*", "ALL HAIL THE MIGHTY HELIX.",
             "Hey hey!", "Well hello there, handsome.", "Oh, hey {user}. You know you, uh, got a thing on your--never mind.",
             "Oh! Just a moment {user}, let me just finish getting this...ah, that's much better."]
prompts = ["What can I do for you?", "What's up?", "What'll it be today?", "What'll it be this time?",
           "Can I help you?", "What now?", "You'll be wanting the massage about now, I expect.",
           "I'm afraid Barry is calling me back into the office, but how can I help?"]

# Command error feedback, the {cmd} fields get replaced with the triggering command via str.format()
command_errors = ["Man I wish I knew how to process {cmd}, but I'm pretty dumb right now. \n\
Try again? Or you could ask for HELP.",
                  "Mm...no. {cmd} doesn't make any sense to me. You sure you don't need any HELP?",
                  "FATAL ERROR.\n\n\
No really, I punched in {cmd} like you told me to and that's what I got.\
Don't bother checking the manual, it just has a picture of the command prompt with the word HELP typed in. Useless."]
# Other stuff
days_of_the_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
main_menu = """
Main Menu:
CALCULATOR    NOTES    USERS
"""
main_menu_help = """\
You new here, love? Don't sweat it, we were all there once.
All you need to know is that all commands are in lowercase, and each module
is called by name. When you're done just QUIT out.

You can always see this message again by typing HELP on the main menu (remember
all commands are lowercase), and every other page has its own HELP information."""
                

# Methods for convenience and elegance
def choose_from(stuff):
    """Simple function for semi-randomizing text responses from a set list (defined above)."""
    return random.choice(stuff)

def get_time_of_day():
    """Returns time in the form of 'Monday afternoon', or 'Thursday morning'"""
    current_time = time.localtime()
    day = days_of_the_week[current_time.tm_wday]
    # note that system time is 24h clock
    hour = current_time.tm_hour
    # translate to morning/afternoon/evening/night/early morning
    if hour >= 6 and hour < 12:
        the_time = " morning"
    elif hour >= 12 and hour < 18:
        the_time = " afternoon"
    elif hour >= 18 and hour < 20:
        the_time = " evening"
    elif hour >= 20:
        the_time = " night"
    else:
        the_time = "early "
        return the_time + day
    return day + the_time

# Method used for on the spot testing, invoked by "test" at main menu
def test():
    #output = "The test function isn't set to anything at the moment."
    test_new_user = users.create_new_user("Test User", module_index)
    
    return test_new_user[1] + " User list: " + str(user_list)


# Initialize with opening greeting and active user
def init():
    """Sets the opening greeting, loads user profiles."""
    global run, output, user_list, active_user
    
    # Locate user profiles
    user_list = []
    for file in os.listdir(os.curdir):
        if file.endswith(".txt"):
            user_list.append(file)

    number_of_users = len(user_list)
    
    # If no profile present, prompt for profile creation
    if number_of_users == 0:
        print """SBot welcomes you. To begin, please choose a username.
Names are case-sensitive and can be changed later."""
        new_user_name = raw_input('Name> ')
        user_creation = users.create_new_user(new_user_name)
        active_user = user_creation[0]
        print user_creation[1], "\n"
        time.sleep(2)
        print main_menu_help
        time.sleep(3)
        output = main_menu
        run = True
        return 1

    # If there is exactly one user profile, load it
    elif number_of_users == 1:
        active_user = users.init_user(user_list[0])
        print "User profile loaded: " + active_user.name
        time.sleep(0.5)

    # If mutiple profiles, prompt selection
    elif number_of_users > 1:
        print "Multiple profiles found. Who are you?"
        # Print the list of user files, excluding .txt
        for user in user_list:
            print user_list.index(user) + 1, user[:-3]
        selection = input('Choose a number> ') - 1
        active_user = users.init_user(user_list[selection])

        print "User profile loaded: " + active_user.name
        time.sleep(0.5)
        
    else:
        print "ERROR LOADING USER PROFILES"
    
    print '\n' + choose_from(greetings).format(user=active_user.name) + " It's " + \
         get_time_of_day() + ". " + choose_from(prompts)
    
    time.sleep(1.0)
    
    output = main_menu
    run = True


# Main menu commands
def SBot_quit():
    global run
    print "Bye bye!"
    time.sleep(1)
    run = False
def SBot_help():
    global output
    output = main_menu_help
def restart():
    print "Resetting memory banks..."
    time.sleep(0.5)
    init()
def run_module(module, *args):
    global output
    print "\n"
    result = module(*args)
    print "\n", "Returning to the main menu..."
    time.sleep(0.75)
    output = main_menu
    return result
def calc_module():
    run_module(calculator.calculator)
def user_management():
    global output
    requires_restart = run_module(users.user_management, active_user)
    if requires_restart:
        print "You've made some changes to your profile. Restarting SBot..."
        time.sleep(2)
        print "\n"
        init()
def notes_module():
    run_module(notes.notes, active_user)
    
menu_options = {'quit': SBot_quit,
                'help': SBot_help,
                'restart': restart,
                'calc': calc_module,
                'calculator': calc_module,
                'users': user_management,
                'notes': notes_module}


### BEGIN PROGRAM ###
    
init()

# Main menu
while run:
    print output
    command = raw_input("MENU> ")

    # Command interpretation
    if command in menu_options:
        menu_options[command]()

    # If command fails due to casing, give feedback
    elif command.isalpha():
        if command.istitle():
            output = "Sorry love, it's casuals only in here. Use lowercase commands next time."
            continue
        elif command.isupper():
            output = "That other guy give you wrong directions again? See, ya gotta keep \
your commands lowercase."
            continue
        else:
            output = choose_from(command_errors).format(cmd = "\"" + command + "\"")
    # Else give standard error
    else:
        output = choose_from(command_errors).format(cmd = "\"" + command + "\"")
        
