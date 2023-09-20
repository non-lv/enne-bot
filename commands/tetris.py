import discord
from discord import app_commands
from discord.ext.commands import Bot
from commands._tetris import model as game

def init(client: Bot):
    @client.tree.command(name="tetris", description='Let\'s play Tetris')
    async def tetris(interaction: discord.Interaction):
        await game.init(interaction)