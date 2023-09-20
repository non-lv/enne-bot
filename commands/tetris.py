import discord
from discord.ext.commands import Bot

from commands._tetris import BoardControll as game


def init(client: Bot):
    @client.tree.command(name="tetris", description='Let\'s play Tetris')
    async def tetris(interaction: discord.Interaction):
        bc = game.BoardControll()
        await bc.gameLoop(interaction)