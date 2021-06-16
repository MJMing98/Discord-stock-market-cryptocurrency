import discord
import discord.ext.commands as dec
from discord import member
from discord import message
from discord.ext.commands import bot
from financeCog import News, Crypto, StockMarket

# Allow intents on new members
intents = discord.Intents.default()
intents.members = True

discClient = dec.Bot(command_prefix="!")

# Called when the bot is ready for use
@discClient.event
async def on_ready():
    print(f'We have logged in as {discClient.user} - {discClient.user.id}')

# Create an event for when the bot receives a message
@discClient.command(
    name="welcome",
    case_insensitive = True,
    pass_context = True
)
async def initResponse(ctx):
    await ctx.send("Hi, my name is {}, how may I help?".format(discClient.user))

# Create bot instance
if __name__ == "__main__":
    with open("botKey.key") as key:
        token = key.read()

    discClient.add_cog(StockMarket(discClient))
    discClient.add_cog(News(discClient))
    discClient.add_cog(Crypto(discClient))

    discClient.run(token, bot = True, reconnect=True)

    

