import tkinter
from tkinter import messagebox
import os
import UserData as User
import requests
import PlayerTracker
from itertools import islice

main_window = tkinter.Tk()
setup_frame = tkinter.Frame(main_window)
character_change_frame = tkinter.Frame(main_window)
main_menu_frame = tkinter.Frame(main_window)

# this is used to keep track of current menu so a user cant spam "GoTo main menu" and create problems
current_menu_displayed = main_menu_frame

# this list must always have the same number of entries as 'user_data_file_structure' found in UserData.py
# this is mostly test code. later it will be improved so it's not so fragile and also make solutions more generic
# always in order:  account > character > league > poesessid > client.txt path
user_inputted_info = ['acc', 'char', 'league', 'poesessid', 'client.txt path']


def program_startup():
    """handles all the necessary checks and routines for startup"""

    # initialize the menu since it should always be available
    init_nav_menu()

    # TODO: ADD THE ZONE TRACKER AND CHAOS COUNTER TO THE MAIN SCREEN
    # check if the userdata.txt file is found if not make the user enter all necessary data
    if os.path.exists('userdata.txt'):
        # load user data first
        User.load_user_data()
        start_player_tracking()
        # display main screen here
        display_main_menu()
    else:
        missing_user_file = 'userdata.txt not found. complete first time setup'
        display_message_box(missing_user_file, display_user_data_entry_fields)


def file_update(update_type='setup', changing_entries=None):
    """this should be called to ensure that the user info is populated. call with 'push' to update instead of setup
       you should pass a list of the entries that will change if you intend to push an update.
       example call: file_update('push', [1, 2]) this will update only the indices 1 and 2 so character and league
    """

    # check if userdata.txt exists and if not create it with the proper format
    if os.path.exists('userdata.txt') and update_type == 'setup':
        print('userdata.txt exists nothing further needed here')
    elif update_type == 'push':
        # the purpose of this case is to allow the function to be used as both a setup and to push updates to UserData
        # first open the file and read it into memory then replace the entries specified finally push the update
        with open('userdata.txt', 'r') as file:
            temp_file = file.readlines()
            for i, item in enumerate(User.user_data_file_structure):
                if i in changing_entries:
                    temp_file[i] = item.replace('%', user_inputted_info[i]) + '\n'
                else:
                    continue
            file.close()
        with open('userdata.txt', 'w') as file:
            file.writelines(temp_file)
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

    # set current window
    global current_menu_displayed
    current_menu_displayed = character_change_frame

    character_change_frame.grid()

    character_list = tkinter.Listbox(character_change_frame, selectmode='single')

    # change default size of character_list so all data is visible
    character_list.config(width=50)

    for c in grab_characters_from_server():
        character_list.insert(tkinter.END, c['name'] + "-" + c['league'])

    character_list.select_set(0)

    # configure list box to expand to stay in center
    tkinter.Grid.rowconfigure(main_window, 0, weight=1)
    tkinter.Grid.columnconfigure(main_window, 0, weight=1)
    character_list.grid()

    select_character = tkinter.Button(character_change_frame, text='Confirm', command=lambda: change_character_callback(
                                      character_list.get(character_list.curselection())))

    select_character.grid()


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
    user_inputted_info[1] = selection.split('-', 1)[0]
    user_inputted_info[2] = selection.split('-', 1)[1]

    # push the update to the file and inform UserData of the change
    file_update('push', [1, 2])


def display_main_menu():
    """displays main menu frame and contents"""

    # set current window
    global current_menu_displayed
    current_menu_displayed = main_menu_frame

    main_menu_frame.grid()

    current_zone_label = tkinter.Label(main_menu_frame, text=str(PlayerTracker.current_zone))
    current_zone_label.grid()


def nav_menu_callback(dest_menu_delegate):
    """this callback function lets us close menus that aren't in use"""

    if dest_menu_delegate == display_main_menu and not current_menu_displayed == main_menu_frame:
        for item in character_change_frame.children.values():
            item.grid_remove()
        # hide frames not in use
        character_change_frame.grid_remove()
        # then display the correct frame
        dest_menu_delegate()
    elif dest_menu_delegate == display_character_change and not current_menu_displayed == character_change_frame:
        for item in main_menu_frame.children.values():
            item.grid_remove()
        # hide frame not in use
        main_menu_frame.grid_remove()
        # then display the correct frame
        dest_menu_delegate()


def init_nav_menu():
    # the menu is always displayed on all screen to allow navigation between screens
    nav_menu_button = tkinter.Menubutton(main_window, text='Navigation', relief='raised')
    nav_menu_button.grid()
    nav_menu_button.menu = tkinter.Menu(nav_menu_button, tearoff=0)
    nav_menu_button['menu'] = nav_menu_button.menu

    # we use a callback here so we can make sure only destination menu is displayed
    nav_menu_button.menu.add_command(label='Main Menu',
                                     command=lambda: nav_menu_callback(display_main_menu))
    nav_menu_button.menu.add_command(label='Change Character',
                                     command=lambda: nav_menu_callback(display_character_change))

    nav_menu_button.grid()

# the reversed_lines, reversed_block and check_last_5_lines functions were found here:
# https://stackoverflow.com/questions/260273/most-efficient-way-to-search-the-last-x-lines-of-a-file-in-python


def reversed_lines(file):
    """Generate the lines of file in reverse order."""
    part = ''
    for block in reversed_blocks(file):
        for c in reversed(block):
            if c == '\n' and part:
                yield part[::-1]
                part = ''
            part += c
    if part:
        yield part[::-1]


def reversed_blocks(file, blocksize=4096):
    """Generate blocks of file's contents in reverse order."""
    file.seek(0, os.SEEK_END)
    here = file.tell()
    while 0 < here:
        delta = min(blocksize, here)
        here -= delta
        file.seek(here, os.SEEK_SET)
        yield file.read(delta)


def check_last_5_lines(file, key):
    """searching the last 5 lines of the file because the last 5 lines in Client.txt contain the info needed"""

    for line in islice(reversed_lines(file), 5):
        # first set tile hash then set zone name
        if key in line.rstrip('\n'):
            temp_zone_name = line.split(key, 1)[1]
            # if the most recent tile hash found isn't the current tile hash then we change the current tile hash
            if not temp_zone_name == PlayerTracker.current_zone:
                PlayerTracker.zone_changed(temp_zone_name)
    main_window.after(100, check_last_5_lines, file, key)


def start_player_tracking():
    file = open(User.client_txt_path, 'r')
    check_last_5_lines(file, 'Entering area ')

# this is the main entry point into the app
program_startup()

# mainloop() needs to be at the end of the code. it's blocking and it's responsible for triggering events
main_window.mainloop()
