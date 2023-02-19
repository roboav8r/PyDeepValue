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
