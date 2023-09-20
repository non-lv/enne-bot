from discord import Interaction, InteractionMessage
import asyncio

colours = ['⬜', '🟥', '🟧', '🟨', '🟩', '🟦', '🟪', '🟫']
controls = ['⬅️', '🔄', '➡️']

async def drawGameOver(msg: InteractionMessage, score: int):
    await asyncio.gather(
        msg.channel.send(f'GAME OVER!! Your score was ${score} 🙃'),
        msg.reactions.clear()
    )

def create_message(board: [[int]], score: int) -> str:
    return f'``Score: {score}``\n' + ''.join([''.join([colours[cell] for cell in row])+'\n' for row in board])

async def draw(interaction: Interaction, board: [[int]], msg: InteractionMessage, score: int) -> (str, InteractionMessage):
    if msg == None:
        await interaction.response.send_message("Loading board...")
       
        msg = await interaction.original_response()
        await asyncio.gather(*[msg.add_reaction(c) for c in controls])

        return None, msg
    else:        
        await msg.edit(content = create_message(board, score))
        msg = await msg.fetch()
        
        actions = await asyncio.gather(*[remove_user_reactions(interaction.user, reaction) for reaction in [rc for rc in msg.reactions if rc.emoji in controls]])
        action = [ac for ac in actions if ac is not None]
        return action[0] if len(action) > 0 else None, msg
    
async def remove_user_reactions(user, reaction):
    if user in [u async for u in reaction.users()]:
        await reaction.remove(user)
        return reaction.emoji
    return None