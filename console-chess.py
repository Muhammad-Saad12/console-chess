#Importing libraries
import chess
import chess.engine
import math

#Initializing the board
chessBoard = chess.Board()
gameOver = False
currentPlayer = chess.WHITE
#Printing the board at every step
def printBoard(chessBoard):
    print("\n")
    print("---------CHESS---------------")
    print("\n")
    print(chessBoard)
    print("\n")
    print("---------HUMAN VS AI ---------")

#Getting the user move
def getUserMove(chessBoard):
    while True:
        try:
            turn = input("Enter your move in the format 'a2a4': ")
            turn = chess.Move.from_uci(turn)
            if turn in chessBoard.legal_moves:
                return turn
            else:
                print("Invalid move. Try again. The format is 'a2a4'.")
        except:
            print("Invalid input. Try again. Board Limit is exceeding or the format is not correct.")


# Checking if the game is over
def isGameOver(chessBoard):
    return chessBoard.is_game_over()
# Checking if the game is draw
def isDraw(chessBoard):
    return chessBoard.is_stalemate() or chessBoard.is_insufficient_material() or chessBoard.is_seventyfive_moves() or chessBoard.is_fivefold_repetition()
# Getting the winner
def getWinner(chessBoard):
    if chessBoard.is_checkmate():
        return "White" if chessBoard.turn == chess.BLACK else "Black"
    else:
        return None
# Switching the player
def switchPlayer(currentPlayer):
    return chess.WHITE if currentPlayer == chess.BLACK else chess.BLACK
# Getting the computer move. This is the AI part. The AI is using the minimax algorithm with alpha beta pruning.

def getComputerMove(chessBoard):
    def min_max(alpha, beta, remainingDepth):
        if remainingDepth == 0:
            return evaluateChessboard(chessBoard)

        if chessBoard.is_checkmate():
            if chessBoard.turn == chess.WHITE:
                return -math.inf
            else:
                return math.inf

        if chessBoard.is_stalemate() or chessBoard.is_insufficient_material() or chessBoard.is_seventyfive_moves() or chessBoard.is_fivefold_repetition():
            return 0

        if chessBoard.turn == chess.WHITE:
            maxEval = -math.inf
            for move in chessBoard.legal_moves:
                chessBoard.push(move)
                eval = min_max(alpha, beta, remainingDepth - 1)
                chessBoard.pop()
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return maxEval
        else:
            minEval = math.inf
            for move in chessBoard.legal_moves:
                chessBoard.push(move)
                eval = min_max(alpha, beta, remainingDepth - 1)
                chessBoard.pop()
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return minEval

    def evaluateChessboard(chessBoard):
        pieceValues = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 4,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0
        }
        score = 0
        for square, piece in chessBoard.piece_map().items():
            if piece.color == chess.WHITE:
                score += pieceValues[piece.piece_type]
            else:
                score -= pieceValues[piece.piece_type]
        return score

    bestMove = None
    bestEval = -math.inf
    alpha = -math.inf
    beta = math.inf
    for move in chessBoard.legal_moves:
        chessBoard.push(move)
        eval = min_max(alpha, beta, remainingDepth=2)
        chessBoard.pop()
        if eval > bestEval:
            bestMove = move
            bestEval = eval
        alpha = max(alpha, eval)
    return bestMove




def play():
    choice = input("Press 1 to start the game: ")
    while choice != "1":
        choice = input("Invalid input. Press 1 to start the game: ")
    
    print("\n")
    print("WELCOME TO CHESS GAME MADE BY SAAD")
    chessBoard = chess.Board()
    currentPlayer = chess.WHITE
    gameOver = False
    
    while not gameOver:
        printBoard(chessBoard)
        if currentPlayer == chess.WHITE:
            move = getUserMove(chessBoard)
        else:
            move = getComputerMove(chessBoard)
        chessBoard.push(move)
        
        if isGameOver(chessBoard):
            gameOver = True
            printBoard(chessBoard)
            winner = getWinner(chessBoard)
            if winner:
                print(winner + " wins!")
            else:
                print("Draw!")
        elif isDraw(chessBoard):
            gameOver = True
            printBoard(chessBoard)
            print("Draw!")
        else:
            currentPlayer = switchPlayer(currentPlayer)


play()
