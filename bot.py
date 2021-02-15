# discord bot stuff
import os
import random
import discord
from dotenv import load_dotenv

# web scraper
import requests
from bs4 import BeautifulSoup as BS

# discord client
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
client = discord.Client()
bot = '!hermes'

# web scraper
source = "https://www.wikipedia.org/wiki/"

# menu
def printMenu():
    return "Hello, here are some things I can do:\n1. Look up something on Wikipedia" \
           "\n\t[EX: !hermes 1 What_To_Look_Up]"

# scrape wiki
def scrapeWiki(arguments):
    # handle the 2000 limit on discord message
    # connect to wikipedia
    request = requests.get(source+arguments[2])
    soup = BS(request.text, "html.parser")
    # store <p>
    response = []

    # get all <p> and store their content in response
    for p in soup.find_all("p"):
        text = p.get_text()
        text = text.replace("\n","")
        response.append(text)

    # get rid of the emtpy lines
    for i in response:
        if i == "" or i == "\n":
            response.remove(i)

    #return array to send in messages
    return response


@client.event
async def on_ready():

    guild = discord.utils.get(client.guilds, name=GUILD)

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == bot:
        await message.channel.send(printMenu())
    elif bot + ' 1' in message.content:
        # handle the 2000 limit on discord message
        m = message.content
        arguments = m.split()
        for p in scrapeWiki(arguments):
            if p != "":
                await message.channel.send(p)

client.run(TOKEN)
