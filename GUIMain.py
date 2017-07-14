import tkinter
from tkinter import messagebox
import os
import UserData as User
import requests

main_window = tkinter.Tk()
setup_frame = tkinter.Frame(main_window)
character_change_frame = tkinter.Frame(main_window)

# this list must always have the same number of entries as 'user_data_file_structure' found in UserData.py
# this is mostly test code. later it will be improved so it's not so fragile and also make solutions more generic
# always in order:  account > character > league > poesessid > client.txt path
user_inputted_info = ['acc', 'char', 'league', 'poesessid', 'client.txt path']


def program_startup():
    """handles all the necessary checks and routines for startup"""

    # TODO: ADD THE ZONE TRACKER AND CHAOS COUNTER TO THE MAIN SCREEN ALSO A MENU TO ACCESS THE OTHER SCREENS WITH
    # check if the userdata.txt file is found if not make the user enter all necessary data
    if os.path.exists('userdata.txt'):
        # load user data first
        User.load_user_data()
        display_character_change()
        # display main screen here
    else:
        missing_user_file = 'userdata.txt not found. complete first time setup'
        display_message_box(missing_user_file, display_user_data_entry_fields)


def file_update(update_type='setup'):
    """this should be called to ensure that the user info is populated. call with 'push' to update instead of setup"""

    # check if userdata.txt exists and if not create it with the proper format
    if os.path.exists('userdata.txt') and update_type == 'setup':
        print('userdata.txt exists nothing further needed here')
    elif update_type == 'push':
        # the purpose of this case is to allow the function to be used as both a setup and to push updates to UserData
        with open('userdata.txt', 'w') as file:
            i = 0
            for item in User.user_data_file_structure:
                file.writelines(item.replace('%', user_inputted_info[i]) + '\n')
                i += 1
            file.close()
    else:
        with open('userdata.txt', 'w') as file:
            a = 0
            for item in User.user_data_file_structure:
                file.writelines(item.replace('%', user_inputted_info[a]) + '\n')
                a += 1
            file.close()
    User.load_user_data()


def display_user_data_entry_fields():
    """this displays all of the necessary fields and button for initial user data setup"""

    setup_frame.pack(fill='both')

    account_label = tkinter.Label(setup_frame, text='Account', justify='left')
    char_label = tkinter.Label(setup_frame, text='Character', justify='left')
    league_label = tkinter.Label(setup_frame, text='League', justify='left')
    poesessid_label = tkinter.Label(setup_frame, text='POESESSID', justify='left')
    path_label = tkinter.Label(setup_frame, text='Client.txt Path', justify='left')

    account_label.grid(pady=3, row=1)
    char_label.grid(pady=3, row=2)
    league_label.grid(pady=3, row=3)
    poesessid_label.grid(pady=3, row=4)
    path_label.grid(pady=3, row=5)

    account_entry = tkinter.Entry(setup_frame, bd=5)
    char_entry = tkinter.Entry(setup_frame, bd=5)
    league_entry = tkinter.Entry(setup_frame, bd=5)
    poesessid_entry = tkinter.Entry(setup_frame, bd=5)
    path_entry = tkinter.Entry(setup_frame, bd=5)

    account_entry.grid(column=1, row=1)
    char_entry.grid(column=1, row=2)
    league_entry.grid(column=1, row=3)
    poesessid_entry.grid(column=1, row=4)
    path_entry.grid(column=1, row=5)

    enter_data_button = tkinter.Button(setup_frame, text='Enter Data', command=store_data_callback)

    enter_data_button.grid(row=6)


def store_data_callback():
    """button press calls this and stores data in file for future use"""

    # iterate over all entry fields in setup_frame and put the data contained in them into user_inputted_info
    i = 0
    for child in setup_frame.children.values():
        if 'entry' in str(child):
            if len(child.get()) == 0:
                print('make sure data is entered into all fields')
                return
            else:
                user_inputted_info[i] = child.get()
                i += 1
    print(user_inputted_info)
    # after data is entered hide the setup frame
    setup_frame.grid_forget()
    setup_frame.destroy()
    file_update()


def display_message_box(message, callback=None):
    """this function displays a message box and waits for the user to hit ok. an optional callback is run afterwards"""

    messagebox.showinfo('', str(message))
    if callback is None:
        return
    else:
        callback()


def display_character_change():
    """displays characters and executes correct function to update character/league selection"""

    character_change_frame.pack(fill='both')

    character_list = tkinter.Listbox(character_change_frame, selectmode='single')

    for c in grab_characters_from_server():
        character_list.insert(tkinter.END, c['name'] + "-" + c['league'])

    character_list.select_set(0)

    character_list.pack(side='left', fill='both', expand=True)

    select_character = tkinter.Button(character_change_frame, text='Confirm', command=lambda: change_character_callback(
                                      character_list.get(character_list.curselection())))

    select_character.pack(side='bottom')


def grab_characters_from_server():
    """returns a dict of all characters:league on the account"""

    cookie = {'POESESSID': User.poesessid}
    param = {'account': User.account_name}

    # when the user updates character league has to be updated too so no reason to give the option to select league
    character_api_endpoint = 'https://www.pathofexile.com/character-window/get-characters'

    r = requests.get(character_api_endpoint, params=param, cookies=cookie)

    if r.status_code == 200:
        return r.json()
    else:
        error_message = 'Something went wrong. Check your POESESSID and try again. Status code: ' + str(r.status_code)
        display_message_box(error_message)


def change_character_callback(selection):
    """this callback function is passed data from the character list and makes that the current character"""

    # the argument is passed as a string grabbed from teh listbox so it needs split
    user_inputted_info[0] = User.account_name
    user_inputted_info[1] = selection.split('-', 1)[0]
    user_inputted_info[2] = selection.split('-', 1)[1]
    user_inputted_info[3] = User.poesessid
    user_inputted_info[4] = User.client_txt_path

    # push the update to the file and inform UserData of the change
    file_update('push')

    # hide the character selection frame
    character_change_frame.grid_forget()
    character_change_frame.destroy()

# this is the main entry point into the app
program_startup()

# mainloop() needs to be at the end of the code. it's blocking and it's responsible for triggering events
main_window.mainloop()
