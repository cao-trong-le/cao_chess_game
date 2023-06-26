from objects import pygame, os, random, MovingObject, Object
from game_screen.screen_object import WIN, WIDTH, HEIGHT
import copy
from mouse_cursor.mouse_object import MouseObject
from mouse_cursor.mouse_data import mouse_data
from helper.__function_tracker import run_once

class PlayerObject(Object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.player_name = ""
        self.first_turn = False
        self.side = "upper"
        self.mouse = MouseObject({**mouse_data})
        self.source = "player/images"
        self.piece = None
        self.piece_image = []
        self.win = False
        self.piece_color = "black"
        self.chess_pieces = None
        self.chess_pieces_order = []
        self.selected_piece = None
        
        self.is_test = False
        
        self.in_promotion = False
        
        self.game_state = None
     
    def update_mouse(self):
        if self.first_turn:
            self.mouse.update()
        
    # @run_once
    def place_chess_pieces(self, board):
        board.place_chess_pieces(self)
        
    def calculate_shortest_path(self):
        pass
        
    # moving characters
    def moving_object(self):
        # get mouse position
        mouse_coor = pygame.mouse.get_pos()
         
        pass
 

    def print_outline(self):
        while True:
            print(self.outline)
            break
               
    def update(self): 
        self.update_mouse()
        # self.update_positions()
        
    
            
            

        
                    
        