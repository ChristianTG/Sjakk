# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 14:20:05 2018

@author: KKKKKKristian  V  BLLLLLLLLage
"""

import numpy as np
from random import shuffle
import pygame
from ctypes import windll

def decode(coord):
    '''Converts positional coordinates (y, x)
    to established cheess-format (a1)'''
    return 'abcdefgh'[coord[1]] + str(8-coord[0])

def encode(s):
    '''Converts established chess-format (a1)
    to positional coordinates (y, x)'''
    return 8-int(s[1]), 'abcdefgh'.index(s[0])

def compare(pos0, pos, board_input=[]):
    '''Compares the piece in pos0 with the piece in pos.
    Returns values:
    0 - pos is outside the board
    1 - pos is empty
    2 - pos0 and pos have different colored pieces
    3 - pos0 and pos have the same colored pieces
    '''
    board_input = board_changer (board_input)
    
    def in_board(pos):
        '''Test to check of a positional coordinate is in the chess board'''
        if min(pos) < 0 or max(pos) > 7: return False
        return True
    
    if not in_board(pos): return 0
    if board_input[pos] == 0: return 1
    elif board_input[pos0] // abs(board_input[pos0]) == -(board_input[pos] // abs(board_input[pos])): return 2
    elif board_input[pos0] // abs(board_input[pos0]) == board_input[pos] // abs(board_input[pos]): return 3


def check_test(board_input=[], no_king=False):
    
    board_input = board_changer (board_input)
        
    checks = []
    for y in range(8):
        for x in range(8):
            if board_input[y][x] == 6*turn:
                pos = (y, x)
                possibleChecks = [pawn_moves(pos, True, board_input), rook_moves(pos, board_input), knight_moves(pos, board_input), bishop_moves(pos, board_input), queen_moves(pos, board_input)]
                
                for possiblePawnCheck in (possibleChecks[0]):
                    if board_input[possiblePawnCheck] == 1*(-turn):
                        checks.append(possiblePawnCheck)
                
                for possibleRookCheck in (possibleChecks[1]):
                     if board_input[possibleRookCheck] == 2*(-turn):
                        checks.append(possibleRookCheck)
                
                for possibleKnightCheck in (possibleChecks[2]):
                     if board_input[possibleKnightCheck] == 3*(-turn):
                        checks.append(possibleKnightCheck)
                
                for possibleBishopCheck in (possibleChecks[3]):
                     if board_input[possibleBishopCheck] == 4*(-turn):
                        checks.append(possibleBishopCheck)
                        
                for possibleQueenCheck in possibleChecks[4]:
                     if board_input[possibleQueenCheck] == 5*(-turn):
                        checks.append(possibleQueenCheck)
                        
                if not no_king:
                    
                    possibleChecks.append(king_moves(pos, board_input))
                    
                    for possibleKingCheck in possibleChecks[5]:
                        if board_input[possibleKingCheck] == 6*(-turn):
                            checks.append(possibleKingCheck)
    
    return tuple(checks)


def move(pos0, pos):
    '''Moves a piece to a new coordinate, setting zero at its starting
    position and replacing the piece at the new position'''
    board[pos] = board[pos0]
    board[pos0] = 0

def try_move(pos0, pos):
    '''Main function to attempt moving a piece
    Takes inputs in positional coordinates'''
    global turn 
    
    piece = board[pos0]
    
    print ("piece is", piece)
    if not piece: return False
    if piece < 0 and turn == white: return False
    if piece > 0 and turn == black: return False
    
    piece *= turn
    
    if piece == 1: legal_moves = pawn_moves(pos0)
    if piece == 2: legal_moves = rook_moves(pos0)
    if piece == 3: legal_moves = knight_moves(pos0)
    if piece == 4: legal_moves = bishop_moves(pos0)
    if piece == 5: legal_moves = queen_moves(pos0)
    if piece == 6: legal_moves = king_moves(pos0)
    
    if not pos in legal_moves: return False
    
    if not board[pos] == 0:
        if turn == white: dead_black.append(board[pos])
        if turn == black: dead_white.append(board[pos])
    
    move(pos0, pos)
    turn *= -1
    return True
    
def play():
    global color, turn, mouse_mode
    if turn == white: color = 'White'
    elif turn == black: color = 'Black'
    print(f"\n\n{color}'s turn.")
    global checks, in_check, board
    checks = check_test([], True)
    if len (checks) > 0: 
        print(f"\n{color} is in check!")
        checkmate_test()
        for check in checks:
            print("King is threatned by", decode(check))
            
    PyGame(mouse_mode)
    if mouse_mode: return
    
    userinput = input('Please move a piece: ')
    
    if userinput == "exit": return
    if userinput == "reset": new_game(); play(); return
    if userinput == "reset fischer": new_game(True); play(); return
    if userinput == "turn":
        if turn == 1: turn = -1
        else: turn = 1
        play()
        return
    if userinput == "test": board = custom_boards[1]; play(); return
    for number in range (len(custom_boards)):
        if userinput == f"custom {number+1}": 
            board = custom_boards[number].copy()
            print (f"\n{board}")
            play()
            return
    
    #The following code introduces an unofficial game mode based on an
    #earlier bug in the game's code caused by BlaggyBOY's sloppy coding :P
    if userinput == "toggle glitch mode": global glitch_mode; glitch_mode = not glitch_mode; print(f"\nGlitch mode set to {glitch_mode}"); play(); return

    userinput = "".join(userinput.split(" ")) # Removes spaces in the userinput string
    
    try: move = try_move(encode(userinput[:2]), encode(userinput[2:]))
    except Exception as error:
        print (error)
        print("\nInvalid input")
        print(f'\n{board}')
        play()
        return
    
    if not move: print('\nMove not valid')
    print(f'\n{board}')
    
    play()

#Functions for returning all legal moves for the different pieces
'''Return a tuple/list of all positions (encoded) after legal moves'''

def pawn_moves(pos, only_attacks=False, board_input=[]):
    
    board_input = board_changer (board_input)
    
    global turn
    potentials = []
    potentials_attack = []
    moves = []
        

    potentials.append((pos[0] + (-turn), pos[1]))
    
    for i in (-1, 1):
        potentials_attack.append((pos[0] + (-turn), pos[1]+i))
    
    if pos[0] == 1 or pos[0] == 6:
        potentials.append((pos[0] + (2*-turn), pos[1]))
    
    for potential in potentials:
        if compare(pos, potential, board_input) == 1:
            moves.append(potential)
        else: break # Breaking, so that the pawn won't skip an occupied square 
    
    if only_attacks:
        moves.clear() #Clears the moves-list, so that only attacking moves can be returned 
   
    for potential in potentials_attack:
        
        if compare (pos, potential, board_input) == 2:
            moves.append(potential)
    
    
    moves = new_board_test(pos, moves)
            
    return tuple(moves)

def rook_moves(pos, board_input=[]):
    
    board_input = board_changer (board_input)
    
    global glitch_mode
    
    moves = []
    for i in (1, -1):
        for j in (0, 1):
            checkslot = list(pos)
            while True:
                checkslot[j] += i
                comparison = compare(pos, tuple(checkslot), board_input)
                
                if comparison == 1:
                    moves.append(tuple(checkslot))
                    
                elif comparison == 2:
                    moves.append(tuple(checkslot))
                    break
                
                elif comparison == 3 and not glitch_mode:
                    break
                
                elif comparison == 0:
                    break
                
     
        
    moves = new_board_test(pos, moves)
            
    
    return tuple(moves)
                    
    
def knight_moves(pos, board_input=[]):
    
    board_input = board_changer (board_input)
    
    potentials = []
    moves = []
    for i in (1, -1):
        for j in (2, -2):
            potentials.append((pos[0]+i, pos[1]+j))
            potentials.append((pos[0]+j, pos[1]+i))
    
    for move in potentials:
        if compare(pos, move, board_input) in (1, 2):
            moves.append(move)
    
    
    moves = new_board_test(pos, moves)
    
    return tuple(moves)


def board_changer (board_input):
    
    global board
    if len(board_input) == 0:
        board_input = board.copy()
    return board_input



def bishop_moves(pos, board_input=[]):
    
    global glitch_mode
    
    board_input = board_changer (board_input)
    
    
    moves = []
    for i in (1, -1):
        for j in (1, -1):
            checkslot = list(pos)
            while True:
                checkslot[0] += i
                checkslot[1] += j
                comparison = compare(pos, tuple(checkslot), board_input)
                
                if comparison == 1:
                    moves.append(tuple(checkslot))
                    
                elif comparison == 2:
                    moves.append(tuple(checkslot))
                    break
                
                elif comparison == 3 and not glitch_mode:
                    break
                
                elif comparison == 0:
                    break
                
    
   
    moves = new_board_test(pos, moves)        
    
        
    return tuple(moves)
        

def queen_moves(pos, board_input=[]):
    
    board_input = board_changer (board_input)
    
    moves = tuple(list(rook_moves(pos, board_input)) + list(bishop_moves(pos, board_input)))
    
    moves = new_board_test(pos, moves)
    
    return moves

def king_moves(pos, board_input=[]):
    
    board_input = board_changer (board_input)
    
    potentials = []
    moves = []
    for i in (1, -1):
        potentials.append((pos[0]+i, pos[1]))
        potentials.append((pos[0], pos[1]+i))
    
    for i in (1, -1):
        potentials.append((pos[0]+i, pos[1]+i))
        potentials.append((pos[0]+i, pos[1]-i))
    
    for move in potentials:
        if compare(pos, move, board_input) in (1, 2):
            moves.append(move)
    
    moves = new_board_test (pos, moves, True)
    
    return tuple(moves)    



def new_board_test (pos, moves, actualKingMoves=False):
    
    global is_real
    
    actualMoves = False # To prevent the king's check_test from treating the king as a piece which can move as every other piece combined, and using this to find legal moves which escape the current check position.
    if abs(board[pos]) != 6 or actualKingMoves:
        actualMoves = True
   
    if is_real and actualMoves:
        is_real = False
        b = tuple(moves)
        for move in b:
#            print ("\nValidating move:", move)
            new_board = board.copy()
            new_board[move] = new_board[pos]
            new_board[pos] = 0
#            print (f"\nIf player were to move the piece to {decode(move)};  \n\n{new_board}")
            
            new_checks = check_test(new_board)
            
#            print ("\nNumber of pieces threatning check: ", len(new_checks))
            
            if len (new_checks) != 0:
                for new_check in new_checks:
#                    print (f"\nPiece {new_checks.index(new_check)+1} is {decode(new_check)}") 
#                
#                print(f"\nAs a result, {move}/{decode(move)} is an illegal move")
#                print ("\nremoves ", move, "from moves list")
                 try: moves.remove(move)
                 except: pass
#                print ("Remaing moves are", moves)
            
#            elif len (new_checks) == 0:
#                print(f"\nNo check in this board; {move}/{decode(move)} is a legal move")
                
#        if len(moves) > 0: print (f"\n\nAll moves have been validated!\nThe following moves are legal")
#        else: print (f"\n\nAll moves have been validated!\nThere are no legal moves")
#        for move in moves:
#            print(f"{moves.index(move)+1}: {decode(move)}")
        is_real = True
        
    return moves

def checkmate_test ():
    
    global turn, color, board
    
    print ("Running checkmate_test")
    
    legal_moves = []
        
    for y in range (8):
        for x in range (8):

            pos = (y, x)
            
            piece = board[pos]
                    
            piece *= turn
    
            if piece == 1: legal_moves.append(pawn_moves(pos))
            if piece == 2: legal_moves.append(rook_moves(pos))
            if piece == 3: legal_moves.append(knight_moves(pos))
            if piece == 4: legal_moves.append(bishop_moves(pos))
            if piece == 5: legal_moves.append(queen_moves(pos))
            if piece == 6: legal_moves.append(king_moves(pos))
            
    
    
    for tuppel in legal_moves:
        if len(tuppel) > 0: return
    
    print (f"\n{color} is checkmate!")
    
    if color == "White": color2 = "Black"
    else: color2 = "White"
    
    print (f"\nCongratulations {color2}!")
    
    if input("\nType reset to restart: ") == "reset": 
        new_game()
        global mouse_mode
        if not mouse_mode: play()
        return
    else: checkmate_test ()
    
        

def new_game(fischer=False):
    
    global board
    global black
    global white
    global turn
    global dead_black
    global dead_white
    global checks
    
    checks = tuple([])
    
    black = -1
    white = 1
    
    turn = white
    
    board = np.zeros([8, 8], int)
    
    pawn = 1
    rook = 2
    knight = 3
    bishop = 4
    queen = 5
    king = 6
    start_row = [rook, knight, bishop, queen, king, bishop, knight, rook]
    
    if fischer: shuffle(start_row)
    
    board[1, :] = black*pawn
    board[6, :] = white*pawn
    
    board[0, :] = black*np.array(start_row)
    board[7, :] = white*np.array(start_row)
    
    dead_black = []
    dead_white = []
    
    # Custom Boards
    global custom_boards
    custom_boards = []
    custom1 = board.copy(); custom1[3, :] = black*np.array(start_row); custom1[4, :] = white*np.array(start_row); custom_boards.append(custom1)
    custom2 = board.copy(); custom2[encode("b5")] = 4; custom2[encode("d7")] = 0; custom_boards.append(custom2)
    # Custom board 3
    custom3 = board.copy()
    custom3[encode("d4")] = 1; custom3[encode("d2")] = 0
    custom3[encode("d5")] = -1; custom3[encode("d7")] = 0
    custom3[encode("b5")] = 5; custom3[encode("d1")] = 0
    custom3[encode("f6")] = -3; custom3[encode("g8")] = 0
    custom_boards.append(custom3)
    
    print(f"\n{board}")
    
print ("Welcome to the most incredible piece of engineering any human has",
       "\never laid their eyes on: a Game of Chess programmed in Python!",
       "\nby KKKKKKristian and BlaggyBOY\n")    



#Glitch mode initialization
global glitch_mode
glitch_mode = False

global is_real
is_real = True
# Pygame related initialization

global mouse_mode
mouse_mode = True

pygame.init()

pygame.display.set_caption("Game of Chess")

screen_size = (800, 800) #Default Value

try:
    screen_size_input = int(input("Set screen size (screen is always square, so only one value): "))
    if screen_size_input % 8 != 0: # If the input isn't a multiple of 8...
        print (f"N.B. The screen size must be divisible by 8!",
        "\nSetting screen size to closest divisible number.")
        screen_size_input -= screen_size_input % 8
    screen_size_input = (screen_size_input, screen_size_input)
    win = pygame.display.set_mode(screen_size_input)
    screen_size = screen_size_input
    print(f"Screen size set to {screen_size}\n")
    
except:
    print(f"\nSetting screen size to default {screen_size}\n")
    win = pygame.display.set_mode(screen_size)

# The code below forces the pygame window to always stay on top of other windows
SetWindowPos = windll.user32.SetWindowPos
SetWindowPos(pygame.display.get_wm_info()['window'], -1, 0, 0, 0, 0, 0x0001)

win.fill((255,255,255))



# LOADING IMAGES

background = pygame.image.load("Images/plain_board.png")
background = pygame.transform.scale(background, screen_size)

black_marked = pygame.image.load("Images/black_square_marked.png")
white_marked = pygame.image.load("Images/white_square_marked.png")

black_marked = pygame.transform.scale(black_marked, (screen_size[0] // 8, screen_size[1] // 8))
white_marked = pygame.transform.scale(white_marked, (screen_size[0] // 8, screen_size[1] // 8))


white_piece_images = []
black_piece_images = []

# The for-loops below are used for loading images.
# This only happens once; at boot-up. Not every time the graphics are updated.

for i in range (6):
    image = pygame.image.load(f"Images/white_indexed/{i+1}.png")
    try:
        image = pygame.transform.scale(image, (screen_size[0] // 8, screen_size[1] // 8))
        white_piece_images.append(image)
    except ValueError:
        print("Size of board must be divisable by 8 (e.g. 800, 600 or 400)")
        
# No reason to check for board size value error in the for-loop below.
# If there is an exception, it will be caught by the preceeding loop
for i in range (6):
    image = pygame.image.load(f"Images/black_indexed/{i+1}.png")
    image = pygame.transform.scale(image, (int(screen_size[0]) // 8, int(screen_size[1]) // 8))
    black_piece_images.append(image)



# Pygame related function

def PyGame (mouse_mode):
    
    checks = []
    run = True
    can_press = True
    target_piece = []
    
    while run:

    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
        
        win.blit(background, (0, 0)) # Clearing the board before displaying updated piece positions
        
        pressed = pygame.mouse.get_pressed()
        if pressed[0] and can_press:
            print("Left Mouse")
            can_press = False
            mouse_pos = pygame.mouse.get_pos()
            y = int(mouse_pos[1] * (800 / screen_size[0] / 100))
            x = int(mouse_pos[0] * (800 / screen_size[0] / 100))
            pos = (y, x)
            print (pos)
                
            
            
            # Regardless of whether marked_square or new_marked_square will 
            # be updated, this code is the same
            # therefore, it's not inside the if-statement
            
            if (pos[0] + pos[1]) % 2 != 0: image = black_marked
            else: image = white_marked
            
            
            x = x * int(screen_size[0] / 800 * 100)
            y = y * int(screen_size[0] / 800 * 100)
            
            
            if (pos == target_piece):
                if turn == 1: marked_square_white = False
                else: marked_square_black = False
                target_piece = []
            
            elif (board[pos] * turn) > 0:
                
                target_piece = pos
                
                win.blit(image, (x, y))
                print (image, (x, y))
                
                if turn == 1: marked_square_white = (image, (x, y))
                else: marked_square_black = (image, (x, y))
                
                
            else:
                
                if len(target_piece) != 0:
                    print ("The tuple", tuple(target_piece))
                    move = try_move(tuple(target_piece), pos)
                
                    if move: 
                        new_marked_square = (image, (x, y))
                        target_piece = []
                        if turn == 1: marked_square_white = False
                        else: marked_square_black = False
                        
                        checks = check_test()
                        
                    
            
            
        if not pressed[0]: can_press = True
        
        try: win.blit (marked_square_black[0], marked_square_black[1])
        except: pass
        try: win.blit (marked_square_white[0], marked_square_white[1])
        except: pass
        try: win.blit (new_marked_square[0], new_marked_square[1])
        except: pass
            
        for i in range(8): # Cycles through every square of the board to check if a piece of any color should be drawn 
            for j in range(8):
                    
                if board[i,j] > 0: # A positive value means the square is occupied by a white piece
                    y = i * (screen_size[0] / 8) 
                    x = j * (screen_size[0] / 8)
                        
                    win.blit(white_piece_images[board[i,j]-1], (x, y))
                        
                elif board[i,j] < 0: # A negative value means the square is occupied by a black piece
                    y = i * (screen_size[0] / 8) 
                    x = j * (screen_size[0] / 8)
                            
                    win.blit(black_piece_images[abs(board[i,j])-1], (x, y))
        
    
        pygame.display.flip()
        
        if len (checks) > 0: 
            global color
            if color == "White": color = "Black"
            else: color == "White" 
            print(f"\n{color} is in check!")
            checkmate_test()
            checks = []
            marked_square_white = False
            marked_square_black = False
            new_marked_square = False
        
        if not mouse_mode: run = False
    
    #return True; Only useable if we plan to exit the program by mouse clicking

new_game()
play()
    
pygame.quit()