import discord
from discord.ext import commands
import commands.init as commands
import os
from dotenv import load_dotenv

def run():
    load_dotenv()

    intent = discord.Intents.default()
    intent.message_content = True
    client = commands.Bot(command_prefix='', intents=intent)

    @client.event
    async def on_ready():
        print(f'{client.user} going full speed.')

        try: 
            synced = await client.tree.sync()
            print(f"Synced {len(synced)} command(s)")
        except Exception as e:
            print(e)

    commands.init(client)

    client.run(os.getenv('TOKEN'))

if __name__ == '__main__':
    run()