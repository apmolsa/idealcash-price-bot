#-*- coding: utf-8 -*-

import json
import codecs
import requests
from bs4 import BeautifulSoup, SoupStrainer
import re
import subprocess
from telegram.ext.dispatcher import run_async
from telegram.ext import Updater
from html import escape

updater = Updater(token='TGTOKEN')
dispatcher = updater.dispatcher

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
          level=logging.INFO)

def getCrexInfo():
  response = requests.get('https://api.crex24.com/v2/public/tickers?instrument=DEAL-BTC')
  data = response.json()[0]
  last = '{:.8f}'.format(data['last'])
  change = data['percentChange']
  ask = '{:.8f}'.format(data['ask'])
  bid = '{:.8f}'.format(data['bid'])

  return '''\
  -----------------------------------------------------------
  https://crex24.com/exchange/DEAL-BTC
  -----------------------------------------------------------
  PRICE: {0} BTC
  CHANGE: {1}%
  SELL: {2} BTC
  BUY: {3} BTC
  '''.format(last, change, ask, bid)

def getStocksInfo():
  response = requests.get('https://app.stocks.exchange/api2/ticker').json()
  data = '';
  for obj in response:
    for key in obj:
      if key == 'market_name' and obj[key] == 'DEAL_BTC':
        data = obj;

  last = data['last']
  ask = data['ask']
  bid = data['bid']
  change24 = data['lastDayAgo']

  change = float(last) / float(change24) * 100 - 100

  return '''\

  -----------------------------------------------------------
  https://app.stocks.exchange/en/basic-trade/pair/BTC/DEAL
  -----------------------------------------------------------
  PRICE: {0} BTC
  CHANGE: {1}%
  SELL: {2} BTC
  BUY: {3} BTC
  -----------------------------------------------------------'''.format(last, change, ask, bid)

def price():
  crex = getCrexInfo()
  stocks = getStocksInfo()
  priceInfo = crex + stocks

  bot.send_message(chat_id=update.message.chat_id, text=priceInfo)

from telegram.ext import CommandHandler

price_handler = CommandHandler('price', price)
dispatcher.add_handler(price_handler)

updater.start_polling()

