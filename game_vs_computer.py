"""
Created on Sun Nov 10 13:58 2024.

@author: AVITA
"""

import helper
import pygame
import random
import sys
import os

pygame.init()
MAX_WIDTH = 1920
MAX_HEIGHT = 970
WIDTH = 720
HEIGHT = WIDTH
window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()
FPS = 60

white = (255, 255, 255)
black = (0, 0, 0)

move_sfx = pygame.mixer.Sound("Assets" + os.sep + "sound" + os.sep + "move.mp3")
kill_sfx = pygame.mixer.Sound("Assets" + os.sep + "sound" + os.sep + "kill.mp3")

board = helper.Board(WIDTH, HEIGHT)
tile_list = [board.tiles[i][j] for i in range(8) for j in range(8)]

white_set = helper.Piece_Set()
white_set.create_pieces(WIDTH, HEIGHT, white, "white", board, 1)
black_set = helper.Piece_Set()
black_set.create_pieces(WIDTH, HEIGHT, black, "black", board, 2)
piece_list = white_set.pieces + black_set.pieces

selected_piece = None
selected_tiles = []

turn = "white"

while True:

    # Window

    board.display(window)
    white_set.display(window)
    black_set.display(window)

    # Computer Logic

    if turn == "black":

        selected_piece = None
        for tile in selected_tiles:
            tile.selected = False
        selected_tiles = []

        chosen_piece = random.choice([piece for piece in black_set.pieces])
        chosen_piece.selected = not chosen_piece.selected

        for piece in black_set.pieces:
            if piece != chosen_piece:
                piece.selected = False
        selected_piece = chosen_piece
        selected_tiles = chosen_piece.if_selected(tile_list, piece_list, board)

        if selected_tiles != []:
            chosen_move = random.choice([tile for tile in selected_tiles])
            if chosen_move.is_empty(piece_list):
                pygame.mixer.Channel(1).play(move_sfx)
                selected_piece.rect.center = chosen_move.rect.center

                selected_piece.selected = False
                turn = "white"
            else:
                if chosen_move.is_opp_color(piece_list, selected_piece.color)[0]:
                    pygame.mixer.Channel(2).play(kill_sfx)
                    piece_to_remove = chosen_move.is_opp_color(piece_list, selected_piece.color)[1]
                    if piece_to_remove.type == "king":
                        print("Black Won")
                        pygame.quit()
                        sys.exit()

                    selected_piece.rect.center = chosen_move.rect.center
                    white_set.pieces.remove(piece_to_remove)
                    piece_list.remove(piece_to_remove)

                    selected_piece.selected = False
                    turn = "white"  
    
    # Events

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if (event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]) or (event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_w]):
            for tile in selected_tiles:
                if tile.to_move_selected():

                    if tile.is_empty(piece_list):
                        pygame.mixer.Channel(3).play(move_sfx)
                        selected_piece.rect.center = tile.rect.center

                        selected_piece.selected = False
                        turn = "black"  
                    else:
                        if tile.is_opp_color(piece_list, selected_piece.color)[0]:
                            pygame.mixer.Channel(4).play(kill_sfx)
                            piece_to_remove = tile.is_opp_color(piece_list, selected_piece.color)[1]
                            if piece_to_remove.type == "king":
                                print("WHite Won")
                                pygame.quit()
                                sys.exit()

                            selected_piece.rect.center = tile.rect.center
                            black_set.pieces.remove(piece_to_remove)
                            piece_list.remove(piece_to_remove)

                            selected_piece.selected = False
                            turn = "black"  
                    selected_piece.selected = False
                    
            selected_piece = None
            for tile in selected_tiles:
                tile.selected = False
            selected_tiles = []

            for tile in tile_list:
                if turn == "white":
                    tile.selected = tile.is_selected(white_set.pieces)

            for piece in piece_list:
                if piece.selected:
                    selected_piece = piece
                    selected_tiles = piece.if_selected(tile_list, piece_list, board)
                
            for tile in selected_tiles:
                tile.selected = True

    # Screen Update

    pygame.display.update()
    clock.tick(FPS)
