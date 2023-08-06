from chessprinting import *
from copy import deepcopy

#note this was written on dark mode, so the piece and square colours may be 
#switched in regular (light) mode

def pieces():
    orboard=chessboard()
    cboard=chessboard()
    cboard[0][0]=cboard[0][7]="♖"
    cboard[7][0]=cboard[7][7]="♜"
    #cboard[0][1]=cboard[0][6]="♘"
    #cboard[7][1]=cboard[7][6]="♞"
    #cboard[0][2]=cboard[0][5]="♗"
    #cboard[7][2]=cboard[7][5]="♝"
    #cboard[0][3]="♕"
    #cboard[7][3]="♛"
    cboard[0][4]="♔"
    cboard[7][4]="♚"
    for i in range (8):
        cboard[1][i]="♙"
    for i in range (8):
        cboard[6][i]="♟︎"
    #cboard[6][5]="♙"
    #cboard[1][5]="♟︎"
    #cboard[6][5]="♕"
    #cboard[5][5]="♕"
    #cboard[4][5]="♕"
    #cboard[3][7]="♛"
    #cboard[4][2]="♝"
    #cboard[0][0]="♟︎"
    #print_chessboard(cboard)
    
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
        #print('invalid pawn move')
        return False
    
#def
    
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

piecenames = {"P": "Pawn", "Q": "Queen", "K": "King", "R": "Rook",
              "N": "Knight", "B": "Bishop"}

validpromotion = ["N", "Q", "B", "R"]
whitepromotion = {"Q": "♛", "R": "♜", "N": "♞", "B": "♝"}
blackpromotion = {"Q": "♕", "R": "♖", "N": "♘", "B": "♗"}

validfiles = ["a", "b", "c", "d", "e", "f", "g", "h"]

validranks = ["1", "2", "3", "4", "5", "6", "7", "8"]

#generates a list of coordinates to avoid iteration later on
coords = [(i,j) for i in range(8) for j in range(8)]
        
    
    
def is_valid(turn, stcord, endcord, capturestate, cboard):
    #returns False if invalid, True otherwise
    # Positions must be within [0:7]
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
    return True

def isvalidpromotion(turn, Move, cboard):
    #returns False if invalid, True otherwise
    startrank = int(Move[2])
    startfile = Move[1]
    stcord = (8-startrank, ord(startfile)-97)
    if (square_status(stcord, cboard) == "♟︎") and (turn == "White") and \
    (startrank == 8) and (Move[-1] in validpromotion) == True:
        return True
    elif (square_status(stcord, cboard) == "♙") and (turn == "Black") and \
    (startrank == 1) and (Move[-1] in validpromotion) == True:
        return True
    return False

def isvalidcastle(turn, Move, cboard, castlestatus):
    #returns False if invalid, True otherwise
    if turn == "White" and castlestatus[1] == 0:
        if Move == "000" and castlestatus[0] == 0 and \
        rook_move((7,0), (7,3), cboard) == True: return True
        elif Move == "00" and castlestatus[2] == 0  and \
        rook_move((7,7), (7,5), cboard) == True: return True
        else: return False
    if turn == "Black" and castlestatus[4] == 0:
        if Move == "000" and castlestatus[3] == 0 and \
        rook_move((0,0), (0,3), cboard) == True: return True
        elif Move == "00" and castlestatus[5] == 0 and \
        rook_move((0,7), (0,5), cboard) == True: return True
        else: return False
    return False

def wking_location(cboard):
    for x in coords:
        if cboard[x[0]][x[1]] == "♚":
            #print(f" W king at {(i,j)}")
            return x
def bking_location(cboard):
    for x in coords:
        if cboard[x[0]][x[1]] == "♔":
            #print(f" B king at {(i,j)}")
            return x

