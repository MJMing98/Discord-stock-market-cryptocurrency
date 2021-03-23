import discord
import botKey

key = botKey.key

discClient = discord.Client()

# Called when the bot is ready for use
@discClient.event
async def onReady():

    # Code replaces 0 as the client object, so it becomes discClient.user
    print('We have logged in as {0.user}'.format(discClient))

# Create another event for when bot receives a message
# Keep in mind, we don't want the bot to respond to messages that are sent by the bot user aka us!
@discClient.event
async def onMessage(message):
    # Check the author of the message, if it's by us, return
    if message.author == discClient.user:
        return

    # Check if the message sent is a command (in this case, $hello command, which is user defined)
    if message.content.startswith('$hello'):
        await message.channel.send('Hello from bot!')


discClient.run(key)