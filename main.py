import discord
import json
#from discord import app_commands
#from discord.ext import commands
#from discord_slash import commands, SlashCommand, SlashContext
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
#from discord import SlashCommand
from discord.ext import commands
import undetected_chromedriver as uc
from discord import Color

with open('C:/Users/modib/Documents/kali/py/AternosBOT/config.json') as f:
   data = json.load(f)

# region variables 
TOKEN = data["TOKEN"]
intents = discord.Intents.all()
intents.message_content = True
client = discord.Client(intents=intents)
#tree = app_commands.CommandTree(client)
PREFIX = "*"
bot = commands.Bot(command_prefix=PREFIX, intents=intents)
options = Options()
options.addArguments("user-data-dir=C:/Users/modib/AppData/Local/Google/Chrome/User Data/Default")
driver = uc.Chrome(options=options)
UNSNITISEDCHARS = '\'!?^~`:;{[}]+='
#endregion

def BootServer() :
    driver.get('https://aternos.org/server/')
    #driver.add_cookie({'name': 'ATERNOS_SESSION', "value" : session, 'sameSite': 'Lax'})
    #driver.add_cookie({'name': 'ATERNOS_SERVER', "value" : server, 'sameSite': 'Lax'})
    #driver.add_cookie({'name': 'ATERNOS_GA', "value" : ga, 'sameSite': 'None'})

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Minecraft"))

@client.event
async def on_message(message:discord.Message):
    if message.author.bot or not(str(message.content).startswith(PREFIX)):
        return
    args = message.content.split(" ")
    args[0] = args[0][1::]
    print(args)
    if args[0] == 'boot' :
        BootServer()

client.run(TOKEN)