## FINAL PROJECT FOR SI 206, SENATE SEARCH, KELSEY TOPORSKI, KTOPS, 28234407
import json
import requests
from bs4 import BeautifulSoup
import plotly.plotly as py
import plotly.graph_objs as go
import sys
import codecs
import csv
import sqlite3
import webbrowser

sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)

# caching for senators info
CACHE_FNAME = 'senator_cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION = {}

def get_unique_key(url):
  return url

def make_request_using_cache(url):
    unique_ident = get_unique_key(url)

    if unique_ident in CACHE_DICTION:
        # print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    else:
        # print("Making a request for new data...")
        resp = requests.get(url)
        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION[unique_ident]

# dictionary of states
state_abbr_dict = {'ak': 'Alaska', 'al': 'Alabama', 'ar': 'Arkansas',
        'az': 'Arizona', 'ca': 'California', 'co': 'Colorado', 'ct': 'Connecticut',
        'de': 'Delaware', 'fl': 'Florida', 'ga': 'Georgia',
        'hi': 'Hawaii', 'ia': 'Iowa', 'id': 'Idaho', 'il': 'Illinois',
        'in': 'Indiana', 'ks': 'Kansas', 'ky': 'Kentucky', 'la': 'Louisiana', 'ma': 'Massachusetts',
        'md': 'Maryland', 'me': 'Maine', 'mi': 'Michigan', 'mn': 'Minnesota',
        'mo': 'Missouri', 'ms': 'Mississippi',
        'mt': 'Montana', 'nc': 'North Carolina', 'nd': 'North Dakota',
        'ne': 'Nebraska', 'nh': 'New Hampshire', 'nj': 'New Jersey', 'nm': 'New Mexico',
        'nv': 'Nevada', 'ny': 'New York', 'oh': 'Ohio', 'ok': 'Oklahoma', 'or': 'Oregon',
        'pa': 'Pennsylvania', 'ri': 'Rhode Island', 'sc': 'South Carolina',
        'sd': 'South Dakota', 'tn': 'Tennessee', 'tx': 'Texas', 'ut': 'Utah',
        'va': 'Virginia', 'vt': 'Vermont', 'wa': 'Washington',
        'wi': 'Wisconsin', 'wv': 'West Virginia', 'wy': 'Wyoming'
}
state_abbr_dict_list = state_abbr_dict.keys()

# senator class
class Senator:
    def __init__(self, first_name='No First Name Available', last_name='No Last Name Available'):
        self.first_name = first_name
        self.last_name = last_name

        # change to equal defaults, then foloow NationalSite way to input the data when it's there
        self.state = 'No State Available'
        self.age = 'No Age Available'
        self.sex = 'Male'
        self.party = 'No Party Available'
        self.website = 'No Website Available'
        self.contact_info_office_address = 'No Contact Info Available'
        self.contact_info_phone = 'No Contact Info Available'
        self.contact_info_online = 'No Contact Info Available'
        self.seat = 'No Seat Info Available'
        self.race = 'Caucasian'

    def __str__(self):
        print1 = 'Senator ' + self.first_name + ' ' + self.last_name + ' from ' + state_abbr_dict[(self.state).lower()] + ': \n'
        print2 = '- Sex: ' + self.sex + '\n'
        print3 = '- Race: ' + self.race + '\n'
        if self.party == 'R':
            print4 = '- Party: Republican' + '\n'
        elif self.party == 'D':
            print4 = '- Party: Democrat' + '\n'
        else:
            print4 = '- Party: Independent' + '\n'
        print5 = '- Website: ' + self.website + '\n'
        return print1 + print2 + print3 + print4 + print5

########## CACHING CALLS ##########
# from senators website main page
base_url = 'https://www.senate.gov/'

base_senate_url = base_url + 'senators/index.htm'
senate_page_text = make_request_using_cache(base_senate_url)
senate_page_soup = BeautifulSoup(senate_page_text, 'html.parser')

