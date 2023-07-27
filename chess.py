from chessprinting import *
from copy import deepcopy

#note this was written on dark mode, so the piece and square colours may be 
#switched in regular (light) mode

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
    #cboard[6][5]="♙"
    #cboard[1][5]="♟︎"
    cboard[6][5]="♕"
    cboard[5][5]="♕"
    print_chessboard(cboard)
    return cboard

def move_length(stcord, endcord):
    #hmove positive is movement towards the left, vmove positive is up
    vmove = stcord[0]-endcord[0]
    hmove = stcord[1]-endcord[1]
    return (vmove, hmove)

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
    
def knight_move(stcord, endcord, cboard):
    (vmove,hmove) = move_length(stcord,endcord)
    if ((abs(hmove) == 2 and abs(vmove) == 1) or (abs(hmove) == 1 and abs(vmove) == 2)):
        return True
    return False
    
def king_move(stcord, endcord, cboard):
    (vmove,hmove) = move_length(stcord,endcord)
    if ((abs(hmove) == 1 or hmove == 0) and (abs(vmove) == 1 or vmove == 0)):
        return True
    return False

def bishop_move(stcord, endcord, cboard):
    (vmove,hmove) = move_length(stcord,endcord)
    if abs(vmove)==abs(hmove):
        #print(abs(hmove))
    #will require similar strategy to rook, iterating squares between to check for occupancy
        for i in range (1, abs(vmove)):
            #print((stcord[0]-i*int(vmove/abs(vmove)),stcord[1]-i*int(hmove/abs(hmove))))
            if bool(square_status((stcord[0]-i*int(vmove/abs(vmove)),stcord[1]-i*int(hmove/abs(hmove))), cboard)) == True:
                return False
        return True
    return False

def rook_move(stcord, endcord, cboard):
    (vmove,hmove) = move_length(stcord,endcord)
    #vertical movement, -i*int(vmove/abs(vmove)) determines direction of i depending on whether movement is up or down
    if hmove == 0:
        for i in range(1, abs(vmove)):
            if bool(square_status((stcord[0]-i*int(vmove/abs(vmove)),stcord[1]), cboard)) == True:
                #print(f"{(stcord[0]-i*int(vmove/abs(vmove)),stcord[1])} is nonempty")
                return False
        return True
    #horizontal similar to vertical
    if vmove == 0:
        for i in range(1, abs(hmove)):
            #print((stcord[0],stcord[1]-i*int(hmove/abs(hmove))))
            if bool(square_status((stcord[0],stcord[1]-i*int(hmove/abs(hmove))), cboard)) == True:
                #print(f"{(stcord[0],stcord[1]-i*int(hmove/abs(hmove)))} is nonempty")
                return False
        return True
    return False

def queen_move(stcord, endcord, cboard):
    # This is just a combination of rook and bishop moves
    if (rook_move(stcord, endcord, cboard) == True or bishop_move(stcord, endcord, cboard) == True):
        return True
    return False

def pawn_move(stcord, endcord, cboard, capturestate):
    (vmove,hmove) = move_length(stcord,endcord)
    # colour returns 1 or -1 in order to make legal movement dependent on colour
    if chesspieces[square_status(stcord, cboard)]["Colour"] == "White":
        start_row = 6
        colour = 1
    else:
        start_row = 1
        colour = -1
    # move of 2 tiles at start position
    if (stcord[0] == start_row and vmove*colour == 2 and hmove == 0 and capturestate == False):
        # coordinate inbetween must be empty
        if square_status(((stcord[0]-colour), stcord[1]), cboard) == False:
            return True
        return False
    elif (vmove*colour == 1 and hmove == 0 and capturestate == False):
        return True
    # next one for capture
    elif (vmove*colour == 1 and abs(hmove) == 1 and capturestate == True):
        return True
    else:
        print('invalid pawn move')
        return False
    
