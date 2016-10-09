#   env\scripts\activate


#           Net Check | Python 3
#               by Ryan Keller
#
#   A proactive monitoring system made in order to view store uptime with the
#   intention of delivering IT and vendor services to stores experiencing outages.
#
################################################################################
#
#   Functions:
#       1) Net Check
#           Manually check the status of a store and detect outages.
#       2) Range Monitor
#           Checks stores within specific ranges; scan an entire enterprise
#       3) List Monitor
#           Collect a .csv list of store data and scan for outages
#
#   Data File Format: .csv (basic excell/spreadsheet)
#       Store               Country         Register Count
#       Integer, 5 long     US or CA        Integer, no limit
#
#   Example data set:
#       10304               US              2
#       267                 CA              6   
#

################################################################################
#                                      Import Segment
################################################################################

import os, sys
from pytrends.request import TrendReq
    
################################################################################
#                                      Credentials
################################################################################

USERNAME = ''
PASSWORD = ''
AGENT = ''

NAMES = []

CREDENTIAL_FILE = os.path.join(os.path.dirname(sys.argv[0]), 'data', 'data.txt')
NAME_LIST = os.path.join(os.path.dirname(sys.argv[0]), 'names', 'names.csv')

COUNTRY = 'World'
COUNTRY = 'US'



################################################################################
#                                      Main Function
################################################################################

def main():
    loadCredentials()
    loadNames()
    
    # Menu loop
    while True:
        try:
            menu()
            choice = option(0, 5)
        
            #CREDENTIAL MANAGER
            if choice == 1:
                credentials()
            #NAMELIST SETTINGS
            elif choice == 2:
                namelist()
            #DOWNLOAD SETTINGS
            elif choice == 3:
                downloadsettings()
            #AD-HOC TREND PULL
            elif choice == 4:
                pull(True, True, True)
                # def pull(adhoc=True, save=True, printDataFrame=False):
            #MASS TREND PULL
            elif choice == 5:
                pull(False, True, True)
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
        USERNAME = 'fostertrends'
        PASSWORD = 'ProfBorah'
        AGENT = 'ProfessorTrendy'
    print('-'*40)
    return
    
    
def loadNames():
    global NAMES
    try:
        r = open(NAME_LIST, 'r')
        NAMES = []
        index = 0
        line = r.readline()
        while line != '':
            line = line.rstrip('\n')
            NAMES.append(line)
            index += 1
            line = r.readline()    
        r.close()
        NAMES = ', '.join(NAMES)
        
        print('Auto-Loading Names:\n' + NAME_LIST + '\t(' + str(index) + ')')
        
    except Exception as e:
        print('Could not load name list by default')
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
    print('='*40)
    print('\t1) Update Credentials')
    print('\t2) Namelist Settings')
    print('\t3) Download Settings')
    print('\t4) Ad-Hoc Trend Pull')
    print('\t5) Namelist Trend Pull')
    print('='*40)
    return
    
    
################################################################################
#                                      Primary Operations
################################################################################
    
def credentials():
    '''User prompt to update instance-based credentials'''
    print('-'*40)
    print('Edit Google Credentials:')
    print(' .'*20)
    global USERNAME, PASSWORD, AGENT
    USERNAME = raw_input('Username: ').rstrip('\n')
    PASSWORD = raw_input('Password: ').rstrip('\n')
    print('"Agent" is the name of the google request')
    AGENT = raw_input('Password: ').rstrip('\n')
    print('-'*40)
    
    return
    
    
def namelist():
    return

def downloadsettings():
    return
    
def pull(adhoc=True, save=True, printDataFrame=False):
    try:
        pytrend = TrendReq(USERNAME, PASSWORD, AGENT)
        if adhoc:
            terms = raw_input('Search: ').rstrip('\n')
        else:
            terms = 'placeholder, placeholder2'
        payload = {'q': terms, 'geo': COUNTRY}
        
        # trend = pytrend.trend(payload)
        # print(trend)
        
        df = pytrend.trend(payload, return_type='dataframe')
        if printDataFrame:
            print(df)
        
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