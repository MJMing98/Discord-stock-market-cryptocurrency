import discord
import discord.ext.commands as dec
from discord import Member
from discord import message
from financeCog import News

'''
from financeCog import Crypto
from financeCog import StockMarket
'''

discClient = dec.Bot(command_prefix="!")

# Called when the bot is ready for use
@discClient.event
async def on_ready():
    print('We have logged in as {discClient.user}')

# Called when new members join the channel
@discClient.event
async def on_member_join(Member, ctx):
    "Introduces a member into the channel."
    await ctx.send('Welcome to the channel, {}!'.format(Member.name))

# Create an event for when the bot receives a message
@discClient.command(
    name="HelpMe"
)
async def initResponse(ctx):
    await ctx.send("Hi, my name is {}, how may I help?".format(discClient.user))

# Create bot instance
if __name__ == "__main__":
    with open("botKey.key") as key:
        token = key.read()

    # INSERT COGS HERE
    # Add cogs into main bot code
    '''
    discClient.add_cog(Crypto(discClient))
    discClient.add_cog(StockMarket(discClient))
    '''
    discClient.add_cog(News(discClient))

    discClient.run(token, reconnect=True)

    