def checkall(anyboard, turn): 
    #print("uptohere")
    #function returns true if under check, false otherwise
    wking = wking_location(anyboard)
    bking = bking_location(anyboard)
    for x in coords:
        i = x[0]
        j = x[1]
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
    #returns true if move is valid, false otherwise
    #print("started validity")
    if Move == "00" or Move == "000":
        return True
    #promotion
    if len(Move) == 4 and (Move[0] in dict.keys(piecenames)) == True \
    and (Move[1] in validfiles) == True and (Move[-1] in dict.keys(piecenames)) == True \
    and (Move[2] in validranks) == True:
        return True
    if len(Move) == 5 or (len(Move) == 6 and (Move[3] == "x" or Move[3] == "X")):
        if (Move[0] in dict.keys(piecenames)) == False:
            return False
        if (Move[1] in validfiles and Move[-2] in validfiles) == False:
            return False
        if (Move[-1] in validranks and Move[2] in validranks) == False:
            return False
        return True
    else: 
        return False

def rookandkingtracker(anyboard, turn_no):
    #initialise movement tracking of rooks and kings for castling
    #if piece has moved then status changes to True
    if turn_no != 1000:
        lwrook = wking = rwrook = lbrook = bking = rbrook = 0
    if square_status((0,0), anyboard) == False: lbrook = 1
    if square_status((0,4), anyboard) == False: bking = 1
    if square_status((0,7), anyboard) == False: rbrook = 1
    if square_status((7,0), anyboard) == False: lwrook = 1
    if square_status((7,4), anyboard) == False: wking = 1
    if square_status((7,7), anyboard) == False: rwrook = 1
    return[lwrook, wking, rwrook, lbrook, bking, rbrook]
    
def checkspecial():
    return False


def checkmate(anyboard, turn):
    #print("startedthis")
    if checkall(anyboard, turn) == False:
        #print("allfine")
        return False
    
    #seeing if there is a valid move to avoid check by taking checking piece
    for x in coords: 
        (i,j) = (x[0], x[1])
        currentsquare = (i,j)
        #print(currentsquare)
        #print(square_status((i,j), anyboard))
        if square_status((i,j), anyboard) != False:
            piece = chesspieces[square_status((i,j), anyboard)]
            #print(checkall(anyboard, turn))
            #while checkall(anyboard, turn) == True:
            for x in coords: 
                (m,n) = (x[0], x[1])
                potentialmove = (m,n)
                #print(potentialmove)
                #print(is_valid(turn, currentsquare, potentialmove, True, anyboard))
                if (is_valid(turn, currentsquare, potentialmove, True, anyboard) == True) \
                    or (is_valid(turn, currentsquare, potentialmove, False, anyboard) == True):
                    #print("there is a valid move")
                    #need to initialise position to see if still under check
                    orboard=chessboard()
                    ctempboard = deepcopy(anyboard)
                    ctempboard[m][n]=ctempboard[i][j]
                    ctempboard[i][j]=orboard[i][j]
                    #print_chessboard(ctempboard)
                    if checkall(ctempboard, turn) == False:
                        #print("not under check any more")
                        return False
    #otherwise, checkmate
    if turn == "White":
        print("Checkmate! Black wins!")
    else:
        print("Checkmate! White wins!")
    return True

