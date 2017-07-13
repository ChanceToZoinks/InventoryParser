import tkinter
import os
import UserData as User

main_window = tkinter.Tk()
setup_frame = tkinter.Frame(main_window)

# this list must always have the same number of entries as 'user_data_file_structure' found in UserData.py
# this is mostly test code. later it will be improved so it's not so fragile
user_inputted_info = ['acc', 'char', 'league', 'poesessid', 'client.txt path']


def file_setup():
    # check if userdata.txt exists and if not create it with the proper format
    if os.path.exists('userdata.txt'):
        print('userdata.txt exists nothing further needed here')
    else:
        with open('userdata.txt', 'w') as file:
            a = 0
            for item in User.user_data_file_structure:
                file.writelines(item.replace('%', user_inputted_info[a]) + '\n')
                a += 1


def display_user_data_entry_fields():
    global main_window
    global setup_frame

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

# mainloop() needs to be at the end of the code. it's blocking and it's responsible for triggering events
file_setup()
display_user_data_entry_fields()
print(str(open('userdata.txt').readlines()))
main_window.mainloop()
