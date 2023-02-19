# PyDeepValue
Python library that finds deeply undervalued US equities via investment techniques of value investors Joel Greenblatt, Peter Lynch, &amp; Tobias Carlisle.

# Setup (optional if latest tickers required)
Create a developer account with TD Ameritrade:
https://developer.tdameritrade.com/

Log in and select "My Apps"

Create an app. Name it whatever you like, and use any callback URL (https://localhost:8080 worked for me), give it a purpose and Order Limit of 0 (this won't be making any orders, it's just for getting tickers).

Open the app you just created and copy the Consumer Key into the included `key.json` file.

# Prerequisites
pip3 install yahooquote

# Usage
Downloading data for all companies:
```
python3 PyDeepValue/DeepValue.py -d
python3 PyDeepValue/DeepValue.py --download
```

## Valuation functions to implement
Some of these are included, I am just making a list
- Categorize Peter Lynch-style: Slow grower, stalwart, fast grower, cyclical, turnaround, asset opportunity
- Year-over-year earnings growth
- PE ratio
- PE ratio relative to historical average
- PE ratio relative to industry average
- PE ratio relative to earnings growth
- ratio of debt to equity / balance sheet strength
- Net cash per share
- dividends and payout ratio
- inventories

## Good qualities to check for - subjective
Also from Lynch
- Boring name/product
- company is a spin off
- fast growth company in no growth industry
- niche firm difficult for others to enter
- recurring need for product, drugs, razors, etc
- user but not producer of technology
- low institutional holding
- low analyst coverage
- insider buying
- company is buying back shares

## To do
- Put all companies in the valuation spreadsheet
- Add symbol, name, sector, industry
- define valuation functions and what data they need
- sector and industy analysis: 


## Improvements
- Separate private (requires API key) class and general/public class (no key required but uses old data)
- Test ideas: US tickers in, US tickers out should be same length
- camel case? What's the standard on naming conventions for python? make everything consistent
- clean up true/false boolean statements to put them on one line :D
- fix printTickerLengths to make it generic based on the filepath
- add default path values to self.valuepath, self.alltickerspath, etc, and make them member variables
- refactor the libraries & modules