# from senators website women page
women_href1 = senate_page_soup.find_all('aside', class_='fluid sidebar_link_container')[0]
women_href2 = women_href1.find('span', class_='teasertext')
women_href3 = women_href2.find_all('p')[3]
women_href4 = women_href3.find_all('a')[2]
women_ats = women_href4.attrs
women_href = women_ats['href']

women_senate_url = base_url + women_href
women_page_text = make_request_using_cache(women_senate_url)
women_page_soup = BeautifulSoup(women_page_text, 'html.parser')

# from race page
race_href1 = senate_page_soup.find_all('aside', class_='fluid sidebar_link_container')[0]
race_href2 = race_href1.find('span', class_='teasertext')
race_href3 = race_href2.find_all('p')[3]
race_href4 = race_href3.find_all('a')[1]
race_ats = race_href4.attrs
race_href = race_ats['href']

race_senate_url = base_url + race_href
race_page_text = make_request_using_cache(race_senate_url)
race_page_soup = BeautifulSoup(race_page_text, 'html.parser')

# from senators website contact page
contact_href1 = senate_page_soup.find_all('aside', class_='fluid sidebar_link_container')[2]
contact_href2 = contact_href1.find('span', class_='teasertext')
contact_href3 = contact_href2.find('p')
contact_href4 = contact_href3.find('a')
contact_ats = contact_href4.attrs
contact_href = contact_ats['href']
contact_senate_url = base_url[:-1] + contact_href

# collecting data from the .gov website and the wiki website and putting it into the class
def get_senators_from_state(state_abbr):
    senators_list = []

    # filling in senator info
    # from main page:
    senators_table_content = senate_page_soup.find('table', id='listOfSenators')
    sen_table_body = senators_table_content.find('tbody')
    names = sen_table_body.find_all('tr')
    for i in names:
        name_text = i.find('a').text
        actual_name = name_text[0:-7]
        first_name = actual_name.split(',')[1][1:]
        if actual_name.split()[0][-1] == ',':
            last_name = actual_name.split()[0][:-1]
        else:
            last_name = actual_name.split()[0]

        if first_name == 'Chris':
            last_name = 'Van Hollen'

        sen = Senator(first_name, last_name)

        state = name_text[-3:-1]
        sen.state = state

        party = name_text[-5]
        sen.party = party

        sen_website = i.find('a')
        ats = sen_website.attrs
        website = ats['href']
        sen.website = website

        # from senators website women page:
        womans_name_page = women_page_soup.find('div', class_='contenttext_generic')
        womans_table = womans_name_page.find('table', class_='sortable')
        womans_table_body = womans_table.find('tbody')
        womans_names = womans_table_body.find_all('tr')
        for i in womans_names:
            current_women1 = i.find('b')
            if current_women1 != None:
                current_women2 = current_women1.find('a').text.strip()
                current_wsen_fn = current_women2.split(',')[1][1:-4]
                current_wsen_ln = current_women2.split(',')[0]

                if current_wsen_fn == sen.first_name and current_wsen_ln == sen.last_name:
                    sen.sex = 'Female'
                elif sen.last_name == 'Stabenow':
                    sen.sex = 'Female'
                elif sen.first_name == 'Catherine':
                    sen.sex = 'Female'
                elif sen.last_name == 'Harris':
                    sen.sex = 'Female'
                elif sen.last_name == 'Cantwell':
                    sen.sex = 'Female'

        # from race page
        race_page_info = race_page_soup.find('div', class_='contenttext_generic')
        race_info = race_page_info.find('full_story')
        race_names = race_info.find_all('p')
        current_names_race = []
        for i in race_names:
            names = i.text
            if names[-1] == '-':
                if names[0] != '-':
                    actual_race_fn = names.split()[0]
                    actual_race_ln = names.split()[1]
                    if actual_race_fn == 'Cory':
                        actual_race_ln = 'Booker'
                    elif actual_race_fn == 'Catherine':
                        actual_race_ln = 'Cortez Masto'
                    else:
                        actual_race_name = actual_race_fn + ' ' + actual_race_ln
                    current_names_race.append(actual_race_name)
                    for i in current_names_race[0:3]:
                        if actual_race_ln == sen.last_name:
                            sen.race = 'African American'
                    for i in current_names_race[3:6]:
                        if actual_race_fn == sen.first_name and actual_race_ln == sen.last_name:
                            sen.race = 'Asian American'
                    for i in current_names_race[6:]:
                        if actual_race_fn == sen.first_name:
                            sen.race = 'Hispanic American'

        if state.lower() == state_abbr:
            senators_list.append(sen)

    return senators_list

