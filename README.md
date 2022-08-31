# PyDeepValue
Python library that finds deeply undervalued US equities via investment techniques of value investors Joel Greenblatt, Peter Lynch, &amp; Tobias Carlisle.

# Setup (optional if latest tickers required)
Create a developer account with TD Ameritrade:
https://developer.tdameritrade.com/

Log in and select "My Apps"

Create an app. Name it whatever you like, and use any callback URL (https://localhost:8080 worked for me), give it a purpose and Order Limit of 0 (this won't be making any orders, it's just for getting tickers).

Open the app you just created and copy the Consumer Key into the included `key.json` file.


## To Do
- Separate private (requires API key) class and general/public class (no key required but uses old data)
- exception handling for if the description is blank, exchange is blank, or other edge cases so that the system exits gracefully
- Test ideas: US tickers in, US tickers out should be same length
- camel case? What's the standard on naming conventions for python? make everything consistent
- clean up true/false boolean statements to put them on one line :D
- fix printTickerLengths to make it generic based on the filepath
- add default path values to self.valuepath, self.alltickerspath, etc