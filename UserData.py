"""this file holds data members for user specific information as well as a setup method to grab the data"""

account_name = ''
character_name = ''
league = ''
poesessid = ''
client_txt_path = ''

# this is the template for the lines of the userdata.txt file if it needs to be created. the user info replaces %
user_data_file_structure = ('account_name=%', 'character_name=%', 'league=%', 'poesessid=%', 'client_txt_path=%')


def load_user_data():
    """loads user data from the text file userdata.txt and stores for local use"""

    global account_name
    global character_name
    global league
    global poesessid
    global client_txt_path

    with open('userdata.txt', 'r') as input_file:
        for line in input_file.readlines():
            if 'account' in line:
                account_name = line.split('=', 1)[1].strip("\'\r\n")
            elif 'character' in line:
                character_name = line.split('=', 1)[1].strip("\'\r\n")
            elif 'league' in line:
                league = line.split('=', 1)[1].strip("\'\r\n")
            elif 'poesessid' in line:
                poesessid = line.split('=', 1)[1].strip("\'\r\n")
            elif 'client' in line:
                client_txt_path = line.split('=', 1)[1].strip("\'\r\n")

load_user_data()
