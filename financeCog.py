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

    async def printNewsRoot(self, ctx, *input):

        if len(input) < 1:

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
            
            await ctx.reply("Title: " + articleTitle + "\nDescription: " + articleDescription + "\nURL: " + articleURL)

        else:
            lang = 'en'
            randSortBy = choice(newsSortBy)
            randCate = 'business' if randint(1,10) % 2 == 1 else 'technology'
            randPageSize = randint(2,100)

            processedString = "-".join(input)

            url = ('https://newsapi.org/v2/everything?q={inputPlaceholder}&language={inputLang}&sortBy={inputSortBy}&pageSize={inputPageSize}&apiKey={apikey}'.format(inputPlaceholder = processedString, inputLang = lang, inputSortBy = randSortBy, inputPageSize = randPageSize, apikey = financeKey))
            response = requests.get(url).json()

            singleArticle = response['articles']

            randArticleIdx = randint(1, randPageSize)

            article = singleArticle[randArticleIdx]
            articleTitle = article['title']
            articleDescription = article['description']
            articleURL = article['url']
            
            await ctx.reply("Title: " + articleTitle + "\nDescription: " + articleDescription + "\nURL: " + articleURL)

    @printNewsRoot.command(
        name="help",
        pass_context=True,
        case_insensitive=True,
        invoke_without_command=True,
        aliases = ['h']
    )

    async def help(self, ctx):

        with ctx.typing():
            await asyncio.sleep(1)
            await ctx.reply("The news command makes the bot print out news article that are of interest to the user.\nSimply type !news and the bot will print out new business and technology related news articles.\nThe bot can also search up news based on input keywords, for example try \"!news AMZN\" for news related to Amazon's stock or try \"!news Elon Musk\" for news about Elon Musk!")


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

        if len(input) != 2 and len(input) != 0:

            await ctx.reply("2 arguments accepted only: 1 keyword for cryptocurrency, 1 for native/base currency!")
            return

        if not input:

            # Creates a checking function, returns author and channel names from context and assigns it to our received msg
            # Done so that the bot only responds to the user that invoked the function
            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel

            await ctx.reply("Please input cryptocurrency keyword (e.g. BTC or ETH)!")
            cryptoKeyword = await self.bot.wait_for('message', check=check)

            await ctx.reply("Please input currency keyword (e.g. USD or GBP)!")
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
                await ctx.reply(quote)

            # Error handling for HTTP requests
            except requests.HTTPError as exception:
                print(exception)
                
                # Obtain first character from exception, which is the statuscode
                statusCode = str(exception).split()[0]

                if statusCode == '400':
                    
                    await ctx.reply("Keywords not found! Make sure the spelling is correct and the keyword for the wanted currency is valid!")

                # Internal server error 
                elif statusCode == '500':
                    
                    await ctx.reply("Oops! Server is down, please try again later!")

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
                await ctx.reply(quote)
            
            # Error handling for HTTP requests
            except requests.HTTPError as exception:
                print(exception)
                
                # Obtain first character from exception, which is the statuscode
                statusCode = str(exception).split()[0]

                # Client error, most probably caused by typo for currency
                if statusCode == '400' or '404':
                    
                    await ctx.reply("Keywords not found! Make sure the spelling is correct and the keyword for the wanted currency is valid!")

                # Internal server error 
                elif statusCode == '500':
                    
                    await ctx.reply("Oops! Server is down, please try again later!")

    @crypto.command(
        name="help",
        pass_context=True,
        case_insensitive=True,
        invoke_without_command=True,
        aliases = ['h']
    )
            
    async def help(self, ctx):

        with ctx.typing():
            await asyncio.sleep(0.75)

            await ctx.reply("The !crypto command is used to check for cryptocurrency prices!\nHere are the available native currencies that are supported by the bot:\n")
            currencyList = []
            url = ('https://api.coinbase.com/v2/currencies')
            response = requests.get(url).json()

            for dict in response['data']:
                currencyList.append(str(dict['name'] + ": " + dict['id']))

            await asyncio.sleep(1.5)
        
            firstHalf = currencyList[:int(len(currencyList)/2)]
            secondHalf = currencyList[int(len(currencyList)/2):]

            await ctx.send('\n'.join(firstHalf) + '\n'.join(secondHalf) + 
                            "First input is a cryptocurrency keyword, then the currency keyword to obtain the current market pair list price. \
                            \nExample: !crypto BTC GBP")

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

        if len(inputs) != 2 and len(inputs) != 0:

            await ctx.reply("2 arguments accepted only: 1 for stock market keyword, 1 for native/base currency!")
            return

        if inputs:
                        
            # input argument returns a list
            stockKeyword = inputs[0]
            currencyKeyword = inputs[1]
                
            try:
                # URL format of HTTPs request
                urlSymbol = ("https://api.twelvedata.com/symbol_search?symbol={inputKeyword}".format(inputKeyword = stockKeyword))
                responseSymbol = requests.get(urlSymbol)

                # Check status from the returned response, enter except loop if returned response has an error message
                responseSymbol.raise_for_status()

                #Returns the object form of the returned JSON response, and obtain symbol data
                dataSymbol = next((exchange for exchange in responseSymbol.json()['data'] if exchange['country'] == 'United States'))

                #dataSymbol = (responseSymbol.json())['data'] if (responseSymbol.json())['data']
                stockExchange = dataSymbol["exchange"]

                # First request for stock data
                urlStock = ("https://api.twelvedata.com/time_series?symbol={inputKeyword}&exchange={inputExchange}&interval=1min&outputsize=1&apikey={inputApiKey}".format(inputKeyword = stockKeyword, inputExchange = stockExchange, inputApiKey = smkey))
                responseStock = requests.get(urlStock)

                # Check status from the returned response, enter except loop if returned response has an error message
                responseStock.raise_for_status()
                dataStock = (responseStock.json())['values'][0]
                
                dataExchangeRate = 1

                # TwelveData API runs on USD by default, so if the input data is not USD, we can query an exchange rate and multiply
                # the queried exchange rate together with the price for the queried stock to change the currency
                if currencyKeyword != "USD":
                    urlExchangeRate = ("https://api.twelvedata.com/exchange_rate?symbol=USD/{inputCurrency}&apikey={inputApiKey}".format(inputCurrency = currencyKeyword, inputApiKey = smkey))
                    responseExchangeRate = requests.get(urlExchangeRate)
                    responseExchangeRate.raise_for_status()

                    # Do the same thing for exchange rate
                    dataExchangeRate = (responseExchangeRate.json())['rate']

                newPrice = float(dataStock['close']) * dataExchangeRate

                quote = 'Current stock ' + stockKeyword + ' price: ' + currencyKeyword + str(newPrice)
                await ctx.reply(quote)

            except StopIteration:
                await ctx.reply("Keywords not found! Bot can only process US stock market data!")
            
            # Error handling for HTTP requests
            except requests.HTTPError as exception:
                print(exception)
                
                # Obtain first character from exception, which is the statuscode
                statusCode = str(exception).split()[0]

                # Client error, most probably caused by typo for currency
                if statusCode == '400':

                    error = str(exception).split(': ', 2)
                    errorMsg = error[1]
                    
                    await ctx.reply("Keywords not found! Make sure the spelling is correct and the keyword for the wanted currency is valid!")

                # Internal server error 
                elif statusCode == '500':
                    
                    await ctx.reply("Oops! Server is down, please try again later!")
                
                # Too many requests error 
                elif statusCode == '429':
                    
                    await ctx.reply("Oops! Too many requests have been made, please try again tomorrow!")
            
        else:
            # Creates a checking function, returns author and channel names from context and assigns it to our received msg
            # Done so that the bot only responds to the user that invoked the function
            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel

            await ctx.reply("Please input stock keyword (e.g. AAPL for Apple or GOOG for Google)!")
            stockKeyword = await self.bot.wait_for('message', check=check)

            await ctx.reply("Please input currency keyword (e.g. USD or GBP)!")
            currencyKeyword = await self.bot.wait_for('message', check=check)

            try:
                # URL format of HTTPs request
                # With stock market, it's a little different because different stock symbols use different indices
                # So, first obtain the index for the queries symbol
                urlSymbol = ("https://api.twelvedata.com/symbol_search?symbol={inputKeyword}".format(inputKeyword = stockKeyword))
                responseSymbol = requests.get(urlSymbol)

                # Check status from the returned response, enter except loop if returned response has an error message
                responseSymbol.raise_for_status()

                #Returns the object form of the returned JSON response, and obtain symbol data
                dataSymbol = next((exchange for exchange in responseSymbol.json()['data'] if exchange['country'] == 'United States'))

                #dataSymbol = (responseSymbol.json())['data'] if (responseSymbol.json())['data']
                stockExchange = dataSymbol["exchange"]

                # Now request for stock data
                urlStock = ("https://api.twelvedata.com/time_series?symbol={inputKeyword}&exchange={inputExchange}&interval=1min&outputsize=1&apikey={inputApiKey}".format(inputKeyword = stockKeyword, inputExchange = stockExchange, inputApiKey = smkey))
                responseStock = requests.get(urlStock)

                # Check status from the returned response
                responseStock.raise_for_status()
    
                # Returns the object form of the returned JSON response, and have the bot print out the final prices
                dataStock = (responseStock.json())['values'][0]
                
                dataExchangeRate = 1

                # TwelveData API runs on USD by default, so if the input data is not USD, we can query an exchange rate and multiply
                # the queried exchange rate together with the price for the queried stock to change the currency
                if currencyKeyword != "USD":
                    urlExchangeRate = ("https://api.twelvedata.com/exchange_rate?symbol=USD/{inputCurrency}&apikey={inputApiKey}".format(inputCurrency = currencyKeyword, inputApiKey = smkey))
                    responseExchangeRate = requests.get(urlExchangeRate)
                    responseExchangeRate.raise_for_status()

                    # Do the same thing for exchange rate
                    dataExchangeRate = (responseExchangeRate.json())['rate']

                newPrice = float(dataStock['close']) * dataExchangeRate

                quote = 'Current stock ' + stockKeyword + ' price: ' + currencyKeyword + str(newPrice)
                await ctx.reply(quote)

            except StopIteration:
                with ctx.typing():
                    await asyncio.sleep(0.5)
                    await ctx.reply("Keywords not found! Bot can only process US stock market data!")

            
            # Error handling for HTTP requests
            except requests.HTTPError as exception:
                print(exception)
                
                # Obtain first character from exception, which is the statuscode
                statusCode = str(exception).split()[0]

                # Client error, most probably caused by typo for currency
                if statusCode == '400':

                    error = str(exception).split(': ', 2)
                    errorMsg = error[1]
                    
                    await ctx.reply("Keywords not found! Make sure the spelling is correct and the keyword for the wanted currency is valid!")

                # Internal server error 
                elif statusCode == '500':
                    
                    await ctx.reply("Oops! Server is down, please try again later!")
                
                # Too many requests error 
                elif statusCode == '429':
                    
                    await ctx.reply("Oops! Too many requests have been made, please try again tomorrow!")

    @stock.command(
        name="help",
        pass_context=True,
        case_insensitive=True,
        invoke_without_command=True,
        aliases = ['h']
    )
            
    async def help1(self, ctx):
        with ctx.typing():
            await asyncio.sleep(1)

            indexList = []
            url = ('https://api.twelvedata.com/exchanges?country=us&type=stock')
            response = requests.get(url).json()['data']

            for dict in response:
                indexList.append(str(dict['name'] + ": " + dict['code']))

            await ctx.reply("The !stock command is used to check for stock prices! \
                            \nNote that since the bot is currently using the basic plan for TwelveData, only American stocks are available.\
                            \nHere are the available indices that are supported by the bot:\n" + '\n'.join(indexList) + 
                            "First input in a stock symbol, then the currency keyword to obtain the current market pair list price.\
                            \nExample: !stock AMZN GBP")
                            
    @dec.group(
        name="exchange",
        pass_context=True,
        case_insensitive=True,
        invoke_without_command=True,
        usage = ['currencyInputs']
    )
    
    async def exchange(self, ctx, *inputs):
        
        if len(inputs) != 2 and len(inputs) != 3:

            await ctx.reply("2 currency types are needed!")
            return

        #Obtain the values from the 
        currencyKeyword1 = inputs[0]
        currencyKeyword2 = inputs[1]

        # If third argument exists, let amount be that value, else it would be a 1:val currency exchange rate
        try:
            amount = inputs[2]
        except:
            amount = 1

        try:
            # Same thing as always, send a request to the API and convert the returned response to an object
            urlExchangeRate = ("https://api.twelvedata.com/currency_conversion?symbol={inputCurrency1}/{inputCurrency2}&amount={inputAmount}&apikey={inputApiKey}".format(inputCurrency1 = currencyKeyword1, inputCurrency2 = currencyKeyword2, inputAmount = amount, inputApiKey = smkey))
            responseExchangeRate = requests.get(urlExchangeRate)
            responseExchangeRate.raise_for_status()

            exchangeRateAmount = (responseExchangeRate.json())['amount']
            exchangeRateSymbol = (responseExchangeRate.json())['symbol']

            if amount == 1:
                await ctx.reply("Convertion rate for {} is {}1 to {}".format(exchangeRateSymbol, currencyKeyword1, currencyKeyword2 + str(exchangeRateAmount)))
            else:
                await ctx.reply("Convertion rate for {} is {} to {}".format(exchangeRateSymbol, currencyKeyword1 + amount, currencyKeyword2 + str(exchangeRateAmount)))

        # Error handling for HTTP requests
        except requests.HTTPError as exception:
            print(exception)
            
            # Obtain first character from exception, which is the statuscode
            statusCode = str(exception).split()[0]

            # Client error, most probably caused by typo for currency
            if statusCode == '400':

                error = str(exception).split(': ', 2)
                errorMsg = error[1]
                
                await ctx.reply("Keywords not found! Make sure the spelling is correct and the keyword for the wanted currency is valid!")

            # Internal server error 
            elif statusCode == '500':
                
                await ctx.reply("Oops! Server is down, please try again later!")
            
            # Too many requests error 
            elif statusCode == '429':
                
                await ctx.reply("Oops! Too many requests have been made, please try again tomorrow!")

    @exchange.command(
        name="help",
        pass_context=True,
        case_insensitive=True,
        invoke_without_command=True
    )

    async def help2(self, ctx):
        with ctx.typing():
            await asyncio.sleep(0.75)
            await ctx.reply("The !exchange command is used to check for currency exchange prices!\
                            \nNot only does it check conversion rates between different native currencies, but it also allows for conversion rates from cryptocurrency to native currency as well.\
                            \nFirst input in the current currency symbol, and then the desired currency symbol. An amount value can be added at the end as well, if not added the bot simply prints out the conversion rate between both currencies.\
                            \nExample: \"!exchange GBP MYR 500\" would convert 500 GBPs to MYRs")
