#   env\scripts\activate

################################################################################
#                                      Import Segment
################################################################################

import os, sys
from pytrends.request import TrendReq
import pandas as pd     #DataFrame File Formatting
    
################################################################################
#                                      Credentials
################################################################################

USERNAME = ''
PASSWORD = ''
AGENT = ''

SEARCHES = []

CREDENTIAL_FILE = os.path.join(os.path.dirname(sys.argv[0]), 'data', 'data.txt')
SEARCH_LIST = os.path.join(os.path.dirname(sys.argv[0]), 'searches', 'searches.csv')
SAVE_FILE = os.path.join(os.path.dirname(sys.argv[0]), 'trends', 'trends.csv')

COUNTRY = 'US'


################################################################################
#                                      Main Function
################################################################################

def main():
    loadCredentials()
    loadSearches()
    
    # Menu loop
    while True:
        try:
            menu()
            choice = option(0, 6)
        
            #CREDENTIAL MANAGER
            if choice == 1:
                credentials()
            #SEARCH LIST SETTINGS
            elif choice == 2:
                searchList = raw_input('Search List Location: ').rstrip('\n')
                loadSearches(searchList)
            #DOWNLOAD SETTINGS
            elif choice == 3:
                global SAVE_FILE
                SAVE_FILE = raw_input('Save Location: ').rstrip('\n')
            elif choice == 4:
                global COUNTRY
                if COUNTRY == 'World':
                    COUNTRY = 'US'
                else:
                    COUNTRY = 'WORLD'
            #AD-HOC TREND PULL
            elif choice == 5:
                pull(True, True, True)
            #MASS TREND PULL
            elif choice == 6:
                pull(False, True, False)
            #EXIT SENTINEL
            elif choice == 0:
                sys.exit()

        except KeyboardInterrupt:
            #Pressed Ctrl-C to terminate a subprocess
            print ('Process interupped by keyboard - returning to menu')
            continue
        except SystemExit:
            break
    return
    
    
    
################################################################################
#                                      Initialization Functions
################################################################################
    
def loadCredentials():
    '''Auto-load a credential file, use defaults if unavailable'''
    global USERNAME, PASSWORD, AGENT
    try:
        r = open(CREDENTIAL_FILE, 'r')
        credentials = []
        index = 0
        line = r.readline()
        while line != '':
            line = line.rstrip('\n')
            line = line.split()
            if len(line) < 2:
                line.append('')
            credentials.append(line[1])
            index += 1
            line = r.readline()    
        r.close()
        
        print('Auto-Loading credentials:\n' + CREDENTIAL_FILE)
        USERNAME = credentials[0]
        PASSWORD = credentials[1]
        AGENT = credentials[2]
        
    except Exception as e:
        print('Could not locate credentials, loading defaults')
        USERNAME = 'missing_user'
        PASSWORD = 'missing_pass'
        AGENT = 'trendpull_agent'
    print('-'*40)
    return
    
    
def loadSearches(searchList=SEARCH_LIST):
    global SEARCHES
    try:
        r = open(SEARCH_LIST, 'r')
        SEARCHES = []
        index = 0
        line = r.readline()
        while line != '':
            line = line.rstrip('\n')
            SEARCHES.append(line)
            index += 1
            line = r.readline()    
        r.close()
        SEARCHES = ', '.join(SEARCHES)
        
        print('Loading search list:\n' + SEARCH_LIST + '\t(' + str(index) + ')')
        
    except Exception as e:
        print('Could not load search list.')
    print('-'*40)
    
    return
    
    
def menu():
    '''Display the main menu'''
    print('\n\n')
    print('='*40)
    print('Trend Pull - Beta')
    print('\tCode by Ryan Keller')
    print('\tGithub: RcKeller | rykeller@uw.edu')
    print(' .'*20)
    print('USER:\t\t' + USERNAME + '\n' +
    'PASS:\t\t' + ('*' * len(PASSWORD)) + '\n' + 
    'AGENT:\t\t' + AGENT)
    print(' .'*20)
    print('SAVING TO:\t\t' + SAVE_FILE)
    print('='*40)
    print('\t1) Update Credentials')
    print('\t2) Update Search List')
    print('\t3) Change Save File')
    print('\t4) Data For: ' + COUNTRY)
    print('\t5) Ad-Hoc Trend Pull')
    print('\t6) Mass Trend Pull')
    print('='*40)
    return
    
    
################################################################################
#                                      Primary Operations
################################################################################
    
def credentials():
    '''User prompt to update instance-based credentials'''
    global USERNAME, PASSWORD, AGENT
    USERNAME = raw_input('Username: ').rstrip('\n')
    PASSWORD = raw_input('Password: ').rstrip('\n')
    print('"Agent" is the name of the google request')
    AGENT = raw_input('Password: ').rstrip('\n')
    print('-'*40)
    
    return
    
    
def pull(adhoc=True, save=True, printDataFrame=False):
    try:
        print('-'*40)
        print('Connecting to Google...')
        pytrend = TrendReq(USERNAME, PASSWORD, AGENT)
        
        if adhoc:
            print(' .'*20)
            terms = raw_input('Search: ').rstrip('\n')
            print(' .'*20)
        else:
            terms = SEARCHES
        payload = {'q': terms, 'geo': COUNTRY}
        
        print('Requesting trends from Google...')
        df = pytrend.trend(payload, return_type='dataframe')
        
        print('Trends received.')
        if printDataFrame:
            print('-'*40)
            print(df)
            print('-'*40)
            
        if save:
            print('Saving trends to: ' + SAVE_FILE + '...')
            df.to_csv(SAVE_FILE, encoding='utf-8')
            print('Saved trend data to: ' + SAVE_FILE)
    
    except Exception as reason:
        returnException(reason)
    return
    
    
################################################################################
#                                      Tertiary Operations
################################################################################

def option(low, high):
    '''Loops until valid menu options are selected'''
    while True:
        try:
            option = int(input('Option >    '))
            if (option >= low) and (option <= high):
                break
            else:
                print('Option must be between ' + low + '-' + high)
        except KeyboardInterrupt as reason:
            sys.exit()
        except:
            print('Option not accepted')
    return option

    
def returnException(reason):
    '''Formatting for returning an exception'''
    print('='*40)
    print(reason)
    print('Returning to Menu - see cause above')
    print('='*40)
    return
    
    
    
################################################################################
#                                      Function Calls
################################################################################

main()