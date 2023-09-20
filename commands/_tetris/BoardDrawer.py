import asyncio

from discord import Interaction, InteractionMessage

from commands._tetris.Actions import Actions
from commands._tetris.Board import Board


class BoardDrawer:
    def __init__(self):
        self.allActions = [Actions.Left, Actions.RotateLeft, Actions.Drop, Actions.RotateRight, Actions.Right]
        self.message: InteractionMessage = None

    async def drawBoard(self, interaction: Interaction, board: Board, score: int):
        if not self.message:
            await interaction.response.send_message(self.__getBoardMessage(board, score))
            self.message = await interaction.original_response()
        else:
            await self.message.edit(content = self.__getBoardMessage(board, score))

    def __getBoardMessage(self, board: Board, score: int) -> str:
        return f'``Score: {score}``\n{str(board)}'

    async def gameOver(self, score: int):
        await asyncio.gather(
            self.message.channel.send(f'GAME OVER!! Your score was ${score} 🙃'),
            self.message.clear_reactions()
        )

    async def addActions(self):
        await asyncio.gather(*[self.message.add_reaction(a.value) for a in self.allActions])

    async def fetchInputs(self, interaction: Interaction) -> list[Actions]:
        self.message = await self.message.fetch()

        actions_to_check = [reaction for reaction in [rc for rc in self.message.reactions if rc.emoji in self.allActions] if reaction.count > 1]
        actions = [ac for ac in await asyncio.gather(*[self.__removeUserReactions(interaction.user, rc) for rc in actions_to_check]) if ac is not None]
        return actions if len(actions) > 0 else None

    async def __removeUserReactions(user, reaction):
        if user in [u async for u in reaction.users()]:
            await reaction.remove(user)
            return reaction.emoji
        return None