import requests
import json
from time import sleep, time
from marketfunctions import *
import threading
from influx import *
import influxdb
import datetime
import timeit

influxhost = '165.227.155.203'
influxport = "8086"
influxuser = "explorer"
influxpassword = "timeseries4days"


class singleMarket():
    def __init__(self, MarketCurrency,
                        BaseCurrency,
                        MarketCurrencyLong,
                        BaseCurrencyLong,
                        MinTradeSize,
                        MarketName,
                        IsActive,
                        Create,
                        Notice,
                        IsSponsored,
                        LogoUrl):

        self.MarketCurrency = MarketCurrency
        self.BaseCurrency = BaseCurrency
        self.MarketCurrencyLong = MarketCurrencyLong
        self.BaseCurrencyLong = BaseCurrencyLong
        self.MinTradeSize = MinTradeSize
        self.MarketName = MarketName
        self.IsActive = IsActive
        self.Create = Create
        self.Notice = Notice
        self.IsSponsored = IsSponsored
        self.LogoUrl = LogoUrl
        self.orderBookHistory = []

    def updateOrderHistory(self, order):
        for key in self.orderBookHistory:
            if self.orderBookHistory[key]['Id'] == order.Id:
                pass
            else:
                print("new transaction detected")
                self.orderBookHistory.append(order)

    def dumpNewOrderToFile(self, MarketName, Id,
                        TimeStamp,
                        Quantity,
                        Price,
                        Total,
                        FillType,
                        OrderType,):
    #not tested
        filename = MarketName + ".txt"
        with open(filename, "a") as myfile:
            myfile.write(Id + "," +
                    TimeStamp+ "," +
                    Quantity + "," +
                    Price + "," +
                    Total + "," +
                    FillType + "," +
                    OrderType)

    # does it look like accumulationg
    def anal(self):
        pass
        #identify if market starts accumulation
        #look for increase of small purchase orders

    def analSpike(self):
        pass
        #check if market is about to spike - implement the unicorn function

    def reportCandidates(self):
        pass

"""
class order():
    def __init__(self, Id,
                    TimeStamp,
                    Quantity,
                    Price,
                    Total,
                    FillType,
                    OrderType,):
        self.Id = Id
        self.TimeStamp = TimeStamp
        self.Quantity = Quantity
        self.Price = Price
        self.Total = Total
        self.FillType = FillType
        self.OrderType = OrderType
"""
apikey = 'c4669cec85f945958ab58620e6e4897c'
apisecret = 'f60594c0fa514ef08dd832e0f2c1e606'
nonce = datetime.datetime.now()

#####################################
def MarketExplorer():
# generic market Exploration block
# to be executed as a separate thread runing every hour.
    while True:
        print(str(datetime.datetime.now()) + ": staring MarketExplorer()")
        allMarkets = getMarkets()
        BTCMarkets = getBTCMarkets(allMarkets)
        updateMarketNames(BTCMarkets)
        sleep(600)
#####################################
#print(marketNames[1])

def updateBittrexMarketHistory():
    newMarketHistory=[]
    for i in marketNames:
        jsonMarketHistory = getMarketHistory(i)
        for i in jsonMarketHistory:
            newMarketHistory.append(transformTransactionToTuple(i))
        marketHistory = newMarketHistory


def pushMarketHistoryToInflux(listHistory):
    print(str(datetime.datetime.now()) + ": starting pushMarketHistoryToInflux")
    for entry in listHistory:
        try:
            client.write_points(formJSONBodyFromHistoricalTransaction("marketHistory", entry))
        except influxdb.exceptions.InfluxDBServerError as e:
            print("InfluxDBServerError :" + str(e))
def recordMarketHistory(market):
    pushMarketHistoryToInflux(getMarketHistory(market))


def updateMarketHistories():
    while True:
        localMarketNames = marketNames
        if(len(localMarketNames) >= 1):
            marketsUpdateTimestart = time()
            for i in localMarketNames:
                print(str(datetime.datetime.now()) + ": saving data for market " + i)
                recordMarketHistory(i)
            marketsUpdateTimeEnd = time()
            #finish time
            print(str(datetime.datetime.now()) + ": market history Loop finished in " + str(marketsUpdateTimeEnd - marketsUpdateTimestart) + " seconds")
        elif(len(localMarketNames) == 0 ):
            print(str(datetime.datetime.now()) + "no markets present. Init Phase?")
            sleep(1)

client = InfluxDBClient(influxhost, influxport, influxuser , influxpassword, 'bittrex')
thread1 = threading.Thread(target = MarketExplorer)
thread2 = threading.Thread(target = updateMarketHistories)

thread1.start()
thread2.start()

"""

for i in BTCMarkets:
    markets.append(singleMarket(i['MarketCurrency'],
                    i['BaseCurrency'],
                    i['MarketCurrencyLong'],
                    i['BaseCurrencyLong'],
                    i['MinTradeSize'],
                    i['MarketName'],
                    i['IsActive'],
                    i['Created'],
                    i['Notice'],
                    i['IsSponsored'],
                    i['LogoUrl']))
"""