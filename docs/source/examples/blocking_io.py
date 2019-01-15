import shitcord

import meme
import trio
from PIL import Image

client = shitcord.Client()


# In most cases, blocking doesn't even affect you.
# But for processes that are computationally expensive or heavy such as PIL
# should be executed using run_sync_in_worker_thread to avoid blocking.
# However, don't excessively use this for small shit.
def my_blocking_stuff():
    with Image.open("my_image.jpg") as image:
        deepfried_image = meme.deepfry(image)
        deepfried_image.save("my_meme.png")

    return 'Finished.'


@client.on('message')
async def on_message(message):
    if str(message).startswith('!wot'):
        # Demonstrating the power of run_sync_in_worker_thread
        result = await trio.run_sync_in_worker_thread(my_blocking_stuff)
        await message.respond(result)  # Sends 'Finished.'


client.start('Token')
