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

def marketCap(company_data_dict):
    return company_data_dict['defaultKeyStatistics']['sharesOutstanding']*company_data_dict['financialData']['currentPrice'] if ('currentPrice' in company_data_dict['financialData'].keys() and 'sharesOutstanding' in company_data_dict['defaultKeyStatistics'].keys()) else 'N/A marketCap'

def enterpriseValue(company_data_dict):
    return company_data_dict['summaryDetail']['marketCap'] + company_data_dict['financialData']['totalDebt'] - company_data_dict['financialData']['totalCash'] if ('marketCap' in company_data_dict['summaryDetail'].keys() and 'totalDebt' in company_data_dict['financialData'].keys() and 'totalCash' in company_data_dict['financialData'].keys()) else 'N/A enterpriseValue'

def netCashPerShare(company_data_dict):
    return (company_data_dict['financialData']['totalCash'] - company_data_dict['financialData']['totalDebt'])/company_data_dict['defaultKeyStatistics']['sharesOutstanding'] if ('sharesOutstanding' in company_data_dict['defaultKeyStatistics'].keys() and 'totalDebt' in company_data_dict['financialData'].keys() and 'totalCash' in company_data_dict['financialData'].keys()) else 'N/A netCashPerShare'