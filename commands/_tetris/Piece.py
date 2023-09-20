from typing_extensions import Self

from commands._tetris.Position import Position


class Piece:
    def __init__(self, piece: [[int]]):
        # Always a rectangle
        self.piece: [[int]] = piece
        self.width = len(piece)
        self.height = len(piece)

        self.pos = Position(0, 0)

    def rotateRight(self) -> Self:
        self.__transpose()
        self.__reverse()
        return self

    def rotateLeft(self) -> Self:
        self.__reverse()
        self.__transpose()
        return self

    def __transpose(self):
        # Transpose matrix, block is the Piece.
        for y in range(len(self.piece)):
            for x in range(y):
                [self.piece[x][y], self.piece[y][x]] = [self.piece[y][x], self.piece[x][y]]

    def __reverse(self):
        self.piece = [row[::-1] for row in self.piece]