from chessprinting import *

def pieces():
    orboard=chessboard()
    cboard=chessboard()
    cboard[0][0]=cboard[0][7]="♖"
    cboard[7][0]=cboard[7][7]="♜"
    cboard[0][1]=cboard[0][6]="♘"
    cboard[7][1]=cboard[7][6]="♞"
    cboard[0][2]=cboard[0][5]="♗"
    cboard[7][2]=cboard[7][5]="♝"
    cboard[0][3]="♕"
    cboard[7][3]="♛"
    cboard[0][4]="♔"
    cboard[7][4]="♚"
    for i in range (8):
        cboard[1][i]="♙"
    for i in range (8):
        cboard[6][i]="♟︎"
    print_chessboard(cboard)
    return cboard

def is_valid():
    return True    

def checkmate():
    return False   

def chess_game():
    print("Welcome to chess game!")
    print("Enter inputs in the following form: if white queen moves from")
    print("d1 to d5, enter Qd1d5. If it takes a piece while moving to d5,")
    print("enter Qd1xd5, ie. the x between coordinates indicates capture.")
    cboard = pieces()
    orboard=chessboard()
    turn = "white"
    while not checkmate():
        while True:
            Move = input("Please enter your move in the above format.")
            startrank = int(Move[2])
            startfile = Move[1]
            endrank = int(Move[-1])
            endfile = Move[-2]
            capturestate = False
            if Move[-3]=="x":
                capturestate = True
            #piececheck = False
            #if ...
            print(startrank, startfile, endrank, endfile, capturestate)
            if is_valid():
                break
        #need to replace start position with original board square
        originalpiece = cboard[8-startrank][ord(startfile)-97]
        cboard[8-startrank][ord(startfile)-97]=orboard[8-startrank][ord(startfile)-97]
        cboard[8-endrank][ord(endfile)-97]=originalpiece
        print_chessboard(cboard)
