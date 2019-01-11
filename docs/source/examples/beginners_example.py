import shitcord

client = shitcord.Client()


@client.on('message')
async def on_message(message):
    if message.content.startswith('!ping'):
        await message.respond('Pong!')


client.start('Token')
