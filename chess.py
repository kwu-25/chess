from chessprinting import *
from copy import deepcopy


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
    for i in range (0):
        cboard[1][i]="♙"
    for i in range (0):
        cboard[6][i]="♟︎"
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
        print(abs(hmove))
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
        start_row = stcord[0] == 6
        colour = 1
    else:
        start_row = stcord[0] == 1
        colour = -1
    # move of 2 tiles at start position
    if (stcord[0] == int(3.5+2.5*colour) and vmove*colour == 2 and hmove == 0 and capturestate == False):
        return True
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
    
def is_valid(turn, stcord, endcord, capturestate, cboard, tempboard):
    # Positions must be within [0:7]
    
    if ((stcord[0] or stcord[1] or endcord[0] or endcord[1]) > 7 or
    (stcord[0] or stcord[1] or endcord[0] or endcord[1]) < 0):
        return False
    #Cannot go from same square to itself is satisfied by later conditions
    # If the start square is empty, invalid move
   
    print(square_status(stcord, cboard))
    print(cboard)
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
    print(stcord)
    print(endcord)
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
    wking_location(cboard)
    bking_location(cboard)
    checkall(cboard, turn, tempboard)
    return True    

def wking_location(cboard):
    for i in range(8): 
        for j in range(8):
            if cboard[i][j] == "♚":
                print(f" W king at {(i,j)}")
                return (i,j)
def bking_location(cboard):
    for i in range(8): 
        for j in range(8):
            if cboard[i][j] == "♔":
                print(f" B king at {(i,j)}")
                return (i,j)

def checkall(cboard, turn, tempboard): 
    wkingnow = wking_location(cboard)
    bkingnow = bking_location(cboard)
    wkingif = wking_location(tempboard)
    bkingif = bking_location(tempboard)
    for i in range(8): 
        for j in range(8):
            if square_status((i,j), cboard) != False:
                piece = chesspieces[square_status((i,j), cboard)]
                if (turn == "White" and piece["Colour"] == "Black" and cboard[i][j] != "♙"):
                    print(cboard[i][j])
                    print(piece)
                    print(chesspieces.get(cboard[i][j]).get("validity_func")((i,j), wkingnow, cboard))
                    if chesspieces.get(cboard[i][j]).get("validity_func")((i,j), wkingnow, cboard) == True:
                        print("White King under check")
                        #return False
                    print(chesspieces.get(cboard[i][j]).get("validity_func")((i,j), wkingif, tempboard))
                    if chesspieces.get(cboard[i][j]).get("validity_func")((i,j), wkingif, tempboard) == True:
                        print("White King will be under check")
                        return False
                else:
                    print("No White Check")
                    return True
    return False
                    
def into_check(cboard, turn):
    return False

def checkpawn(cboard, turn):
    
    return False

def checkspecial():
    return False


def checkmate():
    return False   

def chess_game():
    print("Welcome to chess game!")
    print("Enter inputs in the following form: if white queen moves from")
    print("d1 to d5, enter Qd1d5. If it takes a piece while moving to d5,")
    print("enter Qd1xd5, ie. the x indicates capture.")
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
            #piecename = Move[0]
            stcord = (8-startrank, ord(startfile)-97)
            endcord = (8-endrank, ord(endfile)-97)
            capturestate = False
            if Move[-3]=="x":
                capturestate = True
            #print(startrank, startfile, endrank, endfile, capturestate)
            tempboard = deepcopy(cboard)
            tempboard[8-endrank][ord(endfile)-97]=tempboard[8-startrank][ord(startfile)-97]
            tempboard[8-startrank][ord(startfile)-97]=orboard[8-startrank][ord(startfile)-97]
            #tempboard = True
           
            if is_valid(turn, stcord, endcord, capturestate, cboard, tempboard):
                break
            print("Please enter a valid move.")

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