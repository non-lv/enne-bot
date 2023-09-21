import asyncio
from typing import Union

from discord import Interaction, InteractionMessage, Member, Reaction, User

from commands._tetris.Actions import Actions
from commands._tetris.Board import Board


class BoardDrawer:
    def __init__(self):
        self.message: InteractionMessage = None

    async def drawBoard(self, interaction: Interaction, board: Board):
        if not self.message:
            await interaction.response.send_message(str(board))
            self.message: InteractionMessage = await interaction.original_response()
        else:
            await self.message.edit(content = str(board))

    async def gameOver(self):
        await self.message.clear_reactions()

    async def addActions(self):
        await asyncio.gather(*[self.message.add_reaction(a) for a in [ac.value for ac in Actions]])

    async def fetchInputs(self, interaction: Interaction) -> list[Actions]:
        self.message = await self.message.fetch()

        actions_to_check = [reaction for reaction in [rc for rc in self.message.reactions if rc.emoji in [ac.value for ac in Actions]] if reaction.count > 1]
        actions = [ac for ac in await asyncio.gather(*[self.__removeUserReactions(interaction.user, rc) for rc in actions_to_check]) if ac is not None]
        return self.__emotesToActions(actions) if len(actions) > 0 else None

    def __emotesToActions(self, actions: list[str]) -> list[Actions]:
        return [Actions(a) for a in actions]

    async def __removeUserReactions(self, user: Union[User, Member], reaction: Reaction):
        if user in [u async for u in reaction.users()]:
            await reaction.remove(user)
            return reaction.emoji
        return None