# getting a full list of senators
def get_full_senator_list():
    full_sen_list = []
    state_abbrs_only_list = state_abbr_dict.keys()
    for state in state_abbrs_only_list:
        sen = get_senators_from_state(state)
        full_sen_list.append(sen)

    # this will give a list of senators by state, so each part of the list will be a list of 2, except for Mississippi, which has 1

    return full_sen_list

# creating the database and putting collected data into it
sen_list = get_full_senator_list()
def init_db():
    # creating new database
    conn = sqlite3.connect('senators.db')
    cur = conn.cursor()

    # Drop tables
    statement = '''
        DROP TABLE IF EXISTS 'Senators';
    '''
    cur.execute(statement)
    conn.commit()

    statement = '''
        DROP TABLE IF EXISTS 'States';
    '''
    cur.execute(statement)
    conn.commit()

    # make new table
    statement = '''
        CREATE TABLE 'Senators' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'FirstName' TEXT NOT NULL,
            'LastName' TEXT NOT NULL,
            'StateId' INTEGER,
            'StateAbbr' TEXT,
            'Sex' TEXT,
            'Race' TEXT,
            'Party' TEXT NOT NULL,
            'Website' TEXT
        );
    '''
    cur.execute(statement)
    conn.commit()

    statement = '''
        CREATE TABLE 'States' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'StateName' TEXT NOT NULL,
            'StateAbbr' TEXT NOT NULL
        );
    '''
    cur.execute(statement)
    conn.commit()

    # populating the database
    complete_sen_list = []
    for i in sen_list:
        if len(i) == 2:
            complete_sen_list.append(i[0])
            complete_sen_list.append(i[1])
        else:
            complete_sen_list.append(i[0])

    for i in complete_sen_list:
        insertion = (None, i.first_name, i.last_name, None, i.state, i.sex, i.race, i.party, i.website)
        statement = 'INSERT INTO \'Senators\' '
        statement += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
        cur.execute(statement, insertion)
    conn.commit()

    for i in state_abbr_dict:
        state_abbr = i
        state_name = state_abbr_dict[i]

        insertion = (None, state_name, state_abbr.upper())
        statement = 'INSERT INTO \'States\' '
        statement += 'VALUES (?, ?, ?)'
        cur.execute(statement, insertion)
    conn.commit()

    conn.close()

# getting the right foreign keys and such
def states_mapping():
    conn = sqlite3.connect('senators.db')
    cur = conn.cursor()

    statement = 'SELECT * FROM States'
    cur.execute(statement)
    state_maps = {}

    for state in cur:
        state_id = state[0]
        abbr = state[2]
        state_maps[abbr] = state_id
    conn.commit()

    for i in state_maps:
        state = i
        id = state_maps[i]
        insertion = (id, state)
        statement = 'UPDATE Senators '
        statement += 'SET StateId = ? '
        statement += 'WHERE StateAbbr = ?'
        cur.execute(statement, insertion)
        conn.commit()

    conn.close()

# functions for making plots
def party_breakdown_whole():
    # pie
    reps = ''
    dems = ''
    ind = ''

    conn = sqlite3.connect('senators.db')
    cur = conn.cursor()

    statement = '''
        SELECT COUNT(*)
        FROM Senators
        WHERE Party = 'R'
    '''
    cur.execute(statement)
    conn.commit()
    reps1 = cur.fetchone()
    reps = reps1[0]

    statement = '''
        SELECT COUNT(*)
        FROM Senators
        WHERE Party = 'D'
    '''
    cur.execute(statement)
    conn.commit()
    dems1 = cur.fetchone()
    dems = dems1[0]

    statement = '''
        SELECT COUNT(*)
        FROM Senators
        WHERE Party = 'I'
    '''
    cur.execute(statement)
    conn.commit()
    ind1 = cur.fetchone()
    ind = ind1[0]

    fig = {
    'data': [{'labels': ['Republican','Democrat','Independent'],
              'values': [reps,dems,ind],
              'type': 'pie'}],
    'layout': {'title': 'Party Breakdown of the US Senate'}
    }

    py.plot(fig)

    conn.close()

