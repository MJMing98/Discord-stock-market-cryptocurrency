from os import name
import cbpro
import discord.ext.commands as dec
from discord import TextChannel, GroupChannel, Member, Game
from discord.ext.commands.cog import Cog
from discord.ext.commands.core import check
from twelvedata import TDClient
import requests
from random import randint

# Import keys for 12Data and Coinbase pro
with open("stockmarketKey.key") as StockKey:
    smkey = StockKey.read()

with open("botKey.key") as Botkey:
    key = Botkey.read()

with open("financeNews.key") as newsKey:
    financeKey = newsKey.read()

newsCountry = ['ae', 'ar', 'at','au','be','bg','br','ca','ch','cn','co','cu','cz','de','eg','fr','gb','gr','hk','hu','id','ie','il','in','it','jp','kr','lt','lv','ma','mx','my','ng','nl','no','nz','ph','pl','pt','ro','rs','ru','sa','se','sg','si','sk','th','tr','tw','ua','us','ve','za']
#newsCate = ['business', 'entertainment', 'general', 'health', 'science', 'technology', 'sports']
#newsSources = ['bbc-news', 'independent', 'bloomberg']

# Finance news cog
class News(dec.Cog):

    def __init__(self, bot):

        self.bot = bot

    @dec.command(
        name='advice'
    )

    async def printAdvice(self, ctx):

        # Generate random number for country and params for top story get
        #randCountry = choice(newsCountry)
        # Can't run sources parameter if using either country or category!
        randCountry = 'gb' if randint(1,10) % 2 == 1 else 'us'
        randCate = 'business' if randint(1,10) % 2 == 1 else 'technology'
        randPageSize = randint(2,100)

        url = ('https://newsapi.org/v2/top-headlines?country={inputCountry}&pageSize={inputPageSize}&category={inputCategory}&apiKey={apikey}'.format(inputCountry = randCountry, inputCategory = randCate, inputPageSize = randPageSize, apikey = financeKey))
        response = requests.get(url).json()

        singleArticle = response['articles']

        randArticleIdx = randint(1, randPageSize)

        article = singleArticle[randArticleIdx]
        articleTitle = article['title']
        articleDescription = article['description']
        articleURL = article['url']
        
        await ctx.send("Title: " + articleTitle)
        await ctx.send("Description: " + articleDescription)
        await ctx.send("URL: " + articleURL)


'''
# Cryptocurrency cog
class Crypto(dec.Cog):
    Cog for cryptocurrency'''
'''
    def __init__(self, bot):
        
        self.bot = bot
        
        # Create public coinbase pro client instance
        cbproClient = cbpro.PublicClient()

    @dec.group(
        name='crypto',
        case_insensitive=True,
        invoke_without_command=True,
        pass_context=True
    )

    # Example would be 'BTC-GBP'
    async def crypto(self, ctx, cbproClient):
        
        # Creates a checking function, returns author and channel names from context and assigns it to our received msg
        # Done so that the bot only responds to the user that invoked the function
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        await ctx.send("Please input cryptocurrency keyword (e.g. BTC or ETC)!")
        cryptoKeyword = await self.bot.wait_for('message', check=check)

        await ctx.send("Please input currency keyword (e.g. USD or GBP)!")
        currencyKeyword = await self.bot.wait_for('message', check=check)

        cryptoID = cryptoKeyword + "-" + currencyKeyword
        del cryptoKeyword
        del currencyKeyword

        cryptoResponse = cbproClient.get_product_24hr_stats(cryptoID)
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
