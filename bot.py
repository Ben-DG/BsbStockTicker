#!/usr/bin/env python3

import os
import re
import discord
import marketAPI as api
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()
pattern = re.compile("[$][A-Za-z]{1,10}[-][A-Za-z]{1,5}\\.[A-Za-z]{1,5}|[$[A-Za-z]{1,10}\\.[A-Za-z]{1,5}|[$][A-Za-z]{1,10}[-][A-Za-z]{1,5}|[$][A-Za-z]{1,5}")


@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    stocks = list(set(re.findall(pattern, message.content)))
    for stock in stocks:
        try:
            embed = api.get_basic_quote(stock[1:])
        except:
            continue
        await message.channel.send(embed=embed)


client.run(TOKEN)
