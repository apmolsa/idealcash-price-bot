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

def price():
  response = requests.get('https://api.crex24.com/v2/public/tickers?instrument=DEAL-BTC')
  data = response.json()[0]
  last = '{:.8f}'.format(data['last'])
  change = data['percentChange']
  ask = '{:.8f}'.format(data['ask'])
  bid = '{:.8f}'.format(data['bid'])
  volume = data['volumeInBtc']

  priceInfo = '''\
  ---------------------------------------------------
  BUY DEAL FROM:
  https://crex24.com/exchange/DEAL-BTC
  ---------------------------------------------------
  PRICE: {0} BTC
  CHANGE: {1}%
  SELL: {2} BTC
  BUY: {3} BTC
  ---------------------------------------------------'''.format(last, change, ask, bid)
  bot.send_message(chat_id=update.message.chat_id, text=priceInfo)

from telegram.ext import CommandHandler

price_handler = CommandHandler('price', price)
dispatcher.add_handler(price_handler)

updater.start_polling()