def party_breakdown_state():
    conn = sqlite3.connect('senators.db')
    cur = conn.cursor()

    # getting state names for x axis
    states1 = []
    statement = '''
        SELECT StateName
        FROM States
    '''
    cur.execute(statement)
    conn.commit()
    for row in cur:
        states1.append(row[0])

    # making a states dict with all zeros values, make state dict
    zeros = [0]*50
    state_dict1 = dict(zip(states1, zeros))

    # getting number of rep senators for each state
    reps = []
    statement = '''
        SELECT States.StateName, COUNT(*)
        FROM Senators
        JOIN States
        ON Senators.StateId = States.Id
        WHERE Party = 'R'
        GROUP BY Senators.StateAbbr
    '''
    cur.execute(statement)
    conn.commit()
    for row in cur:
        reps.append(row)
    reps_dict = dict(reps)

    state_dict_vals1 = state_dict1.values()
    reps_dict_vals = reps_dict.values()

    for s in states1:
        for r in reps:
            if s == r[0]:
                state_dict1[s] = r[1]

    state_vals_r = list(state_dict_vals1)

    trace0 = go.Bar(
        x=states1,
        y=state_vals_r,
        name='Republicans',
        marker=dict(
            color='rgb(255,0,0)'
        )
    )

    # getting state names for x axis
    states2 = []
    statement = '''
        SELECT StateName
        FROM States
    '''
    cur.execute(statement)
    conn.commit()
    for row in cur:
        states2.append(row[0])

    # making a states dict with all zeros values, make state dict
    zeros = [0]*50
    state_dict2 = dict(zip(states2, zeros))

    # getting number of dem senators for each state
    dems = []
    statement = '''
        SELECT States.StateName, COUNT(*)
        FROM Senators
        JOIN States
        ON Senators.StateId = States.Id
        WHERE Party = 'D'
        GROUP BY Senators.StateAbbr
    '''
    cur.execute(statement)
    conn.commit()
    for row in cur:
        dems.append(row)
    dems_dict = dict(dems)

    state_dict_vals2 = state_dict2.values()
    dems_dict_vals = dems_dict.values()

    for s in states2:
        for d in dems:
            if s == d[0]:
                state_dict2[s] = d[1]

    state_vals_d = list(state_dict_vals2)

    trace1 = go.Bar(
        x=states2,
        y=state_vals_d,
        name='Democrats',
        marker=dict(
            color='rgb(0,0,255)',
        )
    )

    # getting state names for x axis
    states3 = []
    statement = '''
        SELECT StateName
        FROM States
    '''
    cur.execute(statement)
    conn.commit()
    for row in cur:
        states3.append(row[0])

    # making a states dict with all zeros values, make state dict
    zeros = [0]*50
    state_dict3 = dict(zip(states3, zeros))

    # getting number of ind senators for each state
    inds = []
    statement = '''
        SELECT States.StateName, COUNT(*)
        FROM Senators
        JOIN States
        ON Senators.StateId = States.Id
        WHERE Party = 'I'
        GROUP BY Senators.StateAbbr
    '''
    cur.execute(statement)
    conn.commit()
    for row in cur:
        inds.append(row)
    inds_dict = dict(inds)

    state_dict_vals3 = state_dict3.values()
    inds_dict_vals = inds_dict.values()

    for s in states3:
        for i in inds:
            if s == i[0]:
                state_dict3[s] = i[1]

    state_vals_i = list(state_dict_vals3)

    trace2 = go.Bar(
        x=states3,
        y=state_vals_i,
        name='Independent',
        marker=dict(
            color='rgb(255,255,102)',
        )
    )

    data = [trace0, trace1, trace2]
    layout = go.Layout(
        xaxis=dict(tickangle=-45),
        barmode='group',
    )

    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='angled-text-bar')

