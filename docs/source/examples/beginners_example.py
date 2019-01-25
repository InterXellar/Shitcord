import shitcord

client = shitcord.Client(SomeConfig())


@client.on('message')
async def on_message(message):
    if 'owo' in str(message).lower():
        await message.respond("What's This?")


client.start()
