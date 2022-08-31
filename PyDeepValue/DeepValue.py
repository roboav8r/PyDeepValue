from os.path import exists
from socket import gaierror
import requests
import json
from urllib.parse import quote
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

class DeepValue:

    # Initialize the DeepValue object
    def __init__(self, data_dir='../data/'):

        # Get TD Ameritrade consumer API key from .json file
        self.key = json.load(open(data_dir+'key.json'))

        # Define company data directory
        self.company_data_dir = data_dir + 'company_data/'
    

    ### INPUT/OUTPUT HELPER FUNCTIONS
    # Return a dictionary with the tickers that meet an input regexp
    def getTickersFromRegExp(self,symbol_regexp):

        # Get TD Ameritrade API key from file, symbol search regexp, and TD Ameritrade address
        address='https://api.tdameritrade.com/v1/instruments'
        
        # Build HTTP GET request string
        req_str = ''.join([address,'?apikey=',self.key,'&symbol=',quote(symbol_regexp.encode('utf-8')),'&projection=symbol-regex'])

        # Get tickers from TD Ameritrade API that meet the regexp 
        tickers_json = requests.get(req_str).json()

        return tickers_json

    # Save ticker dictionary to file
    def saveTickerJson(self,ticker_dict,filepath):
        
        # Write reduced tickers to .json file
        with open(filepath, "w") as outfile:
            json.dump(ticker_dict, outfile, indent=4)

    # Load ticker dictionary from file
    def loadTickerDict(self, filepath):
        return json.load(open(filepath))
    
    # Save all tickers to JSON file
    def saveAllTickersToJson(self,all_reg_exp='[A-Z]+',all_tickers_filepath='../data/all_tickers.json'):

        # Usage: DeepValue.saveAllTickersToJson()
        self.saveTickerJson(self.getTickersFromRegExp(all_reg_exp),all_tickers_filepath)


    ### SCREENING HELPER FUNCTIONS: 
    # These reduce the number of tickers to evaluate by excluding foreign stocks, ETFs, etc.

    # Is the ticker listed on a US exchange?
    def isUsListed(self,ticker): 
        # Input: ticker dictionary entry, returned from TD Ameritrade API call (see data/all_tickers.json format)
        # Output: Boolean True/False if the ticker is listed on one of the three US exchanges (NYSE, NASDAQ, AMEX)
        if (ticker['exchange'] in ['NYSE','NASDAQ','AMEX']):
            return True
        else:
            return False
    
    # Is the ticker an equity?
    def isEquity(self,ticker):
        # Input: ticker dictionary entry, returned from TD Ameritrade API call (see data/all_tickers.json format)
        # Output: Boolean True/False if the ticker is an equity (vice an ETF or other asset type)
        if (ticker['assetType'] =='EQUITY'):
            return True
        else:
            return False

    # Scan dictionary of tickers and return only tickers listed on US exchanges (AMEX, NYSE, NASDAQ)
    def getUsEquityJson(self,tickers_dict, us_tickers_filepath='../data/us_equity_tickers.json'):

        # Copy the input dictionary instead of editing it
        us_tickers_dict = tickers_dict.copy()

        # Cycle through all tickers in the input dictionary
        for ticker in tickers_dict.keys():
            
            # In the output dictionary, delete each entry that is NOT a US-listed EQUITY

            if ((self.isUsListed(tickers_dict[ticker])==False) or (self.isEquity(tickers_dict[ticker])==False)):
                del us_tickers_dict[ticker]
                continue # go to the next ticker
                
        # Write us equity ticker dictionary to .json file
        self.saveTickerJson(us_tickers_dict,us_tickers_filepath)
    
    # Check to see if the ticker dictionary actually has a description (some do not)
    def hasDescription(self,ticker):
        if 'description' in ticker.keys():
            return True
        else:
            return False

    # Is the ticker a SPAC?
    def isSpac(self,ticker): 
        # Input: ticker dictionary entry, returned from TD Ameritrade API call (see data/all_tickers.json format)
        # Output: Boolean True/False if the ticker is a Special Purpose Acquisition Corp
        if (('Acquisition Co' in ticker['description']) or ('SPAC' in ticker['description'])):
            return True
        else:
            return False
    
    # Is the company an American Depositary Receipt (ADR)?
    def isAdr(self,ticker):
        # Input: ticker dictionary entry, returned from TD Ameritrade API call (see data/all_tickers.json format)
        # Output: Boolean True/False if the ticker is an ADR
        if ((' ADR' in ticker['description']) or ('epositary' in ticker['description']) or ('Depository' in ticker['description'])):
            return True
        else:
            return False
    
    # Is this ticker for SPAC warrants?
    def isWarrant(self,ticker):
        if (('- Warrant' in ticker['description']) or ('- warrant' in ticker['description']) or ('warrants' in ticker['description']) or ('Warrants' in ticker['description'])):
            return True
        else:
            return False   

    # Scan dictionary of tickers and return only tickers listed on US exchanges (AMEX, NYSE, NASDAQ)
    def getValueJson(self,tickers_dict, value_tickers_filepath='../data/value_tickers.json'):

        # Copy the input dictionary instead of editing it
        value_tickers_dict = tickers_dict.copy()

        # Cycle through all tickers in the input dictionary
        for ticker in tickers_dict.keys():
            
            # In the output dictionary, delete each entry that doesn't have a description or is a SPAC/ADR
            if ((self.hasDescription(tickers_dict[ticker])==False) or (self.isSpac(tickers_dict[ticker])==True) or (self.isAdr(tickers_dict[ticker])==True)or (self.isWarrant(tickers_dict[ticker])==True)):
                del value_tickers_dict[ticker]
                continue # go to the next ticker
                
        # Write us equity ticker dictionary to .json file
        self.saveTickerJson(value_tickers_dict,value_tickers_filepath)

    ### WHITELIST GENERATION
    ## Create a whitelist/blacklist of Sectors, Industries, and Companies

    # Create list of valid sectors/industries to evaluate, given a list of companies from magicformulainvesting.com
    def createIndustryWhitelist(self,company_whitelist_path='../data/whitelist_companies.json',industry_whitelist_path='../data/industry_whitelist.json'):

        # Check if industry whitelist file exists. If not, create it with an empty dictionary inside.
        if exists(industry_whitelist_path) is False:
            print('No industry whitelist file found. Creating.')

            with open(industry_whitelist_path, "w") as outfile:
                json.dump(dict(), outfile, indent=4)

        # Open up whitelist file and get dictionary from it
        industry_whitelist_dict = json.load(open(industry_whitelist_path))

        # Cycle through each company in the companies whitelist
        company_whitelist = json.load(open(company_whitelist_path))

        # Get sector and industry info
        for company in company_whitelist:

            print("Getting info for: " + company)
            #ticker_yf = yf.Ticker(company)
            
            try:
                ticker_info = self.getFundamentals(company, data_expiration=timedelta(days=300))["Company Information"]

                # If sector is not in industry whitelist dictionary, add it and initialize an empty list
                if ticker_info['sector'] not in industry_whitelist_dict.keys():
                    industry_whitelist_dict[ticker_info['sector']] = []

                # If industry is not in sector list, add it
                if ticker_info['industry'] not in industry_whitelist_dict[ticker_info['sector']]:
                    industry_whitelist_dict[ticker_info['sector']].append(ticker_info['industry'])
                
                print(industry_whitelist_dict)
            
            except:
                print('Couldn\'t get info for: ' + company)

                print(industry_whitelist_dict)

        # Write to .json list file
        with open(industry_whitelist_path, "w") as outfile:
            json.dump(industry_whitelist_dict, outfile, indent=4)

    # Create a company blacklist to reduce time downloading data
    def createCompanyBlacklist(self,company_list_path='../data/value_list.json',company_blacklist_path='../data/industry_data/company_blacklist.json',industry_blacklist_path='../data/industry_data/industry_blacklist.json'):

        # Check if industry blacklist file exists. If not, create it with an empty list inside.
        if exists(company_blacklist_path) is False:
            print('No company blacklist file found. Creating.')

            with open(company_blacklist_path, "w") as outfile:
                json.dump([], outfile, indent=4)

        # Open up sector/industry blacklist file as dictionary
        industry_blacklist_dict = json.load(open(industry_blacklist_path))

        # Open up company blacklist json as list
        company_blacklist = json.load(open(company_blacklist_path))
        
        # Cycle through each company in the companies list
        company_list = json.load(open(company_list_path))

        # Get sector and industry info for each company
        for company in company_list:

            print("Getting info for: " + company)
            
            try:
                ticker_info = self.getFundamentals(company, data_expiration=timedelta(days=300))["Company Information"]

                # If company sector is in sector blacklist, ensure company is in the company blacklist
                if ticker_info['sector'] in industry_blacklist_dict.keys():
                    if company not in company_blacklist:
                        company_blacklist.append(company)

            except:
                company_blacklist.append(company)

        # Write blacklist to .json list file
        with open(company_blacklist_path, "w") as outfile:
            json.dump(company_blacklist, outfile, indent=4)


    
    ### MISCELLANEOUS JSON/SCREENER/VALUE FUNCTIONS

    # Sanity check - see how many tickers were screened out
    def printTickerLengths(self):

        # Load all the dictionaries
        all_tickers_dict = self.loadTickerDict('../data/all_tickers.json')
        us_equities_tickers_dict = self.loadTickerDict('../data/us_equity_tickers.json')
        value_tickers_dict = self.loadTickerDict('../data/value_tickers.json')

        print('Total tickers: ' + str(len(all_tickers_dict)))
        print('US equities tickers: ' + str(len(us_equities_tickers_dict)))
        print('Value tickers: ' + str(len(value_tickers_dict)))


    ### COMPANY DATA FETCHING FUNCTIONS

    # Download latest company fundamental information, save to .json file
    def downloadFundamentalData(self,symbol,path,current_time):

        # Initialize YahooFinance ticker object and data dictionary
        ticker = yf.Ticker(symbol)
        data_dict = dict()

        # Call the ticker object and save the data to the dictionary
        data_dict['Last Updated'] = str(current_time)
        data_dict['Company Information'] = ticker.info
        
        # Save the company data as a JSON object
        with open(path, "w") as outfile:
            json.dump(data_dict, outfile, indent=4)
        
        return data_dict

    # Download the latest financial data, save to specified paths
    def downloadFinancials(self,symbol,fin_path, q_fin_path):

        # Initialize YahooFinance ticker object and data dictionary
        ticker = yf.Ticker(symbol)

        # Get quarterly and annual financial dataframes
        financials_df = ticker.financials
        quarterly_financials_df = ticker.quarterly_financials
        
        # Save to .json file
        financials_df.to_json(fin_path,indent=4)
        quarterly_financials_df.to_json(q_fin_path,indent=4)

        # Return dataframes
        return financials_df, quarterly_financials_df

    # Download the latest balance sheet data, save to specified paths
    def downloadBalanceSheet(self,symbol,bal_path, q_bal_path):

        # Initialize YahooFinance ticker object and data dictionary
        ticker = yf.Ticker(symbol)

        # Get quarterly and annual financial dataframes
        balance_sheet_df = ticker.balancesheet
        quarterly_balance_sheet_df = ticker.quarterly_balancesheet
        
        # Save to .json file
        balance_sheet_df.to_json(bal_path,indent=4)
        quarterly_balance_sheet_df.to_json(q_bal_path,indent=4)

        # Return dataframes
        return balance_sheet_df, quarterly_balance_sheet_df

    # Download the latest cashflow data, save to specified paths
    def downloadCashflowData(self,symbol,cf_path, q_cf_path):

        # Initialize YahooFinance ticker object and data dictionary
        ticker = yf.Ticker(symbol)

        # Get quarterly and annual financial dataframes
        cashflow_df = ticker.cashflow
        quarterly_cashflow_df = ticker.quarterly_cashflow
        
        # Save to .json file
        cashflow_df.to_json(cf_path,indent=4)
        quarterly_cashflow_df.to_json(q_cf_path,indent=4)

        # Return dataframes
        return cashflow_df, quarterly_cashflow_df

    # Download fundamental data or retrieve recently saved data, as appropriate
    def getFundamentals(self, symbol, data_expiration=timedelta(days=7)):

        company_data_filepath = self.company_data_dir + str(symbol) + '.json'
        current_time = datetime.now()

        # Check if company fundamental data file exists
        if exists(company_data_filepath):

            # Open fundamental data as dictionary
            fund_data_dict = json.load(open(company_data_filepath))

            # Check if data has expired
            update_datetime = datetime.strptime(fund_data_dict['Last Updated'],"%Y-%m-%d %H:%M:%S.%f")
            timedelta_since_update = current_time - update_datetime
            data_is_expired = (timedelta_since_update > data_expiration)

            # If data is expired
            if data_is_expired:
                fund_data = self.downloadFundamentalData(symbol,company_data_filepath,current_time)
                return fund_data
            # Otherwise, use the retrieved data
            else:
                return fund_data_dict
        
        # If data doesn't exist, OR it's expired
        else:
            new_data = self.downloadFundamentalData(symbol,company_data_filepath,current_time)
        
            # Return dataframe objects
            return new_data

    # Download or retrieve financial data from .json, as appropriate
    def getFinancials(self, symbol):

        company_fin_filepath = self.company_data_dir + str(symbol) + '_financials.json'
        company_q_fin_filepath = self.company_data_dir + str(symbol) + '_quarterly_financials.json'

        # Check if company financial data file exists
        if ((exists(company_fin_filepath) is True) and (exists(company_q_fin_filepath) is True)):

            # Open financial data as pandas dataframes
            financials_df = pd.read_json(company_fin_filepath)
            q_financials_df = pd.read_json(company_q_fin_filepath)

            return [financials_df, q_financials_df]
        
        # If data doesn't exist
        else:
            
            financials_df, q_financials_df = self.downloadFinancials(symbol,company_fin_filepath,company_q_fin_filepath)
        
            # Return dataframe objects
            return [financials_df, q_financials_df]

    # Download or retrieve balance sheet from .json, as appropriate
    def getBalanceSheet(self, symbol):

        company_bal_filepath = self.company_data_dir + str(symbol) + '_balance_sheet.json'
        company_q_bal_filepath = self.company_data_dir + str(symbol) + '_quarterly_balance_sheet.json'

        # Check if balance sheet data file exists
        if ((exists(company_bal_filepath) is True) and (exists(company_q_bal_filepath) is True)):

            # Open balance sheet dataframes
            balance_df = pd.read_json(company_bal_filepath)
            q_balance_df = pd.read_json(company_q_bal_filepath)

            return [balance_df, q_balance_df]
        
        # If data doesn't exist
        else:
            
            balance_df, q_balance_df = self.downloadBalanceSheet(symbol,company_bal_filepath,company_q_bal_filepath)
        
            # Return dataframe objects
            return [balance_df, q_balance_df]


    # Download or retrieve cashflow data from .json, as appropriate
    def getCashFlow(self, symbol):

        company_cashflow_filepath = self.company_data_dir + str(symbol) + '_cash_flow.json'
        company_q_cashflow_filepath = self.company_data_dir + str(symbol) + '_quarterly_cash_flow.json'

        # Check if company fundamental data file exists
        if ((exists(company_cashflow_filepath) is True) and (exists(company_q_cashflow_filepath) is True)):

            # Open cashflow data as Pandas dataframe
            cashflow_df = pd.read_json(company_cashflow_filepath)
            q_cashflow_df = pd.read_json(company_q_cashflow_filepath)

            return [cashflow_df, q_cashflow_df]
        
        # If data doesn't exist
        else:

            cashflow_df, q_cashflow_df = self.downloadCashflowData(symbol,company_cashflow_filepath,company_q_cashflow_filepath)
        
            # Return dataframe objects
            return [cashflow_df, q_cashflow_df]


    ### EVALUATION FUNCTIONS
    def acquirersMultiple(self, stonk_info,stonk_q_financials):
        return stonk_info['enterpriseValue']/sum(stonk_q_financials.loc["Ebit"].iloc[0:4])

    def trailingPe(self, stonk_info):
        return stonk_info['regularMarketPrice']/stonk_info['trailingEps']

    def instOwnershipPct(self, stonk_info):
        return stonk_info['heldPercentInstitutions']

    def balanceSheetStrength(self,balance_sheet):
        tse = balance_sheet.loc['Total Stockholder Equity'].iloc[0]
        ltd = balance_sheet.loc['Long Term Debt'].iloc[0] if ('Long Term Debt' in balance_sheet.index) else 0.0
        return tse/(tse + ltd)

    
    ### SPREADSHEET MANAGEMENT FUNCTIONS

    # Initialize the value dataframe/spreadsheet
    def initValueSheet(self,tickers_dict,value_sheet_filepath='../data/value_sheet.csv'):

        # Check to see if the spreadsheet is already there
        if exists(value_sheet_filepath) is False:

            # Create Pandas dataframe from value ticker dictionary
            self.value_df = pd.DataFrame().from_dict(tickers_dict, orient='index', columns=['description','sector','industry','marketCap','enterpriseValue','acquirersMult','balSheetStr','numAnalystOp','instOwnerPct','instOwnerPctPercentileIndustry','instOwnerPctPercentileMarket','returnOnAssets','roaPercentileIndustry','roaPercentileMarket','returnOnEquity','roePercentileIndustry','roePercentileMarket'])

            # Write value dataframe to csv spreadsheet
            self.value_df.to_csv(value_sheet_filepath,index=True)

        else: # Open the existing spreadsheet and get the dataframe from it
            self.value_df = pd.read_csv(value_sheet_filepath,index_col=0,dtype={'description': str, 'sector': str, 'industry': str, 'marketCap': np.float64, 'enterpriseValue': np.float64, 'acquirersMult': np.float64, 'balSheetStr': np.float32, 'numAnalystOp': int, 'instOwnerPct': np.float32, 'instOwnerPctPercentileIndustry': np.float32, 'instOwnerPctPercentileMarket': np.float32, 'returnOnAssets': np.float32, 'roaPercentileIndustry': np.float32, 'roaPercentileMarket': np.float32, 'returnOnEquity': np.float32, 'roePercentileIndustry': np.float32,'roePercentileMarket': np.float32})

    ### POPULATING THE SPREADSHEET

    # Get ticker data from Yahoo Finance API & create dataframe

    # Write ticker dataframe to value spreadsheet
    def populateValueSheet(self,symbols,value_sheet_filepath='../data/value_sheet.csv', company_blacklist_path='../data/industry_data/company_blacklist.json'):

        # Inputs:
        # symbols = list of symbols of tickers to get data for, e.g. ['A','B','C']
        # Company blacklist path

        company_blacklist = json.load(open(company_blacklist_path))

        for symbol in symbols:

            if symbol not in company_blacklist:

                # Output 
                print('Getting company info for: ' + str(symbol))

                # Get company info
                fundamentals_dict = self.getFundamentals(str(symbol),data_expiration=timedelta(days=10))
                [fin_df, q_fin_df] = self.getFinancials(str(symbol))
                [bal_df, q_bal_df] = self.getBalanceSheet(str(symbol))
                # cashflow_df, q_cashflow_df = self.getCashFlow(str(symbol))


                # Populate the columns of the spreadsheet
                self.value_df.at[symbol, 'sector'] = fundamentals_dict['Company Information']['sector']
                self.value_df.at[symbol, 'industry'] = fundamentals_dict['Company Information']['industry']

                try:
                    self.value_df.at[symbol, 'marketCap'] = fundamentals_dict['Company Information']['marketCap']
                    self.value_df.at[symbol, 'enterpriseValue'] = fundamentals_dict['Company Information']['enterpriseValue']
                    self.value_df.at[symbol, 'acquirersMult'] = self.acquirersMultiple(fundamentals_dict['Company Information'],q_fin_df)
                    self.value_df.at[symbol, 'numAnalystOp'] = fundamentals_dict['Company Information']['numberOfAnalystOpinions']
                    self.value_df.at[symbol, 'balSheetStr'] = self.balanceSheetStrength(q_bal_df)
                    self.value_df.at[symbol, 'instOwnerPct'] = fundamentals_dict['Company Information']['heldPercentInstitutions']
                    self.value_df.at[symbol, 'returnOnAssets'] = fundamentals_dict['Company Information']['returnOnAssets']
                    self.value_df.at[symbol, 'returnOnEquity'] = fundamentals_dict['Company Information']['returnOnEquity']
                    self.value_df.at[symbol, 'ebitQ'] = q_fin_df.loc["Ebit"].iloc[0]
                    self.value_df.at[symbol, 'ebitTTM'] = sum(q_fin_df.loc["Ebit"].iloc[0:4])

                except KeyboardInterrupt:
                    break

                except:
                    print('Error when processing ' + str(symbol))

        # Write dataframe to spreadsheet
        self.value_df.to_csv(value_sheet_filepath,index=True)

            





