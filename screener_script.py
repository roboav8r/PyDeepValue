import PyDeepValue.DeepValue

dv = DeepValue.DeepValueClass()


test_tickers_json = DeepValue.getTickersFromRegExp('[A-Z]')
print(test_tickers_json)