chesspieces = {"♚": {"Colour": "White", "Type": "King", "validity_func": king_move}, 
               "♔": {"Colour": "Black", "Type": "King", "validity_func": king_move},
               "♛": {"Colour": "White", "Type": "Queen", "validity_func": queen_move},
               "♕": {"Colour": "Black", "Type": "Queen", "validity_func": queen_move},
               "♝": {"Colour": "White", "Type": "Bishop", "validity_func": bishop_move},
               "♗": {"Colour": "Black", "Type": "Bishop", "validity_func": bishop_move},
               "♞": {"Colour": "White", "Type": "Knight", "validity_func": knight_move},
               "♘": {"Colour": "Black", "Type": "Knight", "validity_func": knight_move},
               "♜": {"Colour": "White", "Type": "Rook", "validity_func": rook_move},
               "♖": {"Colour": "Black", "Type": "Rook", "validity_func": rook_move},
               "♟︎": {"Colour": "White", "Type": "Pawn", "validity_func": pawn_move},
               "♙": {"Colour": "Black", "Type": "Pawn", "validity_func": pawn_move}}

validpiecenames = ["p", "P", "n", "N", "q", "Q", "k", "K", "b", "B", "r", "R"]

validfiles = ["a", "b", "c", "d", "e", "f", "g", "h"]

validranks = ["1", "2", "3", "4", "5", "6", "7", "8"]
    
def is_valid(turn, stcord, endcord, capturestate, cboard):
    # Positions must be within [0:7]
    
    #if ((stcord[0] or stcord[1] or endcord[0] or endcord[1]) > 7 or
    #(stcord[0] or stcord[1] or endcord[0] or endcord[1]) < 0):
        #return False
    #Cannot go from same square to itself is satisfied by later conditions
    # If the start square is empty, invalid move
    #print("Square status of start")
    #print(square_status(stcord, cboard))
    #print(cboard)
    if square_status(stcord, cboard) == False:
        return False
    # If the piece is not the correct colour, invalid move

    if chesspieces[square_status(stcord, cboard)]["Colour"] != turn:
        return False
    # If the end position is filled and no capture, invalid
    if (capturestate == False and 
    bool(square_status(endcord, cboard)) == True):
        return False
    # If capturing and end position is empty, invalid
    if (capturestate == True and 
        square_status(endcord, cboard) == False):
        return False
    # If capturing a same colour piece, invalid
    if (capturestate == True and chesspieces[square_status(endcord, cboard)]["Colour"] == turn):
        return False
    #print(stcord)
    #print(endcord)
    if chesspieces[square_status(stcord, cboard)]["Type"] == "Knight":
        return knight_move(stcord, endcord, cboard)
    if chesspieces[square_status(stcord, cboard)]["Type"] == "King":
        return king_move(stcord, endcord, cboard)
    if chesspieces[square_status(stcord, cboard)]["Type"] == "Rook":
        return rook_move(stcord, endcord, cboard)
    if chesspieces[square_status(stcord, cboard)]["Type"] == "Bishop":
        return bishop_move(stcord, endcord, cboard)
    if chesspieces[square_status(stcord, cboard)]["Type"] == "Queen":
        return queen_move(stcord, endcord, cboard)
    if chesspieces[square_status(stcord, cboard)]["Type"] == "Pawn":
        return pawn_move(stcord, endcord, cboard, capturestate)
    # Lastly, need to consider if moves will result in own side check
    return True

def wking_location(cboard):
    for i in range(8): 
        for j in range(8):
            if cboard[i][j] == "♚":
                #print(f" W king at {(i,j)}")
                return (i,j)
def bking_location(cboard):
    for i in range(8): 
        for j in range(8):
            if cboard[i][j] == "♔":
                #print(f" B king at {(i,j)}")
                return (i,j)

def checkall(anyboard, turn): 
    #print("uptohere")
    wking = wking_location(anyboard)
    bking = bking_location(anyboard)
    for i in range(8): 
        for j in range(8):
            #print(square_status((i,j), anyboard))
            if square_status((i,j), anyboard) != False:
                piece = chesspieces[square_status((i,j), anyboard)]
                #print(f"Turn is {turn}")
                #print(piece["Colour"])
                #print(anyboard[i][j])
                if (turn == "White" and piece["Colour"] == "Black" and anyboard[i][j] != "♙"):
                    #print(anyboard[i][j])
                    #print(piece)
                    #print(chesspieces.get(anyboard[i][j]).get("validity_func")((i,j), wking, anyboard))
                    #print(chesspieces.get(anyboard[i][j]))
                    if (chesspieces.get(anyboard[i][j]).get("validity_func")((i,j), wking, anyboard)) == True:
                        #print("White King is checked")
                        return True
                    #return True
                    # now onto the pawn conditions
                elif (turn == "White" and anyboard[i][j] == "♙"):
                    if 1 == wking[0]-i and abs(j-wking[1]) == 1:
                        #print("White King is checked")
                        return True
                elif (turn == "Black" and piece["Colour"] == "White" and anyboard[i][j] != "♟︎"):
                    #print(anyboard[i][j])
                    #print(piece)
                    #print(chesspieces.get(anyboard[i][j]).get("validity_func")((i,j), bking, anyboard))
                    if (chesspieces.get(anyboard[i][j]).get("validity_func")((i,j), bking, anyboard)) == True:
                        #print("Black King is checked")
                        return True
                elif (turn == "Black" and anyboard[i][j] == "♟︎"):
                    if 1 == i-bking[0] and abs(j-bking[1]) == 1:
                        #print("Black King is checked")
                        return True
    else:
        #print(f"No {turn} Check")
        return False
    return True
                    
