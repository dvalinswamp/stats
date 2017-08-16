from influxdb import *
import json


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
