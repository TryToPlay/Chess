"""
Created on Sun Nov 10 13:58 2024.

@author: AVITA
"""

import pygame
import os

class Tile():
    def __init__(self, color, width, height, x, y):
        self.rect = pygame.Rect(0, 0, width / 8, height / 8)
        self.pos = (x, y)
        self.rect.center = self.pos
        self.color = color
        self.selected = False
    
    def has_piece(self, pieces):
        for piece in pieces:
            if self.rect.center == piece.rect.center:
                return (True, piece)
        return (False, None)
    
    def is_selected(self, pieces):
        for piece in pieces:
            if self.rect.center == piece.rect.center:
                mouse_pos = pygame.mouse.get_pos()
                if self.rect.collidepoint(mouse_pos):
                    piece.selected = not piece.selected
                    return piece.selected
                else:
                     piece.selected = False

    def to_move_selected(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
             return True
        return False
    
    def is_empty(self, pieces):
        for piece in pieces:
            if self.rect.center == piece.rect.center:
                return False
        return True

    def is_opp_color(self, pieces, selected_color):
         for piece in pieces:
              if self.rect.center == piece.rect.center:
                   if piece.color != selected_color:
                        return (True, piece)
                   else:
                        return (False, piece)

class Board():
    def __init__(self, width, height):
        self.tiles = []
        a = 1
        white = (255,255, 255)
        black = (0, 0, 0)
        for i in range(8):
            row = []
            for j in range(8):
                if i%2 == 0:
                    if a%2 != 0:
                        tile = Tile(white, width, height, (width / 16) + (i * (width / 8)), (height / 16) + (j * (height / 8)))
                    else:
                        tile = Tile(black, width, height, (width / 16) + (i * (width / 8)), (height / 16) + (j * (height / 8)))
                else:
                    if a%2 != 0:
                        tile = Tile(black, width, height,(width / 16) + (i * (width / 8)), (height / 16) + (j * (height / 8)))
                    else:
                        tile = Tile(white, width, height,(width / 16) + (i * (width / 8)), (height / 16) + (j * (height / 8)))
                a += 1
                row.append(tile)
            self.tiles.append(row)
        for i in range(8):
            for j in range(8):
                temp0 = self.tiles[i][j].pos[0]
                temp1 = self.tiles[i][j].pos[1]
                self.tiles[i][j].pos = (temp1, temp0)
    
    def display(self, window):
        for tile in [self.tiles[i][j] for i in range(8) for j in range(8)]:
            if tile.selected:
                if tile.color == (0, 0, 0):
                    pygame.draw.rect(window, (85, 85, 85), tile.rect)
                if tile.color == (255, 255, 255):
                    pygame.draw.rect(window, (170, 170, 170), tile.rect)
            else:
                pygame.draw.rect(window, tile.color, tile.rect)

class Piece():
    def __init__(self, width, height, x, y, image_path, color):
        self.sprite = pygame.transform.scale(pygame.image.load(image_path), (width / 10, height / 10)).convert_alpha()
        self.rect = self.sprite.get_rect()
        self.rect.center = (x, y)
        self.color = color
        self.alive = True
        self.type = None
        self.selected = False
    
    def on_tile(self, tiles):
        for tile in tiles:
            if tile.rect.center == self.rect.center:
                return tile
    
    def if_selected(self):
        pass

class Rook(Piece):
    def __init__(self, width, height, x, y, image_path, color):
        super().__init__(width, height, x, y, image_path, color)
        self.type = "rook"
    
    def if_selected(self, tiles, pieces, board):
        tiles_to_be_selected = []
        self_tile = self.on_tile(tiles)

        for tile_list in board.tiles:
            if self_tile in tile_list:
                self_tile_x = board.tiles.index(tile_list)
                self_tile_y = tile_list.index(self_tile)
        
        for y in range(1, 8):
            if self_tile_y - y < 0:
                break
            tile_to_check = board.tiles[self_tile_x][self_tile_y - y]
            result = tile_to_check.has_piece(pieces)
            if result[0]:
                if result[1].color != self.color:
                    tiles_to_be_selected.append(tile_to_check)
                break
            else:
                tiles_to_be_selected.append(tile_to_check)
        for y in range(1, 8):
            if self_tile_y + y > 7:
                break
            tile_to_check = board.tiles[self_tile_x][self_tile_y + y]
            result = tile_to_check.has_piece(pieces)
            if result[0]:
                if result[1].color != self.color:
                    tiles_to_be_selected.append(tile_to_check)
                break
            else:
                tiles_to_be_selected.append(tile_to_check)
        for x in range(1, 8):
            if self_tile_x - x < 0:
                break
            tile_to_check = board.tiles[self_tile_x - x][self_tile_y]
            result = tile_to_check.has_piece(pieces)
            if result[0]:
                if result[1].color != self.color:
                    tiles_to_be_selected.append(tile_to_check)
                break
            else:
                tiles_to_be_selected.append(tile_to_check)
        for x in range(1, 8):
            if self_tile_x + x > 7:
                break
            tile_to_check = board.tiles[self_tile_x + x][self_tile_y]
            result = tile_to_check.has_piece(pieces)
            if result[0]:
                if result[1].color != self.color:
                    tiles_to_be_selected.append(tile_to_check)
                break
            else:
                tiles_to_be_selected.append(tile_to_check)

        return tiles_to_be_selected

class Bishop(Piece):
    def __init__(self, width, height, x, y, image_path, color):
        super().__init__(width, height, x, y, image_path, color)
        self.type = "bishop"
    
    def if_selected(self, tiles, pieces, board):
        tiles_to_be_selected = []
        self_tile = self.on_tile(tiles)

        for tile_list in board.tiles:
            if self_tile in tile_list:
                self_tile_x = board.tiles.index(tile_list)
                self_tile_y = tile_list.index(self_tile)

        for x in range(1, 8):
                y = x
                if self_tile_y - y < 0 or self_tile_x - x < 0:
                    break
                tile_to_check = board.tiles[self_tile_x - x][self_tile_y - y]
                result = tile_to_check.has_piece(pieces)
                if result[0]:
                    if result[1].color != self.color:
                        tiles_to_be_selected.append(tile_to_check)
                    break
                else:
                    tiles_to_be_selected.append(tile_to_check)
        for x in range(1, 8):
                y = x
                if self_tile_y + y > 7 or self_tile_x - x < 0:
                    break
                tile_to_check = board.tiles[self_tile_x - x][self_tile_y + y]
                result = tile_to_check.has_piece(pieces)
                if result[0]:
                    if result[1].color != self.color:
                        tiles_to_be_selected.append(tile_to_check)
                    break
                else:
                    tiles_to_be_selected.append(tile_to_check)
        for x in range(1, 8):
                y = x
                if self_tile_y - y < 0 or self_tile_x + x > 7:
                    break
                tile_to_check = board.tiles[self_tile_x + x][self_tile_y - y]
                result = tile_to_check.has_piece(pieces)
                if result[0]:
                    if result[1].color != self.color:
                        tiles_to_be_selected.append(tile_to_check)
                    break
                else:
                    tiles_to_be_selected.append(tile_to_check)
        for x in range(1, 8):
                y = x
                if self_tile_y + y > 7 or self_tile_x + x > 7:
                    break
                tile_to_check = board.tiles[self_tile_x + x][self_tile_y + y]
                result = tile_to_check.has_piece(pieces)
                if result[0]:
                    if result[1].color != self.color:
                        tiles_to_be_selected.append(tile_to_check)
                    break
                else:
                    tiles_to_be_selected.append(tile_to_check)

        return tiles_to_be_selected

class Horse(Piece):
    def __init__(self, width, height, x, y, image_path, color):
        super().__init__(width, height, x, y, image_path, color)
        self.type = "horse"
    
    def if_selected(self, tiles, pieces, board):
        tiles_to_be_selected = []
        self_tile = self.on_tile(tiles)

        for tile_list in board.tiles:
            if self_tile in tile_list:
                self_tile_x = board.tiles.index(tile_list)
                self_tile_y = tile_list.index(self_tile)

        y, x = 1, 2
        if not (self_tile_y - y < 0 or self_tile_x - x < 0):
            tile_to_check = board.tiles[self_tile_x - x][self_tile_y - y]
            result = tile_to_check.has_piece(pieces)
            if result[0]:
                 if result[1].color != self.color:
                    tiles_to_be_selected.append(tile_to_check)
            else:
                tiles_to_be_selected.append(tile_to_check)
        y, x = 1, 2
        if not (self_tile_y + y > 7 or self_tile_x - x < 0):
            tile_to_check = board.tiles[self_tile_x - x][self_tile_y + y]
            result = tile_to_check.has_piece(pieces)
            if result[0]:
                 if result[1].color != self.color:
                    tiles_to_be_selected.append(tile_to_check)
            else:
                tiles_to_be_selected.append(tile_to_check)
        y, x = 1, 2
        if not (self_tile_y - y < 0 or self_tile_x + x > 7):
            tile_to_check = board.tiles[self_tile_x + x][self_tile_y - y]
            result = tile_to_check.has_piece(pieces)
            if result[0]:
                 if result[1].color != self.color:
                    tiles_to_be_selected.append(tile_to_check)
            else:
                tiles_to_be_selected.append(tile_to_check)
        y, x = 1, 2
        if not (self_tile_y + y > 7 or self_tile_x + x > 7):
            tile_to_check = board.tiles[self_tile_x + x][self_tile_y + y]
            result = tile_to_check.has_piece(pieces)
            if result[0]:
                 if result[1].color != self.color:
                    tiles_to_be_selected.append(tile_to_check)
            else:
                tiles_to_be_selected.append(tile_to_check)
        y, x = 2, 1
        if not (self_tile_y - y < 0 or self_tile_x - x < 0):
            tile_to_check = board.tiles[self_tile_x - x][self_tile_y - y]
            result = tile_to_check.has_piece(pieces)
            if result[0]:
                 if result[1].color != self.color:
                    tiles_to_be_selected.append(tile_to_check)
            else:
                tiles_to_be_selected.append(tile_to_check)
        y, x = 2, 1
        if not (self_tile_y + y > 7 or self_tile_x - x < 0):
            tile_to_check = board.tiles[self_tile_x - x][self_tile_y + y]
            result = tile_to_check.has_piece(pieces)
            if result[0]:
                 if result[1].color != self.color:
                    tiles_to_be_selected.append(tile_to_check)
            else:
                tiles_to_be_selected.append(tile_to_check)
        y, x = 2, 1
        if not (self_tile_y - y < 0 or self_tile_x + x > 7):
            tile_to_check = board.tiles[self_tile_x + x][self_tile_y - y]
            result = tile_to_check.has_piece(pieces)
            if result[0]:
                 if result[1].color != self.color:
                    tiles_to_be_selected.append(tile_to_check)
            else:
                tiles_to_be_selected.append(tile_to_check)
        y, x = 2, 1
        if not (self_tile_y + y > 7 or self_tile_x + x > 7):
            tile_to_check = board.tiles[self_tile_x + x][self_tile_y + y]
            result = tile_to_check.has_piece(pieces)
            if result[0]:
                 if result[1].color != self.color:
                    tiles_to_be_selected.append(tile_to_check)
            else:
                tiles_to_be_selected.append(tile_to_check)

        return tiles_to_be_selected

class Queen(Piece):
    def __init__(self, width, height, x, y, image_path, color):
        super().__init__(width, height, x, y, image_path, color)
        self.type = "queen"
    
    def if_selected(self, tiles, pieces, board):
        tiles_to_be_selected = []
        self_tile = self.on_tile(tiles)

        for tile_list in board.tiles:
            if self_tile in tile_list:
                self_tile_x = board.tiles.index(tile_list)
                self_tile_y = tile_list.index(self_tile)
        
        for y in range(1, 8):
            if self_tile_y - y < 0:
                break
            tile_to_check = board.tiles[self_tile_x][self_tile_y - y]
            result = tile_to_check.has_piece(pieces)
            if result[0]:
                if result[1].color != self.color:
                    tiles_to_be_selected.append(tile_to_check)
                break
            else:
                tiles_to_be_selected.append(tile_to_check)
        for y in range(1, 8):
            if self_tile_y + y > 7:
                break
            tile_to_check = board.tiles[self_tile_x][self_tile_y + y]
            result = tile_to_check.has_piece(pieces)
            if result[0]:
                if result[1].color != self.color:
                    tiles_to_be_selected.append(tile_to_check)
                break
            else:
                tiles_to_be_selected.append(tile_to_check)
        for x in range(1, 8):
            if self_tile_x - x < 0:
                break
            tile_to_check = board.tiles[self_tile_x - x][self_tile_y]
            result = tile_to_check.has_piece(pieces)
            if result[0]:
                if result[1].color != self.color:
                    tiles_to_be_selected.append(tile_to_check)
                break
            else:
                tiles_to_be_selected.append(tile_to_check)
        for x in range(1, 8):
            if self_tile_x + x > 7:
                break
            tile_to_check = board.tiles[self_tile_x + x][self_tile_y]
            result = tile_to_check.has_piece(pieces)
            if result[0]:
                if result[1].color != self.color:
                    tiles_to_be_selected.append(tile_to_check)
                break
            else:
                tiles_to_be_selected.append(tile_to_check)    
        for x in range(1, 8):
                y = x
                if self_tile_y - y < 0 or self_tile_x - x < 0:
                    break
                tile_to_check = board.tiles[self_tile_x - x][self_tile_y - y]
                result = tile_to_check.has_piece(pieces)
                if result[0]:
                    if result[1].color != self.color:
                        tiles_to_be_selected.append(tile_to_check)
                    break
                else:
                    tiles_to_be_selected.append(tile_to_check)
        for x in range(1, 8):
                y = x
                if self_tile_y + y > 7 or self_tile_x - x < 0:
                    break
                tile_to_check = board.tiles[self_tile_x - x][self_tile_y + y]
                result = tile_to_check.has_piece(pieces)
                if result[0]:
                    if result[1].color != self.color:
                        tiles_to_be_selected.append(tile_to_check)
                    break
                else:
                    tiles_to_be_selected.append(tile_to_check)
        for x in range(1, 8):
                y = x
                if self_tile_y - y < 0 or self_tile_x + x > 7:
                    break
                tile_to_check = board.tiles[self_tile_x + x][self_tile_y - y]
                result = tile_to_check.has_piece(pieces)
                if result[0]:
                    if result[1].color != self.color:
                        tiles_to_be_selected.append(tile_to_check)
                    break
                else:
                    tiles_to_be_selected.append(tile_to_check)
        for x in range(1, 8):
                y = x
                if self_tile_y + y > 7 or self_tile_x + x > 7:
                    break
                tile_to_check = board.tiles[self_tile_x + x][self_tile_y + y]
                result = tile_to_check.has_piece(pieces)
                if result[0]:
                    if result[1].color != self.color:
                        tiles_to_be_selected.append(tile_to_check)
                    break
                else:
                    tiles_to_be_selected.append(tile_to_check)

        return tiles_to_be_selected

class King(Piece):
    def __init__(self, width, height, x, y, image_path, color):
        super().__init__(width, height, x, y, image_path, color)
        self.type = "king"

    def if_selected(self, tiles, pieces, board):
        tiles_to_be_selected = []
        self_tile = self.on_tile(tiles)

        for tile_list in board.tiles:
            if self_tile in tile_list:
                self_tile_x = board.tiles.index(tile_list)
                self_tile_y = tile_list.index(self_tile)
        
        y = 1
        if not self_tile_y - y < 0:
            tile_to_check = board.tiles[self_tile_x][self_tile_y - y]
            result = tile_to_check.has_piece(pieces)
            if result[0]:
                 if result[1].color != self.color:
                    tiles_to_be_selected.append(tile_to_check)
            else:
                tiles_to_be_selected.append(tile_to_check)
        y = 1
        if not self_tile_y + y > 7:
            tile_to_check = board.tiles[self_tile_x][self_tile_y + y]
            result = tile_to_check.has_piece(pieces)
            if result[0]:
                 if result[1].color != self.color:
                    tiles_to_be_selected.append(tile_to_check)
            else:
                tiles_to_be_selected.append(tile_to_check)
        x = 1
        if not self_tile_x - x < 0:
            tile_to_check = board.tiles[self_tile_x - x][self_tile_y]
            result = tile_to_check.has_piece(pieces)
            if result[0]:
                 if result[1].color != self.color:
                    tiles_to_be_selected.append(tile_to_check)
            else:
                tiles_to_be_selected.append(tile_to_check)
        x = 1
        if not self_tile_x + x > 7:
            tile_to_check = board.tiles[self_tile_x + x][self_tile_y]
            result = tile_to_check.has_piece(pieces)
            if result[0]:
                 if result[1].color != self.color:
                    tiles_to_be_selected.append(tile_to_check)
            else:
                tiles_to_be_selected.append(tile_to_check)
        y, x = 1, 1
        if not (self_tile_y - y < 0 or self_tile_x - x < 0):
            tile_to_check = board.tiles[self_tile_x - x][self_tile_y - y]
            result = tile_to_check.has_piece(pieces)
            if result[0]:
                 if result[1].color != self.color:
                    tiles_to_be_selected.append(tile_to_check)
            else:
                tiles_to_be_selected.append(tile_to_check)
        y, x = 1, 1
        if not (self_tile_y + y > 7 or self_tile_x - x < 0):
            tile_to_check = board.tiles[self_tile_x - x][self_tile_y + y]
            result = tile_to_check.has_piece(pieces)
            if result[0]:
                 if result[1].color != self.color:
                    tiles_to_be_selected.append(tile_to_check)
            else:
                tiles_to_be_selected.append(tile_to_check)
        y, x = 1, 1
        if not (self_tile_y - y < 0 or self_tile_x + x > 7):
            tile_to_check = board.tiles[self_tile_x + x][self_tile_y - y]
            result = tile_to_check.has_piece(pieces)
            if result[0]:
                 if result[1].color != self.color:
                    tiles_to_be_selected.append(tile_to_check)
            else:
                tiles_to_be_selected.append(tile_to_check)
        y, x = 1, 1
        if not (self_tile_y + y > 7 or self_tile_x + x > 7):
            tile_to_check = board.tiles[self_tile_x + x][self_tile_y + y]
            result = tile_to_check.has_piece(pieces)
            if result[0]:
                 if result[1].color != self.color:
                    tiles_to_be_selected.append(tile_to_check)
            else:
                tiles_to_be_selected.append(tile_to_check)
        return tiles_to_be_selected

class Pawn(Piece):
    def __init__(self, width, height, x, y, image_path, color):
        super().__init__(width, height, x, y, image_path, color)
        self.type = "pawn"
    
    def if_selected(self, tiles, pieces, board):
        tiles_to_be_selected = []
        self_tile = self.on_tile(tiles)

        for tile_list in board.tiles:
            if self_tile in tile_list:
                self_tile_x = board.tiles.index(tile_list)
                self_tile_y = tile_list.index(self_tile)
        
        if self.color == (255, 255, 255):
            if not self_tile_y - 1 < 0:
                tile_to_check = board.tiles[self_tile_x][self_tile_y - 1]
                result = tile_to_check.has_piece(pieces)
                if not result[0]:
                    tiles_to_be_selected.append(tile_to_check)
            if not (self_tile_y - 1 < 0 or self_tile_x - 1 < 0):
                tile_to_check = board.tiles[self_tile_x - 1][self_tile_y - 1]
                result = tile_to_check.has_piece(pieces)
                if result[0] and result[1].color != self.color:
                        tiles_to_be_selected.append(tile_to_check)
            if not (self_tile_y - 1 < 0 or self_tile_x + 1 > 7):
                tile_to_check = board.tiles[self_tile_x + 1][self_tile_y - 1]
                result = tile_to_check.has_piece(pieces)
                if result[0] and result[1].color != self.color:
                        tiles_to_be_selected.append(tile_to_check)
        if self.color == (0, 0, 0):
            if not self_tile_y + 1 > 7:
                tile_to_check = board.tiles[self_tile_x][self_tile_y + 1]
                result = tile_to_check.has_piece(pieces)
                if not result[0]:
                    tiles_to_be_selected.append(tile_to_check)
            if not (self_tile_y + 1 < 0 or self_tile_x - 1 < 0):
                tile_to_check = board.tiles[self_tile_x - 1][self_tile_y + 1]
                result = tile_to_check.has_piece(pieces)
                if result[0] and result[1].color != self.color:
                        tiles_to_be_selected.append(tile_to_check)
            if not (self_tile_y + 1 < 0 or self_tile_x + 1 > 7):
                tile_to_check = board.tiles[self_tile_x + 1][self_tile_y + 1]
                result = tile_to_check.has_piece(pieces)
                if result[0] and result[1].color != self.color:
                        tiles_to_be_selected.append(tile_to_check)

        return tiles_to_be_selected

class Piece_Set():
    def __init__(self):
        self.pieces = []

    def create_pieces(self, width, height, color_tuple, color_name, board, player):
        if player == 1:
            for i in range(8):
                pawn = Pawn(width, height,
                            board.tiles[6][i].pos[0], board.tiles[6][i].pos[1],
                            "Assets" + os.sep + color_name + os.sep + "pawn.png", color_tuple)
                self.pieces.append(pawn)
            
            self.pieces.append(Rook(width, height,
                                    board.tiles[7][0].pos[0], board.tiles[7][0].pos[1],
                                    "Assets" + os.sep + color_name + os.sep + "rook.png", color_tuple))
            
            self.pieces.append(Horse(width, height,
                                    board.tiles[7][1].pos[0], board.tiles[7][1].pos[1],
                                    "Assets" + os.sep + color_name + os.sep + "horse.png", color_tuple))
            
            self.pieces.append(Bishop(width, height,
                                    board.tiles[7][2].pos[0], board.tiles[7][2].pos[1],
                                    "Assets" + os.sep + color_name + os.sep + "bishop.png", color_tuple))
            
            self.pieces.append(Queen(width, height,
                                    board.tiles[7][3].pos[0], board.tiles[7][3].pos[1],
                                    "Assets" + os.sep + color_name + os.sep + "queen.png", color_tuple))
            
            self.pieces.append(King(width, height,
                                    board.tiles[7][4].pos[0], board.tiles[7][4].pos[1],
                                    "Assets" + os.sep + color_name + os.sep + "king.png", color_tuple))
            
            self.pieces.append(Bishop(width, height,
                                    board.tiles[7][5].pos[0], board.tiles[7][5].pos[1],
                                    "Assets" + os.sep + color_name + os.sep + "bishop.png", color_tuple))
            
            self.pieces.append(Horse(width, height,
                                    board.tiles[7][6].pos[0], board.tiles[7][6].pos[1],
                                    "Assets" + os.sep + color_name + os.sep + "horse.png", color_tuple))
            
            self.pieces.append(Rook(width, height,
                                    board.tiles[7][7].pos[0], board.tiles[7][7].pos[1],
                                    "Assets" + os.sep + color_name + os.sep + "rook.png", color_tuple))
        if player == 2:
            for i in range(8):
                pawn = Pawn(width, height,
                            board.tiles[1][i].pos[0], board.tiles[1][i].pos[1],
                            "Assets" + os.sep + color_name + os.sep + "pawn.png", color_tuple)
                self.pieces.append(pawn)
            
            self.pieces.append(Rook(width, height,
                                    board.tiles[0][0].pos[0], board.tiles[0][0].pos[1],
                                    "Assets" + os.sep + color_name + os.sep + "rook.png", color_tuple))
            
            self.pieces.append(Horse(width, height,
                                    board.tiles[0][1].pos[0], board.tiles[0][1].pos[1],
                                    "Assets" + os.sep + color_name + os.sep + "horse.png", color_tuple))
            
            self.pieces.append(Bishop(width, height,
                                    board.tiles[0][2].pos[0], board.tiles[0][2].pos[1],
                                    "Assets" + os.sep + color_name + os.sep + "bishop.png", color_tuple))
            
            self.pieces.append(Queen(width, height,
                                    board.tiles[0][4].pos[0], board.tiles[0][4].pos[1],
                                    "Assets" + os.sep + color_name + os.sep + "queen.png", color_tuple))
            
            self.pieces.append(King(width, height,
                                    board.tiles[0][3].pos[0], board.tiles[0][3].pos[1],
                                    "Assets" + os.sep + color_name + os.sep + "king.png", color_tuple))
            
            self.pieces.append(Bishop(width, height,
                                    board.tiles[0][5].pos[0], board.tiles[0][5].pos[1],
                                    "Assets" + os.sep + color_name + os.sep + "bishop.png", color_tuple))
            
            self.pieces.append(Horse(width, height,
                                    board.tiles[0][6].pos[0], board.tiles[0][6].pos[1],
                                    "Assets" + os.sep + color_name + os.sep + "horse.png", color_tuple))
            
            self.pieces.append(Rook(width, height,
                                    board.tiles[0][7].pos[0], board.tiles[0][7].pos[1],
                                    "Assets" + os.sep + color_name + os.sep + "rook.png", color_tuple))
    
    def display(self, window):
        for piece in self.pieces:
            window.blit(piece.sprite, piece.rect)
