
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
            # [fin_df, q_fin_df] = self.getFinancials(str(symbol))
            # [bal_df, q_bal_df] = self.getBalanceSheet(str(symbol))
            # cashflow_df, q_cashflow_df = self.getCashFlow(str(symbol))

            # Populate the columns of the spreadsheet
            try:
                self.value_df.at[symbol, 'sector'] = fundamentals_dict['Company Information']['sector']
                self.value_df.at[symbol, 'industry'] = fundamentals_dict['Company Information']['industry']
                self.value_df.at[symbol, 'marketCap'] = fundamentals_dict['Company Information']['marketCap']
                self.value_df.at[symbol, 'enterpriseValue'] = fundamentals_dict['Company Information']['enterpriseValue']
                # self.value_df.at[symbol, 'acquirersMult'] = self.acquirersMultiple(fundamentals_dict['Company Information'],q_fin_df)
                self.value_df.at[symbol, 'numAnalystOp'] = fundamentals_dict['Company Information']['numberOfAnalystOpinions']
                # self.value_df.at[symbol, 'balSheetStr'] = self.balanceSheetStrength(q_bal_df)
                self.value_df.at[symbol, 'instOwnerPct'] = fundamentals_dict['Company Information']['heldPercentInstitutions']
                self.value_df.at[symbol, 'returnOnAssets'] = fundamentals_dict['Company Information']['returnOnAssets']
                self.value_df.at[symbol, 'returnOnEquity'] = fundamentals_dict['Company Information']['returnOnEquity']
                # self.value_df.at[symbol, 'ebitQ'] = q_fin_df.loc["Ebit"].iloc[0]
                # self.value_df.at[symbol, 'ebitTTM'] = sum(q_fin_df.loc["Ebit"].iloc[0:4])

            except KeyboardInterrupt:
                break

            except:
                print('Error when processing ' + str(symbol))

    # Write dataframe to spreadsheet
    self.value_df.to_csv(value_sheet_filepath,index=True)
