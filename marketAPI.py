#!/usr/bin/env python3

import discord
import requests
import json
import re
import math

scrape_url = 'https://finance.yahoo.com/quote'


def get_basic_quote(ticker: str) -> discord.Embed:
    ticker_url = "{}/{}".format(scrape_url, ticker)
    data = get_json(ticker_url)

    price_data = data.get('price')
    price = '{0:.2f}'.format(price_data.get('regularMarketPrice'))
    change = price_data.get('regularMarketChange')
    change_str = "+" + '{0:.2f}'.format(change) if change > 0 else '{0:.2f}'.format(change)
    change_percent = price_data.get('regularMarketChangePercent') * 100
    change_percent_str = "+" + '{0:.2f}'.format(change_percent) if change > 0 else '{0:.2f}'.format(change_percent)
    color = 0x33cc33 if change >= 0 else 0xcc0000

    name_data = data.get('quoteType')
    company_name = name_data.get('longName')
    if company_name is None:
        company_name = name_data.get('shortName')
    if company_name is None:
        company_name = ""

    symbol = data.get('symbol')

    emojis = get_emojis(change_percent)

    title = "".join([company_name, " (", symbol, ")"])
    description = "".join(["**", price, "**",
                           " | ", change_str,
                           " (", change_percent_str, "%)",
                           emojis])

    return discord.Embed(title=title, url=ticker_url, description=description, color=color)


def get_json(url, proxy=None):
    html = requests.get(url=url, proxies=proxy).text
    if "QuoteSummaryStore" not in html:
        return {}

    json_str = html.split('root.App.main =')[1].split(
        '(this)')[0].split(';\n}')[0].strip()
    data = json.loads(json_str)[
        'context']['dispatcher']['stores']['QuoteSummaryStore']

    new_data = json.dumps(data).replace('{}', 'null')
    new_data = re.sub(
        r'\{[\'|\"]raw[\'|\"]:(.*?),(.*?)\}', r'\1', new_data)

    return json.loads(new_data)


def get_emojis(change_percent):
    emoji = "\N{THUMBS DOWN SIGN}" if change_percent < 0 else "\N{ROCKET}"
    res = ""

    for i in range(min(100, math.ceil(abs(change_percent)))):
        res += " " + emoji

    return res