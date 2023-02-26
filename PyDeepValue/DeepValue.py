'''
Import libraries
'''
from os.path import exists
from socket import gaierror

import json


import pandas as pd
import numpy as np
import sys
import getopt

import tickers
import companyinfo
import universe


class DeepValue:

    # Initialize the DeepValue object
    def __init__(self, data_dir='../data/'):

        # Get TD Ameritrade consumer API key from .json file
        self.key = json.load(open(data_dir+'key.json'))

        # Define ticker data directory
        self.ticker_data_dir = data_dir + 'ticker_data/'
        self.ticker_blacklist_path = self.ticker_data_dir + 'ticker_blacklist.json'

        # Define company data directory
        self.company_data_dir = data_dir + 'company_data/'

        # Define universe data directory
        self.universe_data_dir = data_dir + 'universe_data/'
        self.universe_sheet_path = self.universe_data_dir + 'universe.csv'

    
    ### MISCELLANEOUS JSON/SCREENER/VALUE FUNCTIONS

    # Sanity check - see how many tickers were screened out
    def printTickerLengths(self):

        # Load all the dictionaries
        all_tickers_dict = tickers.loadTickerDict('../data/ticker_data/all_tickers.json')
        us_equities_tickers_dict = tickers.loadTickerDict('../data/ticker_data/us_equity_tickers.json')
        value_tickers_dict = tickers.loadTickerDict('../data/ticker_data/value_tickers.json')

        print('Total tickers: ' + str(len(all_tickers_dict)))
        print('US equities tickers: ' + str(len(us_equities_tickers_dict)))
        print('Value tickers: ' + str(len(value_tickers_dict)))


if __name__ == "__main__":

    '''
    Handle user inputs
    '''
    arg_help = "{0} -t gets tickers, -s to screen tickers, -d to download screened tickers, and -e to evaluate".format(sys.argv[0])
    arg_tickers = False
    arg_screen = False
    arg_download = False
    arg_universe = False
    arg_evaluate = False

    try:
        opts, args = getopt.getopt(sys.argv[1:], "htsdue", ["help", "tickers", "screen", "download", "universe", "evaluate"])
    except:
        print(arg_help)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(arg_help)  # print the help message
            sys.exit(2)
        elif opt in ("-t", "--tickers"):
            arg_tickers = True
        elif opt in ("-s", "--screen"):
            arg_screen = True
        elif opt in ("-d", "--download"):
            arg_download = True
        elif opt in ("-u", "--universe"):
            arg_universe = True
        elif opt in ("-e", "--evaluate"):
            arg_evaluate = True

    print('Get tickers: ', arg_tickers)
    print('Screen tickers: ', arg_screen)
    print('Download data: ', arg_download)
    print('Build universe sheet: ', arg_universe)
    print('Evaluate companies: ', arg_evaluate)


    # Initialize DV object
    dv = DeepValue()

    # Perform tasks as specified from command line
    if arg_tickers:
        print("Getting all tickers")
        # Get all tickers, starting from scratch
        all_tickers = tickers.getTickersFromRegExp('[A-Z]+',dv.key)

        # Save all_tickers dictionary to file
        tickers.saveTickerJson(all_tickers,'../data/ticker_data/all_tickers.json')

    if arg_screen:
        print("Screening tickers")

        # Screen all tickers to value tickers
        all_tickers_dict = tickers.loadTickerDict('../data/ticker_data/all_tickers.json')

        # Screen tickers for US equities & save to .json
        tickers.getUsEquityJson(all_tickers_dict, us_tickers_filepath='../data/ticker_data/us_equity_tickers.json')

        # Retrieve US equities tickers
        us_equities_tickers_dict = tickers.loadTickerDict('../data/ticker_data/us_equity_tickers.json')

        # Further screen US tickers for value candidates & save value tickers to .json
        tickers.getValueJson(us_equities_tickers_dict, value_tickers_filepath='../data/ticker_data/value_tickers.json')
        value_tickers_dict = tickers.loadTickerDict('../data/ticker_data/value_tickers.json')
        value_tickers_list = list(value_tickers_dict.keys())
        tickers.saveTickerJson(value_tickers_list,'../data/ticker_data/value_list.json')
        dv.printTickerLengths()

    if arg_download:
        companyinfo.downloadAllCompanyData(tickers.loadTickerDict('../data/ticker_data/value_list.json'),dv,dv.ticker_blacklist_path)

    if arg_universe:
        # Ensure there is a spreadsheet at the location
        universe.initSheet(dv.universe_sheet_path)

        # Populate spreadsheet
        value_tickers_list = tickers.loadTickerDict('../data/ticker_data/value_list.json')
        universe.populateSheet(value_tickers_list, dv.universe_sheet_path, dv.ticker_blacklist_path)

# NEXT

# Redo columns of value spreadsheet
# Add indent to ticker .jsons for readability
# Short percent of float - compare to short interest website
# List of failed companies - find out why! "Fund" fails


# TO DO / KNOWN IMPROVEMENTS

# Move to EDGAR API
# Whitelist creation: modularize the file existence check. Check on startup?
# Custom filepath for data / make this a parameter of the class
# Make data files hidden / inaccessible? What happens if a name changes
# Right now, library checks for existence of files but not contents or update time. it breaks if someone messes with file
# MAke an update financial data which actually checks to see what is in the dataframe and merges the two!
# Check dates on earnings reports - greater than 2 months? refresh_Earnings
#  other edits (especially with data directory) to use as standalone library



# STEP 2: Creating the value sheet
# Retrieve value tickers dict
# value_tickers_dict = dv.loadTickerDict('../data/ticker_data/value_tickers.json')

# Initialize value spreadsheet
# dv.initValueSheet(value_tickers_dict,'../data/value_sheet.csv')


# STEP ???:
# Evaluate companies
# value_tickers_dict = dv.loadTickerDict('../data/ticker_data/value_tickers.json')
# dv.initValueSheet(value_tickers_dict,'../data/value_sheet.csv')
# dv.populateValueSheet(dv.loadTickerDict('../data/ticker_data/value_list.json'),'../data/value_sheet.csv')





# Whitelist stuff
#dv.createIndustryWhitelist()
# Create list of ALL industries
#dv.createIndustryWhitelist(company_whitelist_path='../data/value_list.json',industry_whitelist_path='../data/industry_data/industry_list.json')