def movevalidity(Move):
    #print("started validity")
    if len(Move) == 5 or (len(Move) == 6 and (Move[3] == "x" or Move[3] == "X")):
        if (Move[0] in validpiecenames) == False:
            return False
        if (Move[1] in validfiles and Move[-2] in validfiles) == False:
            return False
        if (Move[-1] in validranks and Move[2] in validranks) == False:
            return False
        return True
    else: 
        return False

def checkspecial():
    return False


def checkmate(anyboard, turn):
    #print("startedthis")
    if checkall(anyboard, turn) == False:
        print("allfine")
        return False
    else:
        for i in range(8): 
            for j in range(8):
                #print(square_status((i,j), anyboard))
                if square_status((i,j), anyboard) != False:
                    piece = chesspieces[square_status((i,j), anyboard)]
                    #print(checkall(anyboard, turn))
                    while checkall(anyboard, turn) == True:
                        return False
                
    
    #return False   

def chess_game():
    print("Welcome to chess game!")
    print("Enter inputs in the following form: if white queen moves from")
    print("d1 to d5, enter Qd1d5. If it takes a piece while moving to d5,")
    print("enter Qd1xd5, ie. the x indicates capture.")
    cboard = pieces()
    orboard=chessboard()
    turn = "White"
    #turn = "Black"
    turn_no = 1
    #checkmate(cboard, turn)
    while not checkmate(cboard, turn):
        while True:
            print(f"It is currently turn {turn_no}, {turn} to move")
            tempboard = deepcopy(cboard)
            if checkall(cboard, turn) == True:
                print(f"Note that you are under check")
            while True:   
                Move = input("Please enter your move in the above format. ")
                #print(movevalidity(Move))
                if movevalidity(Move):
                    break
                print("Please enter a valid move")
            startrank = int(Move[2])
            startfile = Move[1]
            endrank = int(Move[-1])
            endfile = Move[-2]
            #piecename = Move[0]
            stcord = (8-startrank, ord(startfile)-97)
            endcord = (8-endrank, ord(endfile)-97)
            capturestate = False
            if Move[-3]=="x":
                capturestate = True
            #print(startrank, startfile, endrank, endfile, capturestate)
            tempboard[8-endrank][ord(endfile)-97]=tempboard[8-startrank][ord(startfile)-97]
            tempboard[8-startrank][ord(startfile)-97]=orboard[8-startrank][ord(startfile)-97]
            #tempboard = True
            #print("second time")
            #print(bool(checkall(tempboard, turn)))
            if (is_valid(turn, stcord, endcord, capturestate, cboard) and (not checkall(tempboard, turn))):
                break
            print("Please enter a legal move")

        #next (useless) block prints in words the move
        print(f"{turn} {chesspieces[square_status(stcord, cboard)]['Type']} moves from {startfile}{startrank} to {endfile}{endrank}")
        if turn == "White":
            turn = "Black"
        else:
            turn = "White"
        if capturestate == True:
            print(f"and takes {turn} {chesspieces[square_status(endcord, cboard)]['Type']}")
        turn_no += 1
        #need to replace start position with original board square
        cboard[8-endrank][ord(endfile)-97]=cboard[8-startrank][ord(startfile)-97]
        cboard[8-startrank][ord(startfile)-97]=orboard[8-startrank][ord(startfile)-97]
        print("")
        print("The current state is below:")
        print_chessboard(cboard)

chess_game()