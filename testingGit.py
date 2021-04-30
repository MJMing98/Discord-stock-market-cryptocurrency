import discord
import botKey
import cbpro
import requests
import json
import string
import stockmarketKey
from twelvedata import TDClient
import discord.ext.commands as dec
from discord import Member

smkey = stockmarketKey.SMkey
key = botKey.key

# Create bot instance
discClient = dec.Bot(command_prefix="!")
if __name__ == "__main__":
    with open("botKey.key") as key:
        token = key.read()

    discClient.run(token, reconnect=True)

# Create twelveData client instance
smClient = TDClient(smkey)

# Create public coinbase pro client instance
cbproClient = cbpro.PublicClient()

# Called when the bot is ready for use
@discClient.event
async def on_ready():
    print('We have logged in as {discClient.user}')

# Called when new members join the channel
@discClient.event
async def on_member_join(Member):
    await message.channel.send('Welcome to the channel, {}!'.format(Member.name))

# Create an event for when the bot receives a message
@discClient.command(
    name="help"
)
async def initResponse(ctx):
    await ctx.send("Hi, my name is {}, how may I help?".format(discClient.name))
    

# Create another event for when bot receives a message
# Keep in mind, we don't want the bot to respond to messages that are sent by the bot user aka us!
@discClient.event
async def on_message(message):
    # Check the author of the message, if it's by us, return
    if message.author == discClient.user:
        return

    # Check if the message sent is a command (in this case, $hello command, which is user defined)
    if message.content.startswith('$hello'):
        await message.channel.send('Hello from bot!')

    if message.content.startswith('$currency'):
        await message.channel.send("Here are the currencies that are available to trade on Coinbase Pro:")
        response = cbproClient.get_currencies()
        availArr = []
        for element in response:
            
            status = element["display_name"]
            print(element[status])
            
            '''
            if element['status'] == "online":
                availArr.append()
            else:
                continue
            '''
        await message.channel.send(availArr)
        

    if message.content.startswith('$BTC-GBP'):
        currentPrice = crypto('BTC-GBP')
        await message.channel.send(currentPrice)

# Example would be 'BTC-GBP'
def crypto(cryptoID):
        cryptoResponse = cbproClient.get_product_24hr_stats(str(cryptoID))
        #jsonCryptoData = json.loads(cryptoResponse.text)
        quote = 'Current ' + str(cryptoID) + ' price: £' + cryptoResponse['open']
        return(quote)


discClient.run(key)