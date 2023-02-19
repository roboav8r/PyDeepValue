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
