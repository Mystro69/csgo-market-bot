import json
from datetime import datetime
import time
from nacl.bindings import crypto_sign
import requests
from urllib.parse import quote

minPercentage = 5.0
rootApiUrl = "https://api.dmarket.com"

def calc_discount(steamPrice,marketPrice):
    return 100 - (marketPrice / steamPrice * 100)

def get_offer_from_market(cursor):
    market_response = requests.get(rootApiUrl + "/exchange/v1/market/items?gameId=a8db&limit=100&currency=USD&cursor=" + cursor)
    offers = json.loads(market_response.text)["objects"]
    cursor = json.loads(market_response.text)["cursor"]
    return offers,cursor

itemPrices = {}
def get_steam_price(itemName):
    if itemPrices.get(itemName):
        print("already exists:" + itemName)
        return itemPrices.get(itemName)
    else:
        time.sleep(4.0)
        url = "https://steamcommunity.com/market/priceoverview/?appid=730&currency=1&market_hash_name=" + quote(itemName)
        request = requests.get(url)
        jsonBody = json.loads(request.text)
        try:
            value = float((jsonBody["lowest_price"])[1:])
            itemPrices.update({itemName: value})
            return value
        except:
            itemPrices.update({itemName: 0.01})
            print("return 0.01")
            return 0.01

#print(get_steam_price("Rio 2022 Dust II Souvenir Package"))

finished = False
amount = 1
offers, cursor = get_offer_from_market("")
while not finished:
    for v in offers:
        steamPrice = get_steam_price(v["title"])
        discount = calc_discount(steamPrice, float(v["price"]["USD"])/100)
        if discount > minPercentage:
            print(v["title"])
            print("\tSteam price: $" + str(steamPrice))
            print("\tDMarket price: $" + str(int(v["price"]["USD"]) / 100) + " (%" + str("%0.2f" % discount) + ")")
            print("\tBuy: https://dmarket.com/ingame-items/item-list/csgo-skins?userOfferId=" + v["extra"]["linkId"])

    offers, cursor = get_offer_from_market(cursor)
    
    if amount > 1000:
        finished = True

    amount+=1

while True:
    0-0