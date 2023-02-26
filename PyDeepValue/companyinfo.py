import yahooquery as yq
from datetime import datetime, timedelta
import json
from os.path import exists

### COMPANY DATA FETCHING FUNCTIONS

# Download latest company fundamental information, save to .json file
def downloadFundamentalData(symbol,path,current_time, ticker):

    # Initialize data dictionary
    data_dict = dict()

    # Call the ticker object and save the data to the dictionary
    data_dict['Last Updated'] = str(current_time)
    data_dict['Company Information'] = ticker.info
    
    # Save the company data as a JSON object
    with open(path, "w") as outfile:
        json.dump(data_dict, outfile, indent=4)

def downloadKeyData(symbol,path,current_time, ticker, mod):

    # Initialize data dictionary
    data_dict = dict()

    # Call the ticker object and save the data to the dictionary
    data_dict = ticker.get_modules(mod)
    data_dict['Last Updated'] = str(current_time)
    
    # Save the company data as a JSON object
    with open(path, "w") as outfile:
        json.dump(data_dict, outfile, indent=4)

def downloadAllFinancials(symbol,fin_path, q_fin_path, ticker):
    # Get quarterly and annual financial dataframes
    quarterly_financials_df = ticker.all_financial_data()
    
    # Save to .json file
    quarterly_financials_df.to_csv(q_fin_path)


# Download the latest financial data, save to specified paths
def downloadFinancials(symbol,fin_path, q_fin_path, ticker):

    # Get quarterly and annual financial dataframes
    financials_df = ticker.financials
    quarterly_financials_df = ticker.quarterly_financials
    
    # Save to .json file
    financials_df.to_json(fin_path,indent=4)
    quarterly_financials_df.to_json(q_fin_path,indent=4)


# Download the latest balance sheet data, save to specified paths
def downloadBalanceSheet(symbol,bal_path, q_bal_path, ticker):

    # Get quarterly and annual financial dataframes
    balance_sheet_df = ticker.balancesheet
    quarterly_balance_sheet_df = ticker.quarterly_balancesheet
    
    # Save to .json file
    balance_sheet_df.to_json(bal_path,indent=4)
    quarterly_balance_sheet_df.to_json(q_bal_path,indent=4)


# Download the latest cashflow data, save to specified paths
def downloadCashflowData(symbol,cf_path, q_cf_path, ticker):

    # Get quarterly and annual financial dataframes
    cashflow_df = ticker.cashflow
    quarterly_cashflow_df = ticker.quarterly_cashflow
    
    # Save to .json file
    cashflow_df.to_json(cf_path,indent=4)
    quarterly_cashflow_df.to_json(q_cf_path,indent=4)


# # Download fundamental data or retrieve recently saved data, as appropriate
# def getFundamentals(self, symbol, data_expiration=timedelta(days=7)):

#     company_data_filepath = self.company_data_dir + str(symbol) + '.json'
#     current_time = datetime.now()

#     # Check if company fundamental data file exists
#     if exists(company_data_filepath):

#         # Open fundamental data as dictionary
#         fund_data_dict = json.load(open(company_data_filepath))

#         # Check if data has expired
#         update_datetime = datetime.strptime(fund_data_dict['Last Updated'],"%Y-%m-%d %H:%M:%S.%f")
#         timedelta_since_update = current_time - update_datetime
#         data_is_expired = (timedelta_since_update > data_expiration)

#         # If data is expired
#         if data_is_expired:
#             fund_data = self.downloadFundamentalData(symbol,company_data_filepath,current_time)
#             return fund_data
#         # Otherwise, use the retrieved data
#         else:
#             return fund_data_dict
    
#     # If data doesn't exist, OR it's expired
#     else:
#         new_data = self.downloadFundamentalData(symbol,company_data_filepath,current_time)
    
#         # Return dataframe objects
#         return new_data

# # Download or retrieve financial data from .json, as appropriate
# def getFinancials(self, symbol):

#     company_fin_filepath = self.company_data_dir + str(symbol) + '_financials.json'
#     company_q_fin_filepath = self.company_data_dir + str(symbol) + '_quarterly_financials.json'

#     # Check if company financial data file exists
#     if ((exists(company_fin_filepath) is True) and (exists(company_q_fin_filepath) is True)):

#         # Open financial data as pandas dataframes
#         financials_df = pd.read_json(company_fin_filepath)
#         q_financials_df = pd.read_json(company_q_fin_filepath)

#         return [financials_df, q_financials_df]
    
#     # If data doesn't exist
#     else:
        
#         financials_df, q_financials_df = self.downloadFinancials(symbol,company_fin_filepath,company_q_fin_filepath)
    
#         # Return dataframe objects
#         return [financials_df, q_financials_df]

# # Download or retrieve balance sheet from .json, as appropriate
# def getBalanceSheet(self, symbol):

#     company_bal_filepath = self.company_data_dir + str(symbol) + '_balance_sheet.json'
#     company_q_bal_filepath = self.company_data_dir + str(symbol) + '_quarterly_balance_sheet.json'

#     # Check if balance sheet data file exists
#     if ((exists(company_bal_filepath) is True) and (exists(company_q_bal_filepath) is True)):

#         # Open balance sheet dataframes
#         balance_df = pd.read_json(company_bal_filepath)
#         q_balance_df = pd.read_json(company_q_bal_filepath)

#         return [balance_df, q_balance_df]
    
#     # If data doesn't exist
#     else:
        
#         balance_df, q_balance_df = self.downloadBalanceSheet(symbol,company_bal_filepath,company_q_bal_filepath)
    
#         # Return dataframe objects
#         return [balance_df, q_balance_df]


