from os.path import exists
import pandas as pd
import numpy as np
import json

from datetime import timedelta

import companyinfo
import valuation

### SPREADSHEET MANAGEMENT FUNCTIONS

# Initialize the value dataframe/spreadsheet
def initSheet(univ_sheet_filepath):

    # Check to see if the spreadsheet is already there
    if exists(univ_sheet_filepath) is False:
        print("No universe sheet found. Creating.")
        empty_df = pd.DataFrame()
        empty_df.to_csv(univ_sheet_filepath)

    else:
        print("Universe sheet found at: " + univ_sheet_filepath)


### POPULATING THE SPREADSHEET
def populateSheet(symbols,ticker_blacklist_path,company_data_dir,univ_sheet_filepath):

    # Inputs:
    # symbols = list of symbols of tickers to get data for, e.g. ['A','B','C']
    # Company blacklist path

    # Initialize universe dataframe
    # value_df = pd.read_csv(value_sheet_filepath,index_col=0,dtype={'description': str, 'sector': str, 'industry': str, 'marketCap': np.float64, 'enterpriseValue': np.float64, 'acquirersMult': np.float64, 'balSheetStr': np.float32, 'numAnalystOp': int, 'instOwnerPct': np.float32, 'instOwnerPctPercentileIndustry': np.float32, 'instOwnerPctPercentileMarket': np.float32, 'returnOnAssets': np.float32, 'roaPercentileIndustry': np.float32, 'roaPercentileMarket': np.float32, 'returnOnEquity': np.float32, 'roePercentileIndustry': np.float32,'roePercentileMarket': np.float32})
    universe_df = pd.DataFrame(columns=['description','currentPrice','sector','industry','marketCap','enterpriseValue','pegRatio','numAnalystOp','instFloatPctHeld','insiderPctHeld'])
    # universe_df = pd.DataFrame()

    ticker_blacklist = json.load(open(ticker_blacklist_path))

    for symbol in symbols:

        if symbol not in ticker_blacklist:

            # Output 
            print('Getting company info for: ' + str(symbol))

            # Get company info
            company_dict = companyinfo.getCompanyData(str(symbol), company_data_dir, ticker_blacklist_path, timedelta(days=10))

            # Populate the columns of the spreadsheet
            try:
                universe_df.at[symbol,'description'] = company_dict[symbol]['quoteType']['longName']
                universe_df.at[symbol,'currentPrice'] = company_dict[symbol]['financialData']['currentPrice']
                universe_df.at[symbol,'sector'] = company_dict[symbol]['assetProfile']['sector'] if ('sector' in company_dict[symbol]['assetProfile']) else 'N/A sector' 
                universe_df.at[symbol,'industry'] = company_dict[symbol]['assetProfile']['industry'] if ('industry' in company_dict[symbol]['assetProfile']) else 'N/A industry'
                universe_df.at[symbol,'marketCap'] = company_dict[symbol]['summaryDetail']['marketCap'] if ('marketCap' in company_dict[symbol]['summaryDetail'].keys()) else valuation.marketCap(company_dict[symbol])
                universe_df.at[symbol,'enterpriseValue'] = company_dict[symbol]['defaultKeyStatistics']['enterpriseValue'] if ('enterpriseValue' in company_dict[symbol]['defaultKeyStatistics'].keys()) else valuation.enterpriseValue(company_dict[symbol])
                universe_df.at[symbol,'pegRatio'] = company_dict[symbol]['defaultKeyStatistics']['pegRatio'] if ('pegRatio' in company_dict[symbol]['defaultKeyStatistics'].keys()) else 'N/A pegRatio'
                universe_df.at[symbol,'numAnalystOp'] = company_dict[symbol]['financialData']['numberOfAnalystOpinions'] if ('numberOfAnalystOpinions' in company_dict[symbol]['financialData'].keys()) else 0
                universe_df.at[symbol,'instFloatPctHeld'] = company_dict[symbol]['majorHoldersBreakdown']['institutionsFloatPercentHeld']
                universe_df.at[symbol,'insiderPctHeld'] = company_dict[symbol]['majorHoldersBreakdown']['insidersPercentHeld']

            except KeyboardInterrupt:
                break

            except:
                print('Error when processing ' + str(symbol))

        else:
            # Output 
            print('Ticker blacklisted. NOT getting company info for: ' + str(symbol))

    # Write dataframe to spreadsheet
    universe_df.to_csv(univ_sheet_filepath,index=True)
