from objects import pygame, os, random, MovingObject, Object
from game_screen.screen_object import WIN, WIDTH, HEIGHT
import copy
from mouse_cursor.mouse_object import MouseObject
from mouse_cursor.mouse_data import mouse_data
from helper.__function_tracker import run_once
from game_screen.text import Text
from game_screen.button_object import Button

from button.button_object import Button as _Button


class GameStateObject(Object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.board = None
        self.timer = None
        self.player_groups = pygame.sprite.Group()
        
        self.color_picked = False
        self.first_picked_color = None
        self.second_picked_color = None
        
        self.place_pieces = False
        
        # self.global_data = {
        #     "board": self.board,
        #     "timer": self.timer,
        #     "player_groups": self.player_groups
        # }
        
        self.set_turn = False
        
        self.set_color = False
        self.set_color_button_group = pygame.sprite.Group()
        
        
        self.set_board = False
        self.set_players = False
        
        self.test = False
        
        self.current_player = None
        
        self.kings = None
        self.kings_gathered = False
        
        self.winner = None
        
        # game layers
        self.second_layer = pygame.sprite.Group()
        
    def generate_player(self):
        from player.player_object import PlayerObject

        if not self.set_players:
            for _ in range(2):
                player = PlayerObject()
                player.player_name = f"Player {(_ + 1)}"
                player.is_test = self.test
                player.game_state = self
                self.player_groups.add(player)
                
            self.set_players = True
            
    
    def pick_color_tab(self):
        # draw background
        if not self.color_picked:
            pick_color_div = pygame.Rect(20, 20, 280, 280)
            pygame.draw.rect(self.window, (0, 0, 0), pick_color_div, 1)

            # draw button 
            black_button = Button(
                text="Black", 
                size=20, 
                pos_x=40, 
                color=(255, 255, 255),
                background=(0, 0, 0),
                pos_y=(280 / 2 - 40 / 2),
                height=40, 
                width=100,
                surface=self.window
            )
            
            black_button.draw_button()
            
            if black_button.button_on_click_no_event():
                self.first_picked_color = "black"
                self.second_picked_color = "white"
                
                self.color_picked = True
            
            white_button = Button(
                text="White", 
                size=20, 
                pos_x=180, 
                color=(0, 0, 0),
                background=(255, 255, 255),
                pos_y=(280 / 2 - 40 / 2),
                height=40, 
                width=100,
                surface=self.window
            )
            
            white_button.draw_button()
            
            if white_button.button_on_click_no_event():
                self.first_picked_color = "white"
                self.second_picked_color = "black"
                
                self.color_picked = True
              
    def set_color_for_chess_piece(self):
        if not self.set_color:
            for player in self.player_groups.sprites():
                if player.first_turn:
                    player.piece_color = self.first_picked_color 
                    
                    if player.piece_color == "black":
                        player.chess_pieces_order = ["b_p"] * 8 + ["b_r", "b_kn", "b_b", "b_k", "b_q", "b_b", "b_kn", "b_r"]
                    else:
                        player.chess_pieces_order = ["w_p"] * 8 + ["w_r", "w_kn", "w_b", "w_q", "w_k", "w_b", "w_kn", "w_r"]
                else:
                    player.piece_color = self.second_picked_color

                    if player.piece_color == "black":
                        player.chess_pieces_order = ["b_r", "b_kn", "b_b", "b_q", "b_k", "b_b", "b_kn", "b_r"] + ["b_p"] * 8
                    else:
                        player.chess_pieces_order = ["w_r", "w_kn", "w_b", "w_k", "w_q", "w_b", "w_kn", "w_r"] + ["w_p"] * 8

            self.set_color = True
    
    
    def random_turns(self):
        if not self.set_turn:
            self.set_turn = True
            players = self.player_groups.sprites()
            
            for _ in range(len(players)):
                if _ == 0:
                    players[_].first_turn = True
                    self.current_player = players[_]
                else:
                    players[_].first_turn = False
                    
                players[_].side = "lower" if players[_].first_turn else "upper"
                    
   
    def generate_board(self):
        from board.board import BoardObject
        
        if not self.set_board:
            self.board = BoardObject()
            self.board.generate_board()
            self.board.players = self.player_groups
            self.set_board = True
        
    def congrat_winner(self):
        if self.winner:
            congrat_text = Text(
                width = 200,
                height = 40,
                size = 25,
                pos_x = self.window.get_width() // 2 - 200 // 2,
                pos_y = self.window.get_height() // 2 - 40 // 2,
                surface = self.window
            )
                 
            pygame.draw.rect(
                self.window,
                (123, 32, 12),
                pygame.Rect(
                    self.window.get_width() // 2 - 200 // 2,
                    self.window.get_height() // 2 - 40 // 2,
                    200,
                    40
                )
            )
            
            congrat_text.text = f"Player {self.winner.piece_color.capitalize()} Won!"
            congrat_text.display_text()   
                
    
    def place_chess_pieces(self):
        if not self.place_pieces:
            self.place_pieces = True
            
            for player in self.player_groups.sprites():
                if not self.test:
                    player.place_chess_pieces(self.board)
                else:
                    self.board.test_pawn_promotion(player)
                    
    def check_kings(self):
        kings = [piece for piece in self.board.chess_pieces_group.sprites() if piece.piece == "king"]

        if len(kings) < 2:
            self.winner = kings[0].player
            
        self.congrat_winner()
                
    def update(self): 
        self.generate_player()
        self.random_turns()
        self.pick_color_tab()
            
        if self.color_picked:
            self.set_color_for_chess_piece()
            
            self.generate_board()
            
            if self.board and not any([player.win for player in self.player_groups.sprites()]):
                self.board.update()
            
            self.place_chess_pieces()
            
            self.check_kings()
            
        # if self.current_player.in_promotion: 
        #     self.promotion_popup.update()
                
        self.second_layer.update()        
        self.player_groups.update()
        
        

        
                    
        