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
    for i in range (7):
        cboard[6][i]="♟︎"
    print_chessboard(cboard)
    return cboard

def move_length(startcoord, endcoord):
    #hor_move positive is movement towards the left, ver_move positive is up
    ver_move = startcoord[0]-endcoord[0]
    hor_move = startcoord[1]-endcoord[1]
    return (ver_move, hor_move)

def square_status(coord, cboard):
    #square status returns status of piece and false otherwise (empty)
    piece = cboard[coord[0]][coord[1]]
    piecetype = None
    if piece in chesspieces.keys():
        #print(f"The piece {piece} is a {chesspieces[piece]['Colour']} {chesspieces[piece]['Type']}")
        piecetype = (chesspieces[piece]["Colour"],chesspieces[piece]["Type"])
        #print(bool(piece))
        return piece
    else:
        #print("The square is empty")
        return False
    
def knight_move(startcoord, endcoord):
    (hor_move,ver_move) = move_length(startcoord,endcoord)
    if ((abs(hor_move) == 2 and abs(ver_move) == 1) or (abs(hor_move) == 1 and abs(ver_move) == 2)):
        return True
    else: 
        return False

def rook_move(startcoord, endcoord, cboard):
    (ver_move,hor_move) = move_length(startcoord,endcoord)
    #vertical movement, first down and then up
    print(hor_move)
    print(ver_move)
    if hor_move == 0 and ver_move > 0:
        for i in range(1, abs(ver_move)):
            #if all in between are empty, is valid
            print((startcoord[0]-i,startcoord[1]))
            if square_status((startcoord[0]-i,startcoord[1]), cboard) == True:
            
                print(f"{(startcoord[0]-i,startcoord[1])} is nonempty")
                return False
            
    else:
        print("Not move")
        return False

def is_valid(originalpiece, turn, startcoord, endcoord, 
             capturestate, cboard, endsquare):
    # Positions must be within [0:7]
    if ((startcoord[0] or startcoord[1] or endcoord[0] or endcoord[1]) > 7 or 
    (startcoord[0] or startcoord[1] or endcoord[0] or endcoord[1]) < 0):
        return False
    #Cannot go from same square to itself is satisfied by later conditions
    # If the start square is empty, invalid move
    if square_status(startcoord, cboard) == False:
        return False
    # If the piece is not the correct colour, invalid move
    if chesspieces[originalpiece]["Colour"] != turn:
        return False
    # If the end position is filled and no capture, invalid
    if (capturestate == False and 
    bool(square_status(endcoord, cboard)) == True):
        return False
    # If capturing and end position is empty, invalid
    if (capturestate == True and 
        square_status(endcoord, cboard) == False):
        return False
    # If capturing a same colour piece, invalid
    if (capturestate == True and chesspieces[endsquare]["Colour"] == turn):
        return False
    print(startcoord)
    print(endcoord)
    if chesspieces[originalpiece]["Type"] == "Knight":
        return knight_move(startcoord, endcoord)
    if chesspieces[originalpiece]["Type"] == "Rook":
        return rook_move(startcoord, endcoord, cboard)
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
            Move = input("Please enter your move in the above format. ")
            startrank = int(Move[2])
            startfile = Move[1]
            endrank = int(Move[-1])
            endfile = Move[-2]
            startcoord = (8-startrank, ord(startfile)-97)
            endcoord = (8-endrank, ord(endfile)-97)
            capturestate = False
            if Move[-3]=="x":
                capturestate = True
            #print(startrank, startfile, endrank, endfile, capturestate)
            originalpiece = cboard[8-startrank][ord(startfile)-97]
            endsquare = cboard[8-endrank][ord(endfile)-97]
            if is_valid(originalpiece, turn, startcoord, endcoord, 
                        capturestate, cboard, endsquare):
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