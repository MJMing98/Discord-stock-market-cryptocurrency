import cbpro
import discord.ext.commands as dec
from discord import TextChannel, GroupChannel, Member, Game
from twelvedata import TDClient
import stockmarketKey
import botKey

# Import keys for 12Data and Coinbase pro
smkey = stockmarketKey.SMkey
key = botKey.key

# Cryptocurrency cog
class Crypto(dec.Cog):
    "Cog for cryptocurrency"

    def __init__(self, bot):
        
        self.bot = bot
        
        # Create public coinbase pro client instance
        cbproClient = cbpro.PublicClient()

    # Example would be 'BTC-GBP'
    async def crypto(self, ctx, cbproClient, cryptoID):
       
        await ctx.send("Please input valid cryptoID (example, BTC-GBP)!")
       
        cryptoResponse = cbproClient.get_product_24hr_stats(str(cryptoID))
        #jsonCryptoData = json.loads(cryptoResponse.text)
        quote = 'Current ' + str(cryptoID) + ' price: £' + cryptoResponse['open']
        await ctx.send(quote)
        
        return

# Stock market cog
class StockMarket(dec.Cog):
    "Cog for stock markets"

    def __init__(self, bot):

        self.bot = bot

        twelvedataClient = TDClient(smkey)


'''

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
            
            if element['status'] == "online":
                availArr.append()
            else:
                continue

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

'''
