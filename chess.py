from chessprinting import *

chesspieces = {"♚": {"Colour": "White", "Type": "King"}, 
               "♔": {"Colour": "Black", "Type": "King"},
               "♛": {"Colour": "White", "Type": "Queen"},
               "♕": {"Colour": "Black", "Type": "Queen"},
               "♝": {"Colour": "White", "Type": "Bishop"},
               "♗": {"Colour": "Black", "Type": "Bishop"},
               "♞": {"Colour": "White", "Type": "Knight"},
               "♘": {"Colour": "Black", "Type": "Knight"},
               "♜": {"Colour": "White", "Type": "Rook"},
               "♖": {"Colour": "Black", "Type": "Rook"},
               "♟︎": {"Colour": "White", "Type": "Pawn"},
               "♙": {"Colour": "Black", "Type": "Pawn"}}

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

def empty_square(rank, file, cboard):
    if (cboard[8-rank][ord(file)-97] == "⬛" or
    cboard[8-rank][ord(file)-97] == "⬜"):
        return True
    else:
        return False

def is_valid(originalpiece, turn, startrank, startfile, 
             endrank, endfile, capturestate, cboard):
    # If the start square is empty, invalid move
    if empty_square(startrank, startfile, cboard) == True:
        return False
    # If the piece is not the correct colour, invalid move
    if chesspieces[originalpiece]["Colour"] != turn:
        return False
    # If the end position is filled and no capture, invalid
    if (capturestate == False and 
    empty_square(endrank, endfile, cboard) == False):
        return False
    # If it is capture and end position is empty, invalid
    if (capturestate == True and 
        empty_square(endrank, endfile, cboard) == True):
        return False
    
    
    
    # If the piece isn't allowed to move that way
    
    # If it wasn't invalid, then it's valid
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
    turn = "White"
    turn_no = 1
    while not checkmate():
        while True:
            print(f"It is currently turn {turn_no}, {turn} to move")
            Move = input("Please enter your move in the above format.")
            startrank = int(Move[2])
            startfile = Move[1]
            endrank = int(Move[-1])
            endfile = Move[-2]
            capturestate = False
            if Move[-3]=="x":
                capturestate = True
            #print(startrank, startfile, endrank, endfile, capturestate)
            originalpiece = cboard[8-startrank][ord(startfile)-97]
            if is_valid(originalpiece, turn, startrank, startfile, 
                        endrank, endfile, capturestate, cboard):
                break
            print("Please enter a valid move.")
        if turn == "White":
            turn = "Black"
        else:
            turn = "White"
        turn_no += 1
        #need to replace start position with original board square
        #originalpiece = cboard[8-startrank][ord(startfile)-97]
        cboard[8-startrank][ord(startfile)-97]=orboard[8-startrank][ord(startfile)-97]
        cboard[8-endrank][ord(endfile)-97]=originalpiece
        print("The current state is below:")
        print_chessboard(cboard)

chess_game()