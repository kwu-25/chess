#chessprinting
def chessboard(): 
    board = []
    for row in range(8):
        if row % 2 == 0:
            for col in range(8):
                if col % 2 == 0:
                    board += ["⬛"]
                else:
                    board += ["⬜"]
        else:
            #board = []
            for col in range(8):
                if col % 2:
                    board += ["⬛"]
                else:
                    board += ["⬜"]
    for 
    finalboard=[board[0:7],board[8:15],board[0:7],board[8:15],board[0:7],board[8:15],board[0:7],board[8:15]]
    return finalboard
    
board = chessboard()
def print_chessboard(board):
    print("  ", end= "")
    for i in range(len(board)):
        print(i+1, end = " ")
    print()
    for i in range(len(board)):
        print(i+1, end = " ")
        for j in range(len(board[i])):
            print(board[i][j], end = "")
        print()