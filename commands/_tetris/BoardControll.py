from discord import Interaction

from commands._tetris.Actions import Actions
from commands._tetris.Board import Board
from commands._tetris.BoardDrawer import BoardDrawer


class BoardControll:
    def __init__(self):
        self.board = Board(19, 10)
        self.boardDrawer = BoardDrawer()
        self.score = 0

    async def gameLoop(self, interaction: Interaction):
        await self.boardDrawer.drawBoard(interaction, self.board, self.score)
        await self.boardDrawer.addActions()

        actions: list[Actions] = None
        while(self.board.move(actions)):
            await self.boardDrawer.drawBoard(interaction, self.board, self.score)
            actions = await self.boardDrawer.fetchInputs(interaction)
        await self.boardDrawer.gameOver(self.score)