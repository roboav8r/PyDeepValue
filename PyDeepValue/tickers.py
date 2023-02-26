import requests
from urllib.parse import quote
import json

### INPUT/OUTPUT HELPER FUNCTIONS
# Return a dictionary with the tickers that meet an input regexp
def getTickersFromRegExp(symbol_regexp, apikey):

    # Get TD Ameritrade API key from file, symbol search regexp, and TD Ameritrade address
    address='https://api.tdameritrade.com/v1/instruments'
    
    # Build HTTP GET request string
    req_str = ''.join([address,'?apikey=',apikey,'&symbol=',quote(symbol_regexp.encode('utf-8')),'&projection=symbol-regex'])

    # Get tickers from TD Ameritrade API that meet the regexp 
    tickers_json = requests.get(req_str).json()

    return tickers_json

# Save ticker dictionary to file
def saveTickerJson(ticker_dict,filepath):
    
    # Write reduced tickers to .json file
    with open(filepath, "w") as outfile:
        json.dump(ticker_dict, outfile, indent=4)

# Load ticker dictionary from file
def loadTickerDict(filepath):
    return json.load(open(filepath))

# Save all tickers to JSON file
def saveAllTickersToJson(all_reg_exp='[A-Z]+',all_tickers_filepath='../data/all_tickers.json'):

    # Usage: DeepValue.saveAllTickersToJson()
    saveTickerJson(getTickersFromRegExp(all_reg_exp),all_tickers_filepath)


### SCREENING HELPER FUNCTIONS: 
# These reduce the number of tickers to evaluate by excluding foreign stocks, ETFs, etc.

# Is the ticker listed on a US exchange?
def isUsListed(ticker): 
    # Input: ticker dictionary entry, returned from TD Ameritrade API call (see data/all_tickers.json format)
    # Output: Boolean True/False if the ticker is listed on one of the three US exchanges (NYSE, NASDAQ, AMEX)
    if (ticker['exchange'] in ['NYSE','NASDAQ','AMEX']):
        return True
    else:
        return False

# Is the ticker an equity?
def isEquity(ticker):
    # Input: ticker dictionary entry, returned from TD Ameritrade API call (see data/all_tickers.json format)
    # Output: Boolean True/False if the ticker is an equity (vice an ETF or other asset type)
    if (ticker['assetType'] =='EQUITY'):
        return True
    else:
        return False

# Scan dictionary of tickers and return only tickers listed on US exchanges (AMEX, NYSE, NASDAQ)
def getUsEquityJson(tickers_dict, us_tickers_filepath='../data/us_equity_tickers.json'):

    # Copy the input dictionary instead of editing it
    us_tickers_dict = tickers_dict.copy()

    # Cycle through all tickers in the input dictionary
    for ticker in tickers_dict.keys():
        
        # In the output dictionary, delete each entry that is NOT a US-listed EQUITY

        if ((isUsListed(tickers_dict[ticker])==False) or (isEquity(tickers_dict[ticker])==False)):
            del us_tickers_dict[ticker]
            continue # go to the next ticker
            
    # Write us equity ticker dictionary to .json file
    saveTickerJson(us_tickers_dict,us_tickers_filepath)

# Check to see if the ticker dictionary actually has a description (some do not)
def hasDescription(ticker):
    if 'description' in ticker.keys() and (ticker['description'] != "Symbol not found"):
        return True
    else:
        return False

# Is the ticker a SPAC?
def isSpac(ticker): 
    # Input: ticker dictionary entry, returned from TD Ameritrade API call (see data/all_tickers.json format)
    # Output: Boolean True/False if the ticker is a Special Purpose Acquisition Corp
    if (('Acquisition Co' in ticker['description']) or ('SPAC' in ticker['description'])):
        return True
    else:
        return False

# Is the company an American Depositary Receipt (ADR)?
def isAdr(ticker):
    # Input: ticker dictionary entry, returned from TD Ameritrade API call (see data/all_tickers.json format)
    # Output: Boolean True/False if the ticker is an ADR
    if ((' ADR' in ticker['description']) or ('epositary' in ticker['description']) or ('Depository' in ticker['description'])):
        return True
    else:
        return False

# Is this ticker for SPAC warrants?
def isWarrant(ticker):
    if (('- Warrant' in ticker['description']) or ('- warrant' in ticker['description']) or ('warrants' in ticker['description']) or ('Warrants' in ticker['description'])):
        return True
    else:
        return False   

# Scan dictionary of tickers and return only tickers that have descriptions, aren't SPAC-related
def getValueJson(tickers_dict, value_tickers_filepath='../data/value_tickers.json'):

    # Copy the input dictionary instead of editing it
    value_tickers_dict = tickers_dict.copy()

    # Cycle through all tickers in the input dictionary
    for ticker in tickers_dict.keys():
        
        # In the output dictionary, delete each entry that doesn't have a description or is a SPAC/ADR
        if ((hasDescription(tickers_dict[ticker])==False) or (isSpac(tickers_dict[ticker])==True) or (isAdr(tickers_dict[ticker])==True)or (isWarrant(tickers_dict[ticker])==True)):
            del value_tickers_dict[ticker]
            continue # go to the next ticker
            
    # Write us equity ticker dictionary to .json file
    saveTickerJson(value_tickers_dict,value_tickers_filepath)