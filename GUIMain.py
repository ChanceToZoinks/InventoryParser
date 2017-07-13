import tkinter
import os
import UserData as User

main_window = tkinter.Tk()

# this list must always have the same number of entries as 'user_data_file_structure' found in UserData.py
# this is mostly test code. later it will be improved so it's not so fragile
user_inputted_info = ('dong', 'squad', '420', 'blazeit', 'yolo')


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

# mainloop() needs to be at the end of the code. it's blocking and it's responsible for triggering events
file_setup()
print(str(open('userdata.txt').readlines()))
main_window.mainloop()