def sex_breakdown_whole():
    # pie
    male = ''
    female = ''

    conn = sqlite3.connect('senators.db')
    cur = conn.cursor()

    statement = '''
        SELECT COUNT(*)
        FROM Senators
        WHERE Sex = 'Male'
    '''
    cur.execute(statement)
    conn.commit()
    male1 = cur.fetchone()
    male = male1[0]

    statement = '''
        SELECT COUNT(*)
        FROM Senators
        WHERE Sex = 'Female'
    '''
    cur.execute(statement)
    conn.commit()
    female1 = cur.fetchone()
    female = female1[0]

    fig = {
    'data': [{'labels': ['Male','Female'],
              'values': [male,female],
              'type': 'pie'}],
    'layout': {'title': 'Sex Breakdown of the US Senate'}
    }

    py.plot(fig)

    conn.close()

def sex_breakdown_state():
    conn = sqlite3.connect('senators.db')
    cur = conn.cursor()

    # getting state names for x axis
    states1 = []
    statement = '''
        SELECT StateName
        FROM States
    '''
    cur.execute(statement)
    conn.commit()
    for row in cur:
        states1.append(row[0])

    # making a states dict with all zeros values, make state dict
    zeros = [0]*50
    state_dict1 = dict(zip(states1, zeros))

    # getting number of rep senators for each state
    men = []
    statement = '''
        SELECT States.StateName, COUNT(*)
        FROM Senators
        JOIN States
        ON Senators.StateId = States.Id
        WHERE Sex = 'Male'
        GROUP BY Senators.StateAbbr
    '''
    cur.execute(statement)
    conn.commit()
    for row in cur:
        men.append(row)
    men_dict = dict(men)

    state_dict_vals1 = state_dict1.values()
    men_dict_vals = men_dict.values()

    for s in states1:
        for m in men:
            if s == m[0]:
                state_dict1[s] = m[1]

    state_vals_m = list(state_dict_vals1)

    trace0 = go.Bar(
        x=states1,
        y=state_vals_m,
        name='Males',
        marker=dict(
            color='rgb(84,187,239)'
        )
    )

    # getting state names for x axis
    states2 = []
    statement = '''
        SELECT StateName
        FROM States
    '''
    cur.execute(statement)
    conn.commit()
    for row in cur:
        states2.append(row[0])

    # making a states dict with all zeros values, make state dict
    zeros = [0]*50
    state_dict2 = dict(zip(states2, zeros))

    # getting number of dem senators for each state
    wmen = []
    statement = '''
        SELECT States.StateName, COUNT(*)
        FROM Senators
        JOIN States
        ON Senators.StateId = States.Id
        WHERE Sex = 'Female'
        GROUP BY Senators.StateAbbr
    '''
    cur.execute(statement)
    conn.commit()
    for row in cur:
        wmen.append(row)
    wmen_dict = dict(wmen)

    state_dict_vals2 = state_dict2.values()
    wmen_dict_vals = wmen_dict.values()

    for s in states2:
        for w in wmen:
            if s == w[0]:
                state_dict2[s] = w[1]

    state_vals_w = list(state_dict_vals2)

    trace1 = go.Bar(
        x=states2,
        y=state_vals_w,
        name='Female',
        marker=dict(
            color='rgb(226,82,168)',
        )
    )

    data = [trace0, trace1]
    layout = go.Layout(
        xaxis=dict(tickangle=-45),
        barmode='group',
    )

    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='angled-text-bar')

