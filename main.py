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
import time

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
options.add_argument("user-data-dir=C:/Users/modib/AppData/Local/Google/Chrome/User Data/Default")
driver = uc.Chrome(options=options)
#endregion

def GetHelp() :
    mbd = discord.Embed(title="Help", color = Color.red())
    mbd.add_field(name = "Prefix before every command :", value = '`*`')
    mbd.add_field(name = "Boot the server :", value = '`<prefix>boot`')
    mbd.add_field(name = "Check status :", value = '`<prefix>check-status`')
    mbd.add_field(name = "Stop server :", value = '`<prefix>stop`')
    mbd.add_field(name = "Get Help :", value = '`<prefix>help`')
    return mbd

def RestartServer() :
    val = False
    driver.get('https://aternos.org/server/')
    Status = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.XPATH, '//*[@id="read-our-tos"]/main/section/div[3]/div[2]/div[1]/div/span[2]/span'))
    if Status.text == 'Online' :
        restartButton = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.XPATH, '//*[@id="restart"]'))
        restartButton.click()
        offline = False
        return offline
    elif Status.text == 'Offline' :
        offline = True
        return offline

def StopServer() :
    val = False
    driver.get('https://aternos.org/server/')
    Status = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.XPATH, '//*[@id="read-our-tos"]/main/section/div[3]/div[2]/div[1]/div/span[2]/span'))
    if Status.text == 'Online' :
        stopButton = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.XPATH, '//*[@id="stop"]'))
        stopButton.click()
        offline = False
        return offline
    elif Status.text == 'Offline' :
        offline = True
        return offline

def CheckStatus() :
    driver.get('https://aternos.org/server/')
    mbd = discord.Embed(title="Status", color = Color.red())
    Status = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.XPATH, '//*[@id="read-our-tos"]/main/section/div[3]/div[2]/div[1]/div/span[2]/span'))
    if Status.text == 'Online' :
        mbd = discord.Embed(title="Server is running :D", color = Color.green())
        Players = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.XPATH, '//*[@id="read-our-tos"]/main/section/div[3]/div[4]/div[3]/div[1]/div[1]/div[2]/div[2]'))
        mbd.add_field(name = "Players", value = Players.text)
    elif Status.text == 'Offline' :
        mbd = discord.Embed(title="Server is Offline :(", color = Color.red())
    else : 
        mbd = discord.Embed(title="Server is starting :D", color = Color.greyple())
    IPAddress = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.XPATH, '//*[@id="ip"]'))
    mbd.add_field(name = "IPddress", value = IPAddress.text)
    return mbd

def BootServer() :
    message = ''
    driver.get('https://aternos.org/server/')
    Status = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.XPATH, '//*[@id="read-our-tos"]/main/section/div[3]/div[2]/div[1]/div/span[2]/span'))
    if Status.text == 'Online' :
        message = 'no'
        return message
    elif Status.text == 'Offline' :
        startButton = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.XPATH, '//*[@id="start"]'))
        startButton.click()
        time.sleep(1)
        IPAddress = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.XPATH, '//*[@id="ip"]'))
        Software = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.XPATH, '//*[@id="software"]'))
        Version = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.XPATH, '//*[@id="version"]'))
        Status = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.XPATH, '//*[@id="read-our-tos"]/main/section/div[3]/div[2]/div[1]/div/span[2]/span'))
        #driver.add_cookie({'name': 'ATERNOS_SESSION', "value" : session, 'sameSite': 'Lax'})
        #driver.add_cookie({'name': 'ATERNOS_SERVER', "value" : server, 'sameSite': 'Lax'})
        #driver.add_cookie({'name': 'ATERNOS_GA', "value" : ga, 'sameSite': 'None'})
        mbd = discord.Embed(title="Server ", color = Color.dark_purple())
        mbd.add_field(name = "IPAddress", value = IPAddress.text)
        mbd.add_field(name = "Software", value = Software.text)
        mbd.add_field(name = "Version", value = Version.text)
        mbd.add_field(name = "Status", value = Status.text)
        return mbd
    else :
        message = 'error'

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
        await message.channel.send('Booting Server :D')
        mbd = BootServer()
        if mbd == 'no' :
            await message.channel.send('Server Already running :)')

        elif mbd == 'error' :
            await message.channel.send('An error has occured :(, pls contact admin with details, that would help you to get a special role :D, and at the same time help us to improve our bot :D')
        else :
            await message.channel.send(embed = mbd)

    if args[0] == 'stop' :
        await message.channel.send('Stopping Server :)')
        mbd = StopServer()
        if mbd == True :
            await message.channel.send('Server is already offline')
        elif mbd == False :
            await message.channel.send('Server has been shutdawn successfully')
    
    if args[0] == 'restart' :
        await message.channel.send('Restarting Server :)')
        mbd = StopServer()
    if mbd == True :
        await message.channel.send('Server is offline')
    elif mbd == False :
        await message.channel.send('Server restarting...')
    
    if args[0] == 'help' :
        mbd = GetHelp()
        await message.channel.send(embed = mbd)

    if args[0] == 'check-status' :
        await message.channel.send('Checking Status...')
        mbd = CheckStatus()
        await message.channel.send(embed = mbd)
        
client.run(TOKEN)