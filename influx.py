from influxdb import *
import json


def formJSONBodyFromHistoricalTransaction(typpe, val):
    jsonBody = [
    {
        "measurement": typpe,
        "tags": {
            'fillType': val['FillType'],
            'orderType': val['OrderType']
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