def race_breakdown():
    # pie
    white = ''
    af_am = ''
    asian = ''
    hisp = ''

    conn = sqlite3.connect('senators.db')
    cur = conn.cursor()

    statement = '''
        SELECT COUNT(*)
        FROM Senators
        WHERE Race = 'Caucasian'
    '''
    cur.execute(statement)
    conn.commit()
    white1 = cur.fetchone()
    white = white1[0]

    statement = '''
        SELECT COUNT(*)
        FROM Senators
        WHERE Race = 'African American'
        '''
    cur.execute(statement)
    conn.commit()
    af_am1 = cur.fetchone()
    af_am = af_am1[0] + 1

    statement = '''
        SELECT COUNT(*)
        FROM Senators
        WHERE Race = 'Asian American'
        '''
    cur.execute(statement)
    conn.commit()
    asian1 = cur.fetchone()
    asian = asian1[0]

    statement = '''
        SELECT COUNT(*)
        FROM Senators
        WHERE Race = 'Hispanic American'
        '''
    cur.execute(statement)
    conn.commit()
    hisp1 = cur.fetchone()
    hisp = hisp1[0]

    fig = {
    'data': [{'labels': ['Caucasian', 'African American', 'Asian American', 'Hispanic'],
              'values': [white, af_am, asian, hisp],
              'type': 'pie'}],
    'layout': {'title': 'Race Breakdown of the US Senate'}
    }

    py.plot(fig)

    conn.close()

# MAIN PART OF CODE:
init_db()
states_mapping()

# user interactive part
if __name__ == "__main__":
    print('Welcome to Kelsey\'s Senate Search!')
    user_input = input('For directions on what you can do, please type \'help\', if you already know, type your search! ')
    print('\n')

    while user_input != 'exit':
        if user_input == 'help':
            print('\n' + 'I\'m so glad you asked for help! Here\'s what you can do here:' + '\n')
            print('To see a party breakdown of members of the current senate, please type \'party breakdown whole\'' + '\n')
            print('To see a party breakdown by state, please type \'party breakdown state\'' + '\n')
            print('To see a sex breakdown of members of the current senate, please type \'sex breakdown whole\'' + '\n')
            print('To see a sex breakdown by state, please type \'sex breakdown state\'' + '\n')
            print('To see a race breakdown of the members of senate (spoiler alert - there\'s a lot of white people!!), please type \'race breakdown\'' + '\n')
            print('To open the contact list for all the current senators, please type \'contact list\'' + '\n')
            print('To search for senators by state, please type in a state abbreviation. (ex: \'mi\' = Michigan)')
            print('This will give you a list of senators from that state, along with some information on them.' + '\n')
            print('To exit the program, please type \'exit\'')

        elif user_input == 'party breakdown whole':
            print('FACT: Republicans currently hold a house majority.')
            print('Check your browser to see a graph!' + '\n')
            party_breakdown_whole()

        elif user_input == 'party breakdown state':
            print('Check your browser to see a graph!' + '\n')
            party_breakdown_state()

        elif user_input == 'sex breakdown whole':
            print('Unsurprisingly, there are more men in the senate than women, which I think stinks.')
            print('Check your browser to see a graph!' + '\n')
            sex_breakdown_whole()

        elif user_input == 'sex breakdown state':
            print('Check your browser to see a graph!' + '\n')
            sex_breakdown_state()

        elif user_input == 'race breakdown':
            print('FACT: There are currently only 9 senators of color, none of whom are Native American Indians.')
            print('FACT: Kamala Harris is both African American and Asian American.')
            print('Check your browser to see a graph!' + '\n')
            race_breakdown()

        elif user_input == 'contact list':
            print('Check your browser to see the contact list!' + '\n')
            webbrowser.open(contact_senate_url)

        elif user_input[0:2] in state_abbr_dict_list:
            senator_results = get_senators_from_state(user_input[0:2])
            print('Senators from ' + state_abbr_dict[user_input[0:2]] + ': ' + '\n')
            for i in senator_results:
                print(i.__str__())

        else:
            print('Sorry, that\'s not a valid input! Try again.' + '\n')

        user_input = input('For directions on what you can do, please type \'help\', if you already know, type your search! ' )
        print('\n')

    # when main loop is exited
    print('Thanks for stopping by! Have a good day, and don\'t forget that 33/100 senate seats are up for grabs on Novermber 6, 2018, so get involved and go vote!')
