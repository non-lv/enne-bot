from discord import Interaction
import random
from commands._tetris import view

async def init(interaction: Interaction):
    board = createBoard()
    floatPlane = createBoard()
    score = 0
    await gameLoop(board, floatPlane, False, interaction, None, score)

def createBoard() -> [[int]]:
    # Width: 5
    # Height: 10
    return [[0 for _ in range(10)] for _ in range(20)]

async def gameLoop(board: [[int]], floatPlane: [[int]], isFloating: bool, interaction: Interaction, message: str, score: int):
    while(True):
        if not isFloating:
            floatPlane = createBoard()
            newBlock = spawnBlock()

            if canPlaceBlock(board, newBlock):
                board = placeBlock(board, newBlock)
                floatPlane = placeBlock(floatPlane, newBlock)
            else:
                view.drawGameOver(message, score)
                return; # Game Over
            
            isFloating = True
        else:
            if hasCollided(board, floatPlane):
                # Check for Lines
                score, board = checkLines(board, score)

                isFloating = False
            else:
                board, floatPlane = moveBlock(board, floatPlane)

        mov, message = await view.draw(interaction, board, message, score)
        match mov:
            case '➡️':
                board, floatPlane = moveRight(board, floatPlane)
            case '⬅️':
                board, floatPlane = moveLeft(board, floatPlane)
            case '🔄':
                rotate(board, floatPlane)

def checkLines(board: [[int]], score: int) -> (int, [[int]]):
    for y in range(len(board)):
        x = 0
        for x in range(len(board[0])):
            if board[y][x] == 0:
                break
        if x == len(board[0]):
            board.splice(y, 1)
            board.unshift([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            score += 1

    return score, board

def moveBlock(board: [[int]], floatPlane: [[int]]) -> ([[int]], [[int]]):
    for y in range(len(board)-1, -1, -1):
        for x in range(len(board[0])):
            if floatPlane[y][x] != 0:
                floatPlane[y + 1][x] = floatPlane[y][x]
                board[y + 1][x] = floatPlane[y][x]
                floatPlane[y][x] = 0
                board[y][x] = 0

    return board, floatPlane

def checkLeft(board: [[int]], floatPlane: [[int]]) -> bool:
    for y in range(len(board)):
        for x in range(len(board[0])):
            if floatPlane[y][x] != 0 and floatPlane[y][x - 1] == 0 and board[y][x - 1] != 0 and x - 1 > 0:
                return False
    return True

def checkRight(board: [[int]], floatPlane: [[int]]) -> bool:
    for y in range(len(board)):
        for x in range(len(board[0])):
            if floatPlane[y][x] != 0 and floatPlane[y][x + 1] == 0 and board[y][x + 1] != 0 and x + 1 < len(board[0]):
                return False
    return True

def moveLeft(board: [[int]], floatPlane: [[int]]) -> ([[int]], [[int]]):
    if checkLeft(board, floatPlane):
        for y in range(len(board)):
            for x in range(len(board[0])):
                if floatPlane[y][x] != 0:
                    floatPlane[y][x - 1] = floatPlane[y][x]
                    board[y][x - 1] = floatPlane[y][x]
                    floatPlane[y][x] = 0
                    board[y][x] = 0
    return board, floatPlane

def moveRight(board: [[int]], floatPlane: [[int]]) -> ([[int]], [[int]]):
    if checkRight(board, floatPlane):
        for y in range(len(board)):
            for x in range(len(board[0])-1, -1, -1):
                if (floatPlane[y][x] != 0):
                    floatPlane[y][x + 1] = floatPlane[y][x]
                    board[y][x + 1] = floatPlane[y][x]
                    floatPlane[y][x] = 0
                    board[y][x] = 0
    return board, floatPlane

def rotate(board: [[int]], floatPlane: [[int]]):
    # Finding the center of the Block
    left = len(floatPlane[0]) - 1
    right = 0
    top = len(floatPlane) - 1
    bot = 0
    for y in range(len(floatPlane)):
        for x in range(len(floatPlane[0])):
            if (floatPlane[y][x] != 0):
                if (left >= x):
                    left = x
                if (right <= x):
                    right = x
                if (top >= y):
                    top = y
                if (bot <= y):
                    bot = y

    # Isolate the Block
    block = []
    for y in range(top, bot):
        row = []
        for x in range(left, right):
            row.append(floatPlane[y][x])
        block.append(row)

    # Rotate the Block
    if len(block) > 3 or len(block[0]) > 3:         # Long Piece
        col = block[0][0]
        if (len(block) > 1):
            block = [[col, col, col, col]]
        else:
            block = [[col], [col], [col], [col]]
    elif len(block) < 3 and len(block[0]) < 3:      # Square Block
        return
    else:
        # Get the 3x3 Grid
        if len(block) == 2:
            block.append([0, 0, 0])
        else:
            for a in block:
                a.append(0)

        rotateBlock(block)

    # Remove the block from the grid
    for y in range(len(floatPlane)):
        for x in range(len(floatPlane[0])):
            if (floatPlane[y][x] != 0):
                floatPlane[y][x] = 0
                board[y][x] = 0

    # Place The Block back on the grid
    checkRotPlacement(block, board, floatPlane, left, top)

def checkRotPlacement(block: [[int]], board: [[int]], floatPlane: [[int]], left: int, top: int):
    if left + len(block[0]) > len(board[0]):
        left = len(board[0]) - len(block[0])

    temp = checkTopPlacement(block, board, top, left)
    while temp != top:
        temp = checkTopPlacement(block, board, top, left)
        top = temp

    # Place the Block
    for y in range(top, top + len(block)):
        for x in range(left, left + len(block[0])):
            if block[y - top][x - left] != 0:
                floatPlane[y][x] = block[y - top][x - left]
                board[y][x] = block[y - top][x - left]

def checkTopPlacement(block: [[int]], board: [[int]], top: int, left: int) -> int:
    for y in range(top, top + len(block)):
        for x in range(left, left + len(block[0])):
            if block[y - top][x - left] != 0 and board[y][x] != 0:
                top -= 1
    return top

def rotateBlock(block: [[int]]):
    # Transpose matrix, block is the Piece.
    for y in range(len(block)):
        for x in range(y):
            [block[x][y], block[y][x]] = [block[y][x], block[x][y]]

    # Reverse the order of the columns.
    for b in block:
        b.reverse()

def hasCollided(board: [[int]], floatPlane: [[int]]) -> bool:
    for x in range(len(board)):
        for y in range(len(board[0])):
            if floatPlane[x][y] != 0:
                if x == len(board) - 1 or (board[x + 1][y] != 0 and floatPlane[x + 1][y] == 0):
                    return True
    return False

def canPlaceBlock(board: [[int]], block: [[int]]) -> bool:
    for y in range(len(block)):
        for x in range(len(block[y])):
            if board[x][y + 3] != 0:
                return False
    return True

def placeBlock(board: [[int]], block: [[int]]) -> [[int]]:
    for y in range(len(block)):
        for x in range(len(block[y])):
            board[x][y + 3] = block[y][x]
    return board

def spawnBlock() -> [[int]]:
    pieces = [
        [[1, 1, 1, 1]],             # I Block
        [[2, 2, 2], [0, 2]],        # T Block
        [[0, 3, 3], [3, 3]],        # S Block
        [[4, 4], [0, 4, 4]],        # Z Block
        [[5, 5, 5], [5]],           # L Block
        [[6, 6, 6], [0, 0, 6]],     # J Block
        [[7, 7], [7, 7]]            # Square Block
    ]

    return pieces[random.randint(0, 6)]