import copy
from dataclasses import replace

from commands._tetris.Actions import Actions
from commands._tetris.Piece import Piece
from commands._tetris.PieceFactory import PieceFactory


class Board:
    def __init__(self, height: int, width: int):
        self.height: int = height
        self.width: int = width
        self.board: list[list[int]] = [[0 for _ in range(width)] for _ in range(height)]
        self.score = 0
        self.counter = 0

        self.pf = PieceFactory()
        self.piece: Piece = None

    def move(self, actions: list[Actions]) -> bool:
        if self.counter >= 3:
            self.__placePieceAndReset()
            return True

        if(not self.piece):
            self.piece = self.pf.get()
            self.piece.pos.x = int((self.width - len(self.piece.piece))/2)

            self.__checkAndFixPieceOverlap()
            # If new piece spawns offscreen - Game Over
            if self.piece.pos.y + self.piece.height <= 0:
                return False
        else:
            pieceMovement: bool = self.__movePieceDown()
            if not pieceMovement and not actions:
                self.__placePieceAndReset()
            else:
                if not pieceMovement:
                    self.counter += 1
                self.__executeActions(actions)
        return True

    def __str__(self) -> str:
        fullBoard = copy.deepcopy(self.board)
        if(self.piece):
            self.__placePiece(fullBoard)
        colours = ['⬜', '🟥', '🟧', '🟨', '🟩', '🟦', '🟪', '🟫']
        return f'``Score: {self.score}``\n' + ''.join([''.join([colours[cell] for cell in row])+'\n' for row in fullBoard])

#region Actions
    def __executeActions(self, actions: list[Actions]):
        if not actions: return

        if Actions.Left in actions and Actions.Right in actions:
            actions.remove(Actions.Left)
            actions.remove(Actions.Right)

        if Actions.RotateLeft in actions and Actions.RotateRight in actions:
            actions.remove(Actions.RotateLeft)
            actions.remove(Actions.RotateRight)

        for action in actions:
            match action:
                case Actions.RotateLeft:
                    self.__rotatePieceLeft()
                case Actions.RotateRight:
                    self.__rotatePieceRight()
                case Actions.Left:
                    self.__movePieceLeft()
                case Actions.Right:
                    self.__movePieceRight()
                case Actions.Drop:
                    self.__drop()

    def __rotatePieceRight(self):
        self.piece.rotateRight()
        self.__checkAndFixPieceHorizontalPos()
        self.__checkAndFixPieceOverlap()

    def __rotatePieceLeft(self):
        self.piece.rotateLeft()
        self.__checkAndFixPieceHorizontalPos()
        self.__checkAndFixPieceOverlap()

    def __movePieceLeft(self) -> bool:
        originalPos = replace(self.piece.pos)
        self.piece.pos.x -= 1
        if self.__checkAndFixPieceHorizontalPos():
            self.piece.pos = originalPos
            return False

        self.__checkAndFixPieceOverlap()
        return True

    def __movePieceRight(self) -> bool:
        originalPos = replace(self.piece.pos)
        self.piece.pos.x += 1
        if self.__checkAndFixPieceHorizontalPos():
            self.piece.pos = originalPos
            return False

        self.__checkAndFixPieceOverlap()
        return True

    def __drop(self):
        while self.__movePieceDown():
            None
        self.__placePieceAndReset()
#endregion

#region Helper Functions
    def __checkLines(self):
        for y in range(self.height):
            i = 0
            for x in range(self.width):
                if self.board[y][x]:
                    i += 1
            if i == self.width:
                del self.board[y]
                self.board.insert(0, [0 for _ in range(self.width)])
                self.score += 1

    def __movePieceDown(self) -> bool:
        self.piece.pos.y += 1
        if not self.__tryPlacePiece():
            self.piece.pos.y -= 1
            return False
        return True

    # checks if piece is placable in current pos
    def __tryPlacePiece(self) -> bool:
        # Vertical offscreen check
        if self.piece.pos.y + self.piece.height > self.height:
            pieceSection = self.piece.piece[self.height - self.piece.pos.y:]
            for y in range(len(pieceSection)):
                for x in range(self.piece.width):
                    if pieceSection[y][x]:
                        return False

        # Piece overlap with left border
        if self.piece.pos.x < 0:
            leftIndex = 0
            pieceSection = [row[abs(self.piece.pos.x):] for row in self.piece.piece]
        else:
            leftIndex = self.piece.pos.x
            pieceSection = self.piece.piece

            # Piece overlap with right border
            if self.piece.pos.x + self.piece.width > self.width:
                pieceSection = [row[self.piece.pos.x + self.piece.width - self.width:]for row in self.piece.piece]

        # Top Offscreen Cut
        if self.piece.pos.y < 0:
            pieceSection = pieceSection[abs(self.piece.pos.y):]
            section = [row[leftIndex:self.piece.pos.x+len(pieceSection[0])] for row in self.board[0:len(pieceSection)]]
        else:
            # section of board that intersects with piece
            section = [row[leftIndex:self.piece.pos.x+len(pieceSection[0])] for row in self.board[self.piece.pos.y:self.piece.pos.y+len(pieceSection)]]

        for y in range(len(section)):
            for x in range(len(section[0])):
                if pieceSection[y][x] and section[y][x]:
                    return False

        return True

    def __placePieceAndReset(self):
        self.__placePiece(self.board)
        self.__checkLines()
        self.piece = None
        self.counter = 0

    def __placePiece(self, board: list[list[int]]):
        y_piece = 0 if self.piece.pos.y >= 0 else abs(self.piece.pos.y)
        y_board = self.piece.pos.y if self.piece.pos.y >= 0 else 0

        while y_piece < self.piece.height and y_board < self.height:
            x_piece = 0 if self.piece.pos.x >= 0 else abs(self.piece.pos.x)
            x_board = self.piece.pos.x if self.piece.pos.x >= 0 else 0

            while x_piece < self.piece.width and x_board < self.width:
                if(self.piece.piece[y_piece][x_piece]):
                    board[y_board][x_board] = self.piece.piece[y_piece][x_piece]
                x_piece += 1
                x_board += 1

            y_piece += 1
            y_board += 1

    # check if part of piece is outside of horizontal bounds and nudge it back in
    def __checkAndFixPieceHorizontalPos(self) -> bool:
        if self.piece.pos.x < 0 and not all(row[:abs(self.piece.pos.x)] == 0 for row in self.piece.piece):
            self.__movePieceRight()
            self.__checkAndFixPieceHorizontalPos()
            return True
        elif self.piece.pos.x + self.piece.width > self.width and not all(row[self.piece.pos.x + self.piece.width - self.width:] == 0 for row in self.piece.piece):
            self.__movePieceLeft()
            self.__checkAndFixPieceHorizontalPos()
            return True
        return False

    # move piece up till it is placeable
    #TODO implement limit of how much a piece can jump up
    def __checkAndFixPieceOverlap(self):
        while not self.__tryPlacePiece():
            self.piece.pos.y -= 1
    #endregion