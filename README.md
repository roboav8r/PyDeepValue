# PyDeepValue
Python library to help find and evaluate deeply undervalued US equities via investment techniques of value investors Joel Greenblatt, Peter Lynch, Roaring Kitty, Tobias Carlisle, and Aswath Damodaran.

NOTE: ***This is a work in progress but I am leaving it public in case anyone else might want to collaborate!***

Current status:
- Pulls data from Yahoo Finance API
- Some relative valuation metrics can be generated into a spreadsheet
- Getting started on intrinsic valuation based on Aswath Damodaran's lectures

# Setup (optional if latest tickers required)
Create a developer account with TD Ameritrade:
https://developer.tdameritrade.com/

Log in and select "My Apps"

Create an app. Name it whatever you like, and use any callback URL (https://localhost:8080 worked for me), give it a purpose and Order Limit of 0 (this won't be making any orders, it's just for getting tickers).

Open the app you just created and copy the Consumer Key into the included `key.json` file.

# Prerequisites
pip3 install yahooquote

# Usage

Getting all the tickers from TD Ameritrade:
```
python3 PyDeepValue/DeepValue.py -t
python3 PyDeepValue/DeepValue.py --tickers
```

Screening tickers for eligible US equities:
```
python3 PyDeepValue/DeepValue.py -s
python3 PyDeepValue/DeepValue.py --screen
```

Downloading data for all eligible companies:
```
python3 PyDeepValue/DeepValue.py -d
python3 PyDeepValue/DeepValue.py --download
```

Making an overview/"universe" spreadsheet:
```
python3 PyDeepValue/DeepValue.py -u
python3 PyDeepValue/DeepValue.py --universe
```

Performing a sector and industry analysis:
```
python3 PyDeepValue/DeepValue.py -i
python3 PyDeepValue/DeepValue.py --industry
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
- insider buying - OpenInsider?
- company is buying back shares

## To do
- sector and industry analysis
- define valuation functions and what data they need
- company analysis


## Improvements
- Switch to EDGAR API - https://www.sec.gov/edgar/sec-api-documentation
- Separate private (requires API key) class and general/public class (no key required but uses old data)
- Test ideas: US tickers in, US tickers out should be same length
- camel case? What's the standard on naming conventions for python? make everything consistent
- clean up true/false boolean statements to put them on one line :D
- fix printTickerLengths to make it generic based on the filepath
- add default path values to self.valuepath, self.alltickerspath, etc, and make them member variables
- refactor the libraries & modules
- for blacklist, give error code as to why it failed (e.g. no company info, call failed)

# Other Valuation Ideas / Features
- Roaring Kitty "Tracker" spreadsheet for overall market and sectors - Debt/Region/Indices/Commodities/Industries/Style chart10y - price - ch
- Tracking top 40: value, confidence
- - watch, on deck, pulse (big companies that indicate market) - various levels of monitoring
- Roaring Kitty Universe
- Roaring Kitty Company/fundamental analysis
- "Tags": keywords of the company; insiders own, PE firm involved, fund managers involved, 
- - Specific analyst or company purchasing?

# References
https://pages.stern.nyu.edu/adamodar/pdfiles/eqnotes/packet1pg2.pdf
