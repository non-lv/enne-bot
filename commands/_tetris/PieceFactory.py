import random

from commands._tetris.Piece import Piece


class PieceFactory:
    pieces = [
        [[0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0]],   # I Block
        [[0, 0, 0], [2, 2, 2], [0, 2, 0]],                          # T Block
        [[0, 0, 0], [0, 3, 3], [3, 3, 0]],                          # S Block
        [[0, 0, 0], [4, 4, 0], [0, 4, 4]],                          # Z Block
        [[0, 0, 0], [5, 5, 5], [5, 0, 0]],                          # L Block
        [[0, 0, 0], [6, 6, 6], [0, 0, 6]],                          # J Block
        [[7, 7], [7, 7]]                                            # Square Block
    ]

    def __init__(self):
        self.bag = None

    def get(self) -> Piece:
        if(not self.bag):
            self.bag = self.pieces.copy()
        piece = self.bag[random.randint(0, len(self.bag)-1)]
        self.bag.remove(piece)
        return Piece(piece)