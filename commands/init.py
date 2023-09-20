from discord.ext.commands import Bot
from commands import tetris

def init(client: Bot):
    tetris.init(client)

    import discord
    @client.tree.command(name="test", description='Testing stuff')
    async def test(interaction: discord.Interaction):
        await interaction.response.send_message(f'lol')
        msg = await interaction.original_response()
        await msg.add_reaction('0️⃣')