def chess_game():
    print("Welcome to chess game! You may need to switch to dark mode.")
    print("Enter inputs in long algebraic form: if white queen moves from")
    print("d1 to d5, enter Qd1d5. If it takes a piece while moving to d5,")
    print("enter Qd1xd5, ie. the x indicates capture. To promote, enter")
    print("the pawn position followed by the letter of the intended piece,")
    print("eg. Pa8Q to promote to queen. To castle, enter 00 for kingside")
    print("and 000 for queenside castling. En passant is notated as a")
    print("regular capture; use the location of the captured pawn.")
    cboard = pieces()
    print_chessboard(cboard)
    orboard=chessboard()
    turn = "White"
    #turn = "Black"
    turn_no = 1
    castlestatus = [0, 0, 0, 0, 0, 0]
    while not checkmate(cboard, turn):
        while True:
            print(f"It is currently turn {turn_no}, {turn} to move.")
            if sum(rookandkingtracker(cboard, turn_no)) >= sum(castlestatus):
                castlestatus = rookandkingtracker(cboard, turn_no)
            #print(sum(castlestatus))
            tempboard = deepcopy(cboard)
            if checkall(cboard, turn) == True:
                print(f"Note that you are under check.")
            while True:   
                Move = input("Please enter your move in the above format. ")
                #print(movevalidity(Move))
                if movevalidity(Move):
                    break
                print("Please enter a valid move")
            #base placeholders below
            #print("uptohere")
            startrank = 1
            startfile = "a"
            endrank = 1
            endfile = "a"
            capturestate = False
            if len(Move) == 6 or len(Move) == 5:
                startrank = int(Move[2])
                startfile = Move[1]
                endrank = int(Move[-1])
                endfile = Move[-2]
                if Move[-3]=="x":
                    capturestate = True
                #print(startrank, startfile, endrank, endfile, capturestate)
                tempboard[8-endrank][ord(endfile)-97]=tempboard[8-startrank][ord(startfile)-97]
                tempboard[8-startrank][ord(startfile)-97]=orboard[8-startrank][ord(startfile)-97]
                #tempboard = True
                stcord = (8-startrank, ord(startfile)-97)
                endcord = (8-endrank, ord(endfile)-97)
                if (is_valid(turn, stcord, endcord, capturestate, cboard) and (not checkall(tempboard, turn))):
                    break
                print("Please enter a legal move")
            elif len(Move) == 4:
                #this for promotion
                startrank = int(Move[2])
                startfile = Move[1]
                if (isvalidpromotion(turn, Move, cboard)):
                    break 
                print("Please enter a legal promotion")
            elif Move == "000" or Move == "00":
                #print("herenow")
                if isvalidcastle(turn, Move, cboard, castlestatus):
                    break
                print("Please enter a valid castling")
        #next block prints in words the move
        if len(Move) == 6 or len(Move) == 5:
            print(f"{turn} {chesspieces[square_status(stcord, cboard)]['Type']} moves from {startfile}{startrank} to {endfile}{endrank}")
            if capturestate == True:
                print(f"and takes {turn} {chesspieces[square_status(endcord, cboard)]['Type']}")
        if len(Move) == 4:
            print(f"{turn} pawn on '{Move[1]}' file promotes to {piecenames[Move[-1]]}")
        if Move == "000":
            print(f"{turn} castles queenside")
        if Move == "00":
            print(f"{turn} castles kingside")
        #need to replace start position with original board square
        if len(Move) == 6 or len(Move) == 5:
            cboard[8-endrank][ord(endfile)-97]=cboard[8-startrank][ord(startfile)-97]
            cboard[8-startrank][ord(startfile)-97]=orboard[8-startrank][ord(startfile)-97]
        #for promotion
        elif len(Move) == 4:
            if turn == "White":
                cboard[8-startrank][ord(startfile)-97]=f"{whitepromotion[Move[-1]]}"
        elif (Move == "000" or Move == "00") and turn == "White":
            cboard[7][4] = orboard[7][4]
            if Move == "000": cboard[7][2], cboard[7][3], cboard[7][0] = "♚", "♜", orboard[7][0]
            else: cboard[7][6], cboard[7][5], cboard[7][7] = "♚", "♜", orboard[7][7]
        elif (Move == "000" or Move == "00") and turn == "Black":
            cboard[0][4] = orboard[0][4]
            if Move == "000": cboard[0][2], cboard[0][3], cboard[0][0] = "♔", "♖", orboard[0][0]
            else: cboard[0][6], cboard[0][5], cboard[0][7] = "♔", "♖", orboard[0][7]
        
        if turn == "White":
            turn = "Black"
        else:
            turn = "White"
            turn_no += 1
        print("")
        print("The current state is below:")
        print_chessboard(cboard)

chess_game()