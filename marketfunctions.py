import requests
import json
bittrexURL = "https://bittrex.com/api/v1.1"
getMarketsURL = bittrexURL + '/public/getmarkets'
currencies = bittrexURL + '/public/getcurrencies'
ticker_example = bittrexURL + '/public/getticker'
getMarketSummaryURL = bittrexURL + '/public/getmarketsummary'
getmarketsummariesUrl = bittrexURL + "/public/getmarketsummaries"
getMarketHistoryURL = bittrexURL + "/public/getmarkethistory"
getOrderbookURL = bittrexURL +"/public/getorderbook"
marketNames = []

def getMarkets():
    try:
        response = requests.get(getMarketsURL)
    except ConnectionError as error:
        print(error)
        pass

    if ((response.json()['success']== True)):
        #print(response.json()['result'])
        return(response.json()['result'])
    else:
        print("Epic Fail")
        # good stuff, adopt to other functions
        raise NameError("getMarkets exeption: " + response.json()['message'])

def getMarketSummary(market):
    try:
        response = requests.get(getMarketSummaryURL + "?market=" + market)
    except ConnectionError as error:
        print(error)
        pass

    if (response.json()['success'] == True):
        print("Success detected")
    else:
        print("Epic Fail")
        # good stuff, adopt to other functions
        raise NameError("getMarketSummary exeption: " + response.json()['message'])

def getMarketHistory(market):
    try:
        response = requests.get(getMarketHistoryURL + "?market=" + market)
    except ConnectionError as error:
        print(error)
        pass

    if (response.json()['success'] == True):
        print("getMarketHistory: Success detected")

        return(response.json()['result'])
    else:
        print("Epic Fail")
        # good stuff, adopt to other functions
        raise NameError("getMarketHistory exeption: " + response.json()['message'])

def getOrderbook(market, type, depth):
    print("starting gerOrderBook ofr market: " + market)
    try:
        response = requests.get(getOrderbookURL + "?market=" + market + "&type=" + type + "&depth=" + depth)
    except ConnectionError as error:
        print(error)
        pass

    print("getOrderbook for market: " + market)
    if (response.json()['success'] == True):
        print("Success detected")
        return response.json()['result']
    else:
        print("Epic Fail")
        # good stuff, adopt to other functions
        raise NameError("getorderbook exeption: " + response.json()['message'])

def getMarketName(allMaketsItem):
    return(allMaketsItem['MarketName'])

def updateMarketNames(markets):
    for i in markets:
        marketName=getMarketName(i)
        if marketName not in marketNames:
            marketNames.append(marketName)
            print("updated marketNames with new market: " + marketName)

def transformTransactionToTuple(transaction):
    print(transaction)
    return((transaction['Id'],
            transaction['TimeStamp'],
            transaction['Quantity'],
            transaction['Price'],
            transaction['Total'],
            transaction['FillType'],
            transaction['OrderType']))

def getBTCMarkets(markets):
    BTCMarkets = []
    for i in markets:
        if i['BaseCurrency'] == 'BTC':
            BTCMarkets.append(i)
    return BTCMarkets

def getTickerResponce(market):
    try:
        ticker_response = requests.get(ticker_example + "?market=" + market)
    except ConnectionError as error:
        print(error)
        pass
    print("ticker")
    if ((ticker_response.json()['success']== True)):
        print(ticker_response.json()['result']['Bid'])
        print(ticker_response.json()['result'])