# # Download or retrieve cashflow data from .json, as appropriate
# def getCashFlow(self, symbol):

#     company_cashflow_filepath = self.company_data_dir + str(symbol) + '_cash_flow.json'
#     company_q_cashflow_filepath = self.company_data_dir + str(symbol) + '_quarterly_cash_flow.json'

#     # Check if company fundamental data file exists
#     if ((exists(company_cashflow_filepath) is True) and (exists(company_q_cashflow_filepath) is True)):

#         # Open cashflow data as Pandas dataframe
#         cashflow_df = pd.read_json(company_cashflow_filepath)
#         q_cashflow_df = pd.read_json(company_q_cashflow_filepath)

#         return [cashflow_df, q_cashflow_df]
    
#     # If data doesn't exist
#     else:

#         cashflow_df, q_cashflow_df = self.downloadCashflowData(symbol,company_cashflow_filepath,company_q_cashflow_filepath)
    
#         # Return dataframe objects
#         return [cashflow_df, q_cashflow_df]

# Download all data for all value candidates
def downloadAllCompanyData(symbols,company_data_dir,ticker_blacklist_path):

    # Check if industry blacklist file exists. If not, create it with an empty list inside.
    if exists(ticker_blacklist_path) is False:
        print('No ticker blacklist file found. Creating.')

        with open(ticker_blacklist_path, "w") as outfile:
            json.dump([], outfile, indent=4)

    # Inputs:
    # symbols = list of symbols of tickers to get data for, e.g. ['A','B','C']
    modules = 'assetProfile summaryDetail price defaultKeyStatistics'
    modules = 'assetProfile recommendationTrend cashflowStatementHistory indexTrend defaultKeyStatistics industryTrend quoteType incomeStatementHistory fundOwnership summaryDetail insiderHolders calendarEvents upgradeDowngradeHistory price balanceSheetHistory earningsTrend secFilings institutionOwnership majorHoldersBreakdown balanceSheetHistoryQuarterly earningsHistory esgScores summaryProfile netSharePurchaseActivity insiderTransactions sectorTrend incomeStatementHistoryQuarterly cashflowStatementHistoryQuarterly earnings pageViews financialData'

    for symbol in symbols:
        # Output 
        print('Downloading company info for: ' + str(symbol))
        ticker = yq.Ticker(symbol)
        current_time = datetime.now()

        company_data_filepath = company_data_dir + str(symbol) + '.json'
        company_fin_filepath = company_data_dir + str(symbol) + '_financials.json'
        company_q_fin_filepath = company_data_dir + str(symbol) + '_quarterly_financials.json'
        company_q_fin_csv_filepath = company_data_dir + str(symbol) + '_quarterly_financials.csv'

        try:
            downloadKeyData(str(symbol),company_data_filepath,current_time,ticker,modules)
            downloadAllFinancials(symbol,company_fin_filepath,company_q_fin_csv_filepath,ticker)
        
        except KeyboardInterrupt:
                break
        
        except:
            print('Error processing ' + str(symbol))

            # Open up company blacklist json as list
            ticker_blacklist = json.load(open(ticker_blacklist_path))

            ticker_blacklist.append(symbol)
            
            # Write blacklist to .json list file
            with open(ticker_blacklist_path, "w") as outfile:
                json.dump(ticker_blacklist, outfile, indent=4)

# Download fundamental data or retrieve recently saved data, as appropriate
def getCompanyData(symbol,company_data_dir,ticker_blacklist_path,data_expiration=timedelta(days=7)):

    company_data_filepath = company_data_dir + str(symbol) + '.json'
    current_time = datetime.now()

    # Check if company fundamental data file exists
    if exists(company_data_filepath):

        # Open fundamental data as dictionary
        comp_data_dict = json.load(open(company_data_filepath))

        # Check if data has expired
        update_datetime = datetime.strptime(comp_data_dict['Last Updated'],"%Y-%m-%d %H:%M:%S.%f")
        timedelta_since_update = current_time - update_datetime
        data_is_expired = (timedelta_since_update > data_expiration)

        # If data is expired
        if data_is_expired:
            comp_data = downloadAllCompanyData(symbol,company_data_dir,ticker_blacklist_path)
            return comp_data
        # Otherwise, use the retrieved data
        else:
            return comp_data_dict
    
    # If data doesn't exist, OR it's expired
    else:
        new_data = downloadAllCompanyData(symbol,company_data_dir,ticker_blacklist_path)
    
        # Return dataframe objects
        return new_data


        # company_data_filepath = dv_obj.company_data_dir + str(symbol) + '.json'
        # downloadFundamentalData(str(symbol),company_data_filepath,current_time,ticker)

        # company_fin_filepath = dv_obj.company_data_dir + str(symbol) + '_financials.json'
        # company_q_fin_filepath = dv_obj.company_data_dir + str(symbol) + '_quarterly_financials.json'
        # downloadFinancials(symbol,company_fin_filepath,company_q_fin_filepath,ticker)
        
        # company_bal_filepath = dv_obj.company_data_dir + str(symbol) + '_balance_sheet.json'
        # company_q_bal_filepath = dv_obj.company_data_dir + str(symbol) + '_quarterly_balance_sheet.json'    
        # downloadBalanceSheet(symbol,company_bal_filepath,company_q_bal_filepath,ticker)

        # company_cashflow_filepath = dv_obj.company_data_dir + str(symbol) + '_cash_flow.json'
        # company_q_cashflow_filepath = dv_obj.company_data_dir + str(symbol) + '_quarterly_cash_flow.json'
        # downloadCashflowData(symbol,company_cashflow_filepath,company_q_cashflow_filepath,ticker)