# Initialize DV object
dv = DeepValue()

# Retrieve all tickers
#all_tickers_dict = dv.loadTickerDict('../data/all_tickers.json')

# Screen tickers for US equities & save to .json
# dv.getUsEquityJson(all_tickers_dict)

# Retrieve US equities tickers
#us_equities_tickers_dict = dv.loadTickerDict('../data/us_equity_tickers.json')

# Further screen US tickers for value candidates & save value tickers to .json
# dv.printTickerLengths()
# dv.getValueJson(us_equities_tickers_dict)
# dv.printTickerLengths()


# Retrieve value tickers dict
value_tickers_dict = dv.loadTickerDict('../data/value_tickers.json')

# Print out lengths
# dv.printTickerLengths()

# Initialize value spreadsheet
dv.initValueSheet(value_tickers_dict,'../data/value_sheet.csv')

# Get list of all tickers to check - these are just the keys of the value dictionary with no additional values
# value_tickers_list = list(value_tickers_dict.keys())
# dv.saveTickerJson(value_tickers_list,'../data/value_list.json')
# dv.createCompanyBlacklist()

# Populate value spreadsheet
dv.populateValueSheet(dv.loadTickerDict('../data/value_list.json'),'../data/value_sheet.csv')


# Whitelist stuff
#dv.createIndustryWhitelist()
# Create list of ALL industries
#dv.createIndustryWhitelist(company_whitelist_path='../data/value_list.json',industry_whitelist_path='../data/industry_data/industry_list.json')



# NEXT

# Redo columns of value spreadsheet
# Add indent to ticker .jsons for readability
# Short percent of float - compare to short interest website
# List of failed companies - find out why! "Fund" fails


# TO DO / KNOWN IMPROVEMENTS

# Whitelist creation: modularize the file existence check. Check on startup?
# Clean up the value tickers list in the short term !!! add indent=4 !!!
# Custom filepath for data / make this a parameter of the class
# Make data files hidden / inaccessible? What happens if a name changes
# Right now, library checks for existence of files but not contents or update time. it breaks if someone messes with file
# MAke an update financial data which actually checks to see what is in the dataframe and merges the two!
# Check dates on earnings reports - greater than 2 months? refresh_Earnings
# __main__ function - starting from scratch, do all the screening, pulling data, and evaluating
#  other edits (especially with data directory) to use as standalone library