from os import name
import discord.ext.commands as dec
from discord import TextChannel, GroupChannel, Member, Game
from discord.ext.commands.cog import Cog
from discord.ext.commands.core import check
from twelvedata import TDClient
import requests
from random import randint, choice
import asyncio

# Import keys for 12Data and Coinbase pro
with open("stockmarketKey.key") as StockKey:
    smkey = StockKey.read()

with open("botKey.key") as Botkey:
    key = Botkey.read()

with open("financeNews.key") as newsKey:
    financeKey = newsKey.read()

newsCountry = ['ae', 'ar', 'at','au','be','bg','br','ca','ch','cn','co','cu','cz','de','eg','fr','gb','gr','hk','hu','id','ie','il','in','it','jp','kr','lt','lv','ma','mx','my','ng','nl','no','nz','ph','pl','pt','ro','rs','ru','sa','se','sg','si','sk','th','tr','tw','ua','us','ve','za']
newsSortBy = ['relevancy', 'popularity', 'publishedAt']

# Finance news cog
class News(dec.Cog):

    def __init__(self, bot):

        self.bot = bot

    @dec.group(
        name='news',
        invoke_without_command=True,
        pass_context = True,
        usage=['inputs']
    )

    async def printNewsRoot(self, ctx, input = "empty"):

        if input == "empty":

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

        else:
            lang = 'en'
            randSortBy = choice(newsSortBy)
            randCate = 'business' if randint(1,10) % 2 == 1 else 'technology'
            randPageSize = randint(2,100)

            url = ('https://newsapi.org/v2/everything?q={inputPlaceholder}&language={inputLang}&sortBy={inputSortBy}&pageSize={inputPageSize}&apiKey={apikey}'.format(inputPlaceholder = input.strip(), inputLang = lang, inputSortBy = randSortBy, inputPageSize = randPageSize, apikey = financeKey))
            response = requests.get(url).json()

            singleArticle = response['articles']

            randArticleIdx = randint(1, randPageSize)

            article = singleArticle[randArticleIdx]
            articleTitle = article['title']
            articleDescription = article['description']
            articleURL = article['url']
            
            await ctx.send("Title: " + articleTitle)
            await ctx.send(articleDescription)
            await ctx.send("URL: " + articleURL)

# Cryptocurrency cog
class Crypto(dec.Cog):
    '''Cog for cryptocurrency'''

    def __init__(self, bot):
        
        self.bot = bot

    @dec.group(
        name='crypto',
        case_insensitive=True,
        invoke_without_command=True,
        pass_context=True,
        usage = ['cryptoInputs']
    )

    # Example would be 'BTC-GBP'
    async def crypto(self, ctx, *input):
        
        if ctx.invoked_subcommand is not None:
            return

        if not input:

            # Creates a checking function, returns author and channel names from context and assigns it to our received msg
            # Done so that the bot only responds to the user that invoked the function
            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel

            await ctx.send("Please input cryptocurrency keyword (e.g. BTC or ETH)!")
            cryptoKeyword = await self.bot.wait_for('message', check=check)

            await ctx.send("Please input currency keyword (e.g. USD or GBP)!")
            currencyKeyword = await self.bot.wait_for('message', check=check)

            cryptoID = str(cryptoKeyword.content.strip().rstrip(".")) + "-" + str(currencyKeyword.content.strip().rstrip("."))
            del cryptoKeyword
            del currencyKeyword

            try:
                url = ('https://api.coinbase.com/v2/prices/{inputKeyword}/spot'.format(inputKeyword = cryptoID))
                response = requests.get(url)
                response.raise_for_status()
                data = (response.json())['data']

                quote = 'Current stock ' + cryptoID + ' price: ' + data["currency"] + data['amount']
                await ctx.send(quote)

            # Error handling for HTTP requests
            except requests.HTTPError as exception:
                print(exception)
                
                # Obtain first character from exception, which is the statuscode
                statusCode = str(exception).split()[0]

                if statusCode == '400':

                    error = str(exception).split(': ', 2)
                    errorMsg = error[1]
                    
                    async with ctx.typing():
                        await ctx.send("Keywords not found! Make sure the spelling is correct and the keyword for the wanted currency is valid!")
                        await asyncio.sleep(2)

                # Internal server error 
                elif statusCode == '500':
                    
                    async with ctx.typing():
                        await ctx.send("Oops! Server is down, please try again later!")
                        await asyncio.sleep(2)

        else:
            
            # input argument returns a list
            cryptoKeyword = input[0]
            currencyKeyword = input[1]
            
            cryptoID = cryptoKeyword + '-' + currencyKeyword
            try:
                # URL format of HTTPs request
                url = ('https://api.coinbase.com/v2/prices/{inputKeyword}/spot'.format(inputKeyword = cryptoID))
                response = requests.get(url)

                # Check status from the returned response, enter except loop if returned response has an error message
                response.raise_for_status()

                # Returns the object form of the returned JSON response, and have the bot print out the final prices
                data = (response.json())['data']

                quote = 'Current stock ' + cryptoID + ' price: ' + data["currency"] + data['amount']
                await ctx.send(quote)
            
            # Error handling for HTTP requests
            except requests.HTTPError as exception:
                print(exception)
                
                # Obtain first character from exception, which is the statuscode
                statusCode = str(exception).split()[0]

                # Client error, most probably caused by typo for currency
                if statusCode == '400':

                    error = str(exception).split(': ', 2)
                    errorMsg = error[1]
                    
                    async with ctx.typing():
                        await ctx.send("Keywords not found! Make sure the spelling is correct and the keyword for the wanted currency is valid!")
                        await asyncio.sleep(2)

                # Internal server error 
                elif statusCode == '500':
                    
                    async with ctx.typing():
                        await ctx.send("Oops! Server is down, please try again later!")
                        await asyncio.sleep(2)

    @crypto.command(
        name="help",
        pass_context=True,
        case_insensitive=True,
        invoke_without_command=True,
        aliases = ['h']
    )
            
    async def help(self, ctx):
        async with ctx.typing():
            await asyncio.sleep(0.75)
        await ctx.send("The !crypto command is used to check for cryptocurrency prices!")
        await ctx.send("Here are the available native currencies that are supported by the bot:")

        async with ctx.typing():
            currencyList = []
            url = ('https://api.coinbase.com/v2/currencies')
            response = requests.get(url).json()

            for dict in response['data']:
                currencyList.append(str(dict['name'] + ": " + dict['id']))

            await asyncio.sleep(1.5)
        
        print(currencyList)

        firstHalf = currencyList[:int(len(currencyList)/2)]
        secondHalf = currencyList[int(len(currencyList)/2):]

        await ctx.send('\n'.join(firstHalf))
        await ctx.send('\n'.join(secondHalf))

        await ctx.send("First input in a crytpcurrency keyword, then the currency keyword to obtain the current market pair list price.")
        await ctx.send("Example: !crypto BTC GBP")

# Stock market cog
class StockMarket(dec.Cog):
    """Cog for stock markets"""

    def __init__(self, bot):

        self.bot = bot

    @dec.group(
        name='stock',
        case_insensitive=True,
        invoke_without_command=True,
        pass_context=True,
        usage = ['stockInputs']
    )

    async def stock(self, ctx, *inputs):
        
        if ctx.invoked_subcommand is not None:
            return

        if input:
            print("Do something")
            # QUERY API FOR DATA
        
        else:
            print("Do something")
            # QUERY API FOR DATA WITHOUT ANY INPUTS
    