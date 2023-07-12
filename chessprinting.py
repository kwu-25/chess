#chessprinting
def chessboard(): 
    board = []
    for row in range(8):
        if row % 2 == 0:
            for col in range(9):
                if col % 2 == 0:
                    board += ["⬛"]
                else:
                    board += ["⬜"]
        else:
            #board = []
            for col in range(9):
                if col % 2:
                    board += ["⬛"]
                else:
                    board += ["⬜"]
    finalboard=[]
    for _ in range(4):
        finalboard += [board[0:8],board[9:17]]
    return finalboard
    

def print_chessboard(board):
    print(" ", end= "\t")
    for i in range(len(board)):
        print(chr(97+i), end = "\t")
    print()
    for i in range(len(board)):
        #print("\n")
        print(8-i, end = "\t")
        for j in range(len(board[i])):
            print(board[i][j], end = "\t")
        print()
        
