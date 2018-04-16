## FINAL PROJECT FOR SI 206, SENATE SEARCH, KELSEY TOPORSKI, KTOPS, 28234407
############ TESTING ############
import unittest
from finalproj import *

class TestThatProjectBoi(unittest.TestCase):
    # testing get senators from problematic states with problematic senators
    def test_get_sens_info(self):
        sens = get_senators_from_state('nj')
        self.assertEqual(sens[0].first_name, 'Cory A.')
        self.assertEqual(sens[0].last_name, 'Booker')
        self.assertEqual(sens[0].sex, 'Male')
        self.assertEqual(sens[0].race, 'African American')
        self.assertEqual(sens[0].party, 'D')
        self.assertEqual(sens[0].state, 'NJ')

        self.assertEqual(sens[1].first_name, 'Robert')
        self.assertEqual(sens[1].last_name, 'Menendez')
        self.assertEqual(sens[1].sex, 'Male')
        self.assertEqual(sens[1].race, 'Hispanic American')
        self.assertEqual(sens[1].party, 'D')
        self.assertEqual(sens[1].state, 'NJ')

        sens = get_senators_from_state('ca')
        self.assertEqual(sens[0].first_name, 'Dianne')
        self.assertEqual(sens[0].last_name, 'Feinstein')
        self.assertEqual(sens[0].sex, 'Female')
        self.assertEqual(sens[0].race, 'Caucasian')
        self.assertEqual(sens[0].party, 'D')
        self.assertEqual(sens[0].state, 'CA')

        self.assertEqual(sens[1].first_name, 'Kamala D.')
        self.assertEqual(sens[1].last_name, 'Harris')
        self.assertEqual(sens[1].sex, 'Female')
        self.assertEqual(sens[1].race, 'African American')
        self.assertEqual(sens[1].party, 'D')
        self.assertEqual(sens[1].state, 'CA')

        sens = get_senators_from_state('mi')
        self.assertEqual(sens[0].first_name, 'Gary C.')
        self.assertEqual(sens[0].last_name, 'Peters')
        self.assertEqual(sens[0].sex, 'Male')
        self.assertEqual(sens[0].race, 'Caucasian')
        self.assertEqual(sens[0].party, 'D')
        self.assertEqual(sens[0].state, 'MI')

        self.assertEqual(sens[1].first_name, 'Debbie')
        self.assertEqual(sens[1].last_name, 'Stabenow')
        self.assertEqual(sens[1].sex, 'Female')
        self.assertEqual(sens[1].race, 'Caucasian')
        self.assertEqual(sens[1].party, 'D')
        self.assertEqual(sens[1].state, 'MI')

        sens = get_senators_from_state('vt')
        self.assertEqual(sens[0].first_name, 'Patrick J.')
        self.assertEqual(sens[0].last_name, 'Leahy')
        self.assertEqual(sens[0].sex, 'Male')
        self.assertEqual(sens[0].race, 'Caucasian')
        self.assertEqual(sens[0].party, 'D')
        self.assertEqual(sens[0].state, 'VT')

        self.assertEqual(sens[1].first_name, 'Bernard')
        self.assertEqual(sens[1].last_name, 'Sanders')
        self.assertEqual(sens[1].sex, 'Male')
        self.assertEqual(sens[1].race, 'Caucasian')
        self.assertEqual(sens[1].party, 'I')
        self.assertEqual(sens[1].state, 'VT')

        sens = get_senators_from_state('nv')
        self.assertEqual(sens[0].first_name, 'Catherine')
        self.assertEqual(sens[0].last_name, 'Cortez')
        self.assertEqual(sens[0].sex, 'Female')
        self.assertEqual(sens[0].race, 'Hispanic American')
        self.assertEqual(sens[0].party, 'D')
        self.assertEqual(sens[0].state, 'NV')

        self.assertEqual(sens[1].first_name, 'Dean')
        self.assertEqual(sens[1].last_name, 'Heller')
        self.assertEqual(sens[1].sex, 'Male')
        self.assertEqual(sens[1].race, 'Caucasian')
        self.assertEqual(sens[1].party, 'R')
        self.assertEqual(sens[1].state, 'NV')

    # testing database queries about senators
    def test_sens_db_queries(self):
        conn = sqlite3.connect('senators.db')
        cur = conn.cursor()

        statement = '''
            SELECT COUNT(*)
            FROM Senators
            WHERE Party = 'I'
        '''
        cur.execute(statement)
        conn.commit()
        inds = cur.fetchone()
        self.assertEqual(inds[0], 2)

        statement = '''
            SELECT COUNT(*)
            FROM Senators
            WHERE Party = 'D'
        '''
        cur.execute(statement)
        conn.commit()
        dems = cur.fetchone()
        self.assertEqual(dems[0], 47)

        statement = '''
            SELECT COUNT(*)
            FROM Senators
            WHERE Party = 'R'
        '''
        cur.execute(statement)
        conn.commit()
        reps = cur.fetchone()
        self.assertEqual(reps[0], 50)

    # testing database queries about states
    def test_states_db_queries(self):
        conn = sqlite3.connect('senators.db')
        cur = conn.cursor()
        statement = '''
            SELECT COUNT(*)
            FROM States
        '''
        cur.execute(statement)
        conn.commit()
        state_num = cur.fetchone()
        self.assertEqual(state_num[0], 50)

unittest.main()
