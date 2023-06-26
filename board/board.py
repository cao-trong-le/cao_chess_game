from objects import pygame, os, random, MovingObject, Object
from game_screen.screen_object import WIN, WIDTH, HEIGHT
import copy
from mouse_cursor.mouse_object import MouseObject
from mouse_cursor.mouse_data import mouse_data
from helper.__function_tracker import run_once
from chess_piece.chess_piece_data import _chess_pieces_dict
from chess_piece.chess_piece import (
    ChessPieceObject,
    Pawn,
    King,
    Queen,
    Rock,
    Knight,
    Bishop
)


class BoardObject(Object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.pos_x = 0
        self.pos_y = 0
        # self.rect.x = 0
        # self.rect.y = 0
        self.width_grids = 8
        self.height_grids = 8
        self.grids = []
        self.tiles_group = pygame.sprite.Group()
        
        # chess pieces positions
      
        self.chess_pieces_group = pygame.sprite.Group()
        self.set_chess_pieces = 2
        
        self.players = None
        
        self.chess_piece_objects = {
            "p": Pawn,
            "k": King,
            "q": Queen,
            "r": Rock,
            "kn": Knight,
            "b": Bishop
        }
        
        self.set_test_pawn_promotion = False
            
    def generate_board(self):
        for x in range(self.width_grids):
            self.grids.append([])
            
            for y in range(self.height_grids):
                grid = TileObject()
                
                if x % 2:
                    if not y % 2:
                        grid.image = ["b_piece.png"]
                        grid.image_changed = True
                    else:
                        grid.image = ["w_piece.png"]
                        grid.image_changed = True
                
                elif not x % 2:
                    if not y % 2:
                        grid.image = ["w_piece.png"]
                        grid.image_changed = True
                    else:
                        grid.image = ["b_piece.png"]
                        grid.image_changed = True
                
                grid.pos_x = x * grid.width
                grid.pos_y = y * grid.height
                grid.board = self
                grid.players = self.players
                grid.chess_pieces = self.chess_pieces_group
                grid.coor = (x, y)
                
                self.tiles_group.add(grid)
                self.grids[x].append((x, y))
                

    def test_pawn_promotion(self, player):
        if not self.set_test_pawn_promotion:
            state = [
                ["", "", "", "", "", "", "", ""],
                ["", "", "", "", "b_p", "", "", ""],
                ["", "", "", "", "", "", "", ""],
                ["", "", "", "", "", "", "", ""],
                ["", "", "", "", "", "", "", ""],
                ["", "", "", "", "", "", "", ""],
                ["", "", "", "", "w_p", "", "", ""],
                ["", "", "", "", "", "", "", ""]
            ]
            
            for _ in range(len(state)):
                state[_] = list(zip(state[_], self.grids[_]))
                
            
            if self.set_chess_pieces > 0: 
                self.set_chess_pieces -= 1
                 
                for index, value in enumerate(state):
                    for index, val in enumerate(value):
                        if val[0] != "":
                            # create chess piece
                            grid_coor = val[1]
                            
                            # get_chess_piece_pos
                            pos_x, pos_y = grid_coor[1] * 40, grid_coor[0] * 40
                            
                            # find chess piece
                            piece_alias = val[0]
                            
                            piece_object = self.chess_piece_objects.get(piece_alias.split("_")[1])
                                        
                            chess_piece = piece_object({**_chess_pieces_dict.get(piece_alias)})
                            chess_piece.pos_x = pos_x
                            chess_piece.pos_y = pos_y
                            chess_piece.piece_coor = (grid_coor[0], grid_coor[1])
                            chess_piece.rotate = 0
                            chess_piece.board = self
                            chess_piece.player = player
                            chess_piece.side = player.side
                            
                            self.chess_pieces_group.add(chess_piece)
                    
                # print((self.chess_pieces_group.sprites()))

        
        self.set_test_pawn_promotion = True
                
    # @run_once
    def place_chess_pieces(self, player):
        # get chess pieces coor
        if self.set_chess_pieces > 0:
            side_board = None
        
            if player.first_turn:    
                side_board = self.grids[6] + self.grids[7]
            else:
                side_board = self.grids[0] + self.grids[1]
                
                
            for index, value in enumerate(side_board):
                # create chess piece
                
                # get_chess_piece_pos
                pos_x, pos_y = value[0] * 40, value[1] * 40
                
                # find chess piece
                piece_alias = player.chess_pieces_order[index]
                
                piece_object = self.chess_piece_objects.get(piece_alias.split("_")[1])
                               
                chess_piece = piece_object({**_chess_pieces_dict.get(piece_alias)})
                chess_piece.pos_x = pos_y
                chess_piece.pos_y = pos_x
                chess_piece.piece_coor = (value[0], value[1])
                chess_piece.rotate = 0
                chess_piece.board = self
                chess_piece.player = player
                chess_piece.side = player.side
                
                self.chess_pieces_group.add(chess_piece)
                
            # print((self.chess_pieces_group.sprites()))
            self.set_chess_pieces -= 1
            
        
    def render_board(self):
        self.tiles_group.update()
        self.chess_pieces_group.update()
               
    def update(self): 
        self.render_board()
        
        
class TileObject(Object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.pos_x = 0
        self.pos_y = 0
        # self.rect.x = 0
        # self.rect.y = 0
        self.height = 40
        self.width = 40
        self.source = "board/images"
        self.image = ["blank_tile.png"]
        self.image_changed = True
        
        self.coor = (0, 0)
        
        self.board = None
        self.players = None
        self.chess_pieces = None
        
        self.hitbox_color = (200, 100, 100)
        self.display_hitbox = False

        self.clicked = False

    def on_click(self):
        left_click = pygame.mouse.get_pressed(3)[0]
        mouse_pos = pygame.mouse.get_pos()
        _player = None
        move = False
  
        if self.board.players:
            for player in self.board.players.sprites():
                if player.first_turn:
                    _player = player
            
        if left_click and self.rect.collidepoint(mouse_pos) and not move and not self.clicked:
            # print("on click")
            self.clicked = True
            
            if _player.selected_piece and _player.selected_piece.selected:
                self.refresh_tiles()
                self.display_hitbox = True
                
                if (self.coor[1], self.coor[0]) in _player.selected_piece.attack_movements:
                    attack_target = self.has_attack_target()
                
                    if attack_target:
                        attack_target.kill()
                        self.move_chess_piece(_player)
                        
       
                elif (self.coor[1], self.coor[0]) in _player.selected_piece.predicted_movements:
                    # print(len(self.board.chess_pieces_group.sprites()))
                    piece = _player.selected_piece
                    
                    if piece.piece == "king" and piece.can_castle:
                        king = piece
                        selected_rock = None

                        self.castle_the_king(_player, king, selected_rock)
                                           
                    else:
                        self.move_chess_piece(_player)
                    
                    
                # swap turn with other player

        if not left_click:
            self.clicked = False
            
    def castle_the_king(self, player, king, selected_rock):
        for rock in king.target_rocks:
            if rock.piece_coor == (self.coor[1], self.coor[0]):
                selected_rock = rock
        
        if king.pos_x < selected_rock.pos_x:
            king.piece_coor = (king.piece_coor[0], king.piece_coor[1] + 2)
            king.pos_x = king.piece_coor[1] * 40
            
            selected_rock.piece_coor = (king.piece_coor[0], king.piece_coor[1] - 1)
            selected_rock.pos_x = selected_rock.piece_coor[1] * 40
            
        else:
            king.piece_coor = (king.piece_coor[0], king.piece_coor[1] - 2)
            king.pos_x = king.piece_coor[1] * 40
            
            selected_rock.piece_coor = (king.piece_coor[0], king.piece_coor[1] + 1)
            selected_rock.pos_x = selected_rock.piece_coor[1] * 40
            
            
        player.selected_piece.first_move = False
        player.selected_piece.selected = False
        player.selected_piece.can_castle = False
        player.selected_piece.target_rocks = []
        player.selected_piece.predicted_movements.clear()
        player.selected_piece.attack_movements.clear()
        
        self.swap_turn()
            
                
    def move_chess_piece(self, player):
        player.selected_piece.piece_coor = (self.coor[1], self.coor[0])
        player.selected_piece.pos_x = self.coor[0] * 40
        player.selected_piece.pos_y = self.coor[1] * 40
        
        if player.selected_piece.piece in set(["pawn", "king", "rock"]):
            player.selected_piece.first_move = False
        
        # print(player.in_promotion)
        
        player.selected_piece.selected = False
        player.selected_piece.predicted_movements.clear()
        player.selected_piece.attack_movements.clear()
        
        
        
        self.swap_turn()
                
        
    def has_attack_target(self):
        for piece in self.board.chess_pieces_group.sprites():
            if piece.piece_coor == (self.coor[1], self.coor[0]):
                return piece
        return None
                    
    def swap_turn(self):
        for player in self.board.players.sprites():
            if player.first_turn:
                player.first_turn = False
            else:
                player.first_turn = True
    
            
    def refresh_tiles(self):
        for tile in self.board.tiles_group.sprites():
            tile.display_hitbox = False
            
        
    def update(self):
        self.handle_image()
        self.rendering_object()
        self.on_click()  
        
        if self.display_hitbox:
            self.hitbox()
            
        self.update_positions()
        

        
                    
        