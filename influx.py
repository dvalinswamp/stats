from influxdb import *
import json
from datetime import datetime, timedelta
import statistics
from time import sleep, time
from logmod import *


influxhost = '165.227.155.203'
influxport = "8086"
influxuser = "explorer"
influxpassword = "timeseries4days"

def initDB():
    global client
    client= InfluxDBClient(influxhost, influxport, influxuser, influxpassword, 'bittrex')


def pushMarketHistoryToInflux(market, listHistory):
    logger.info("starting pushMarketHistoryToInflux for market: " + market)
    for entry in listHistory:
        try:
            client.write_points(formJSONBodyFromHistoricalTransaction(market, "marketHistory", entry))
        except influxdb.exceptions.InfluxDBServerError as e:
            logger.error("InfluxDBServerError :" + str(e))


def formJSONBodyFromHistoricalTransaction(market, typpe, val):
    jsonBody = [
    {
        "measurement": typpe,
        "tags": {
            'fillType': val['FillType'],
            'orderType': val['OrderType'],
            'market': market
        },
        "time": val['TimeStamp'],
        "fields": {
            'Quantity':val['Quantity'],
            'Price':val['Price'],
            'Total':val['Total'],
        }
    }
    ]
    return jsonBody

def formJSONBodyForSTDevAndVolume(market, stdev, volume):
    jsonBody = [
        {
            "measurement": 'stdevAndVolume',
            "tags": {
                'market': market
            },
            "time": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
            "fields": {
                'stDev': stdev,
                'volume': volume
            }
        }
    ]
    return jsonBody


def selectFromMarketHistory(market, type, starttime):
    q = client.query("SELECT * from marketHistory  WHERE \"market\" = '" +
                     market + "' and time >= \'" + starttime + "\' and orderType = '" + type + "'")
    return q

def selectFromSTDevHistory(market, starttime):
    q = client.query("SELECT * from stdevAndVolume  WHERE \"market\" = '" +
                     market + "' and time >= \'" + starttime + "\' and orderType = '" + type + "'")
    return q

def updateSellSTdevAndVolumeOver10minutes(market):
    sellsPrices = []
    sellsVolume = 0
    tenMinsAgo = (datetime.utcnow() - timedelta(minutes=10)).strftime('%Y-%m-%dT%H:%M:%SZ')
    tenMinHistory = selectFromMarketHistory(market, "SELL", tenMinsAgo)
    for x in tenMinHistory.get_points():
        sellsPrices.append(x['Price'])
        sellsVolume += x['Total']
    try:
        stdev = statistics.stdev(sellsPrices)
        client.write_points(formJSONBodyForSTDevAndVolume(market, stdev, sellsVolume))

    except statistics.StatisticsError as e:
        logger.error("Statistics error: " + str(e))
        logger.error("Statistics error. 10 minute order count: " + str(len(sellsPrices)))


#####testin section
'''
markets = ["BTC-LTC"]
'''



