from objects import Object
import pygame

from button.button_object import Button
from popup.popup_object import PromotionPopup

class ChessPieceObject(Object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.source = "chess_piece/images"
        self.piece = None
        self.piece_image = []
        self.image_changed = False
        self.win = False
        self.selected = False
        self.width = 40
        self.height = 40
        self.rotate = 0
        self.side = "upper"
        self.piece_coor = (0, 0)
        self.predicted_movements = set([])
        self.attack_movements = set([])
        self.board = None
        self.player = None
        self.chess_pieces = None
        self.predict_movements = False
        
        self.clicked = False
        
        
    def select_chess_piece(self):
        # highlight the selected chess piece and predict its movements
        left_click = pygame.mouse.get_pressed(3)[0]
        mouse_pos = pygame.mouse.get_pos()
        
        if (left_click and 
            self.rect.collidepoint(mouse_pos) and 
            self.player.first_turn and 
            not self.clicked):
            
            self.clicked = True
            self.reset_piece()
            self.selected = True
            
            self.predict_movements = True
            
            # player = self.find_player()
            self.player.selected_piece = self
            
            self.predict_piece_movements()
            
        if not left_click:
            self.clicked = False
            
            
    # def find_player(self):
    #     for player in self.players.sprites():
    #         if player.first_turn:
    #             return player
    
    def reset_piece(self):
        if self.player.selected_piece:
            self.player.selected_piece.selected = False
            
    def get_king(self):
        for piece in self.board.chess_pieces_group.sprites():
            if piece.piece == "king" and self.player.side == piece.side:
                return piece
            
    def check_checkmate(self):
        king = self.get_king()
        
        if king is not None:
            if king.piece_coor in self.attack_movements:
                king.is_check = True
                king.check_pos.add(self.piece_coor)  
            king.is_check = False
            
    def check_boundary(self, x, y, is_move):
        if ((0 <= x <= 7) and (0 <= y <= 7)):
            
            if is_move:
                if (x, y) in set([piece.piece_coor for piece in self.board.chess_pieces_group.sprites()]):
                    return False
                else:
                    return True
                
            else:
                if (x, y) in set([piece.piece_coor if piece.side != self.player.side else None for piece in self.board.chess_pieces_group.sprites()]):
                    return True
                else:
                    return False

        return False
            
    def predict_piece_movements(self):
        return 
    
    def update(self):
        self.handle_image()
        self.rendering_object()
        self.select_chess_piece()
        
        if self.selected:
            self.object_mask_outline()
            
        # self.highlight_predicted_movements()
        
        if not self.player.is_test:
            self.check_checkmate()
            
        self.update_positions()
        
                           
class King(ChessPieceObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.piece = "king"
        self.is_check = False
        self.check_pos = set()
        self.first_move = True
        self.encounters = set()
        self.can_castle = False
        
        self.target_rocks = []
        
    def checkmate(self):
        return
    
    def select_chess_piece(self):
        left_click = pygame.mouse.get_pressed(3)[0]
        mouse_pos = pygame.mouse.get_pos()
        
        if (left_click and 
            self.rect.collidepoint(mouse_pos) and 
            self.player.first_turn and 
            not self.selected):
            
            self.reset_piece()
            self.selected = True
            
            self.conditions_castle_the_king()
    
            if self.can_castle:
                print(self.target_rocks)
                print("we can castle the king now")
            
            self.predict_movements = True
            
            # player = self.find_player()
            self.player.selected_piece = self
            
            self.predict_piece_movements()
    
    def conditions_castle_the_king(self):
        # no obstacles between king and rocks
        # conditions: king first move, no obstacle, no checkmate, rock first move
        conditions = [False, False, False, False]
        
        # check king first move
        if self.first_move:
            conditions[0] = True
            
        # is under check
        if self.piece_coor not in self.check_pos:
            conditions[2] = True
        
        # get rock pos
        rocks = set([piece if (piece.piece == "rock" and self.player.side == piece.side) else None for piece in self.board.chess_pieces_group.sprites()])
        
        check_directions = [
            [1, True, (0, -1)], 
            [1, True, (0, 1)]
        ]
        
        def check_encounters(direction, coor):
            # first check if any other ally pieces on the way if they are then return False
            
            if coor in set([piece.piece_coor if piece.side == self.player.side else None for piece in self.board.chess_pieces_group.sprites()]):
                self.encounters.add(coor) 
                direction[1] = False
                return
            
            if not ((0 <= coor[0] <= 7) and (0 <= coor[1] <= 7)):
                direction[1] = False
        
        for direction in check_directions:
            # check move 
            while direction[1]:
                move_coor = (
                    self.piece_coor[0] + direction[0] * direction[-1][0], 
                    self.piece_coor[1] + direction[0] * direction[-1][1]
                )

                check_encounters(direction, move_coor)
                direction[0] += 1
        
        # print(f"Encounters: {self.encounters}")
        
        self.target_rocks = []
         
        for rock in rocks:
            if rock and rock.piece_coor in self.encounters:
                self.target_rocks.append(rock)
                self.predicted_movements.add(rock.piece_coor)
                conditions[1] = True

        # print(f"Target Rocks: {self.target_rocks}")
                
        conditions[3] = any([piece.first_move if piece.side == self.player.side else None for piece in self.target_rocks])
        
        # the rocks and the king both have to be their first turn
        # the king is not under check 
        
        print(conditions)
        
        self.can_castle = all(conditions)
        
        
        
    def predict_piece_movements(self):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for x, y in directions:
            move_coor = (self.piece_coor[0] + x, self.piece_coor[1] + y)
            
            if self.check_boundary(move_coor[0], move_coor[1], True):
                self.predicted_movements.add(move_coor) 
                
            if self.check_boundary(move_coor[0], move_coor[1], False):
                self.attack_movements.add(move_coor)
                
        # print(self.predicted_movements)
        # print(self.attack_movements)
        
    def update(self):
        super().update()
                             
class Queen(ChessPieceObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        
    def predict_piece_movements(self):
        print("queen")  
        
        directions = [
            [1, True, 1, True, (1, 0)], 
            [1, True, 1, True, (-1, 0)], 
            [1, True, 1, True, (0, 1)], 
            [1, True, 1, True, (0, -1)], 
            [1, True, 1, True, (-1, -1)], 
            [1, True, 1, True, (-1, 1)], 
            [1, True, 1, True, (1, -1)], 
            [1, True, 1, True, (1, 1)]
        ]
        
        def check_queen_move_boundary(direction, coor):
            if self.check_boundary(coor[0], coor[1], True):
                self.predicted_movements.add(coor) 
            else:
                direction[1] = False
                
        def check_queen_attack_boundary(direction, coor):
            # first check if any other ally pieces on the way if they are then return False
            if coor in set([piece.piece_coor if piece.side == self.player.side else None for piece in self.board.chess_pieces_group.sprites()]):
                direction[3] = False
                return
            
            if ((0 <= coor[0] <= 7) and (0 <= coor[1] <= 7)):
                if self.check_boundary(coor[0], coor[1], False):
                    self.attack_movements.add(coor) 
                    direction[3] = False
            else:
                direction[3] = False
        
        for direction in directions:
            # check move 
            while direction[1]:
                move_coor = (
                    self.piece_coor[0] + direction[0] * direction[-1][0], 
                    self.piece_coor[1] + direction[0] * direction[-1][1]
                )

                check_queen_move_boundary(direction, move_coor)
                direction[0] += 1
                
            while direction[3]:
                move_coor = (
                    self.piece_coor[0] + direction[2] * direction[-1][0], 
                    self.piece_coor[1] + direction[2] * direction[-1][1]
                )

                check_queen_attack_boundary(direction, move_coor)
                direction[2] += 1
           
        print(self.predicted_movements)
        print(self.attack_movements)
                 
class Rock(ChessPieceObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.piece = "rock"
        self.first_move = True
        self.clicked = False
        
    def select_chess_piece(self):
        left_click = pygame.mouse.get_pressed(3)[0]
        mouse_pos = pygame.mouse.get_pos()
        
        if (left_click and 
            self.rect.collidepoint(mouse_pos) and 
            self.player.first_turn and 
            not self.selected and 
            not self.clicked):
            
            self.clicked = True
            
            # check if the prev selected piece is king and it is able to castle
            prev_selected_piece = self.player.selected_piece
            
            if (prev_selected_piece.piece == "king" and 
                prev_selected_piece.can_castle and
                self.piece_coor in [piece.piece_coor for piece in self.board.chess_pieces_group.sprites()]):
                self.selected = True

            else:
                self.reset_piece()
                
                self.selected = True
                self.predict_movements = True
                
                # player = self.find_player()
                self.player.selected_piece = self
                
                self.predict_piece_movements()
        
        if not left_click:
            self.clicked = False
        
    def predict_piece_movements(self):
        # [move_step, move, atk_step, attack, coor]
        directions = [
            [1, True, 1, True, (1, 0)], 
            [1, True, 1, True, (-1, 0)], 
            [1, True, 1, True, (0, 1)], 
            [1, True, 1, True, (0, -1)]
        ]
        
        def check_move_boundary(direction, coor):
            if self.check_boundary(coor[0], coor[1], True):
                self.predicted_movements.add(coor) 
            else:
                direction[1] = False
                
        def check_attack_boundary(direction, coor):
            # first check if any other ally pieces on the way if they are then return False
            if coor in set([piece.piece_coor if piece.side == self.player.side else None for piece in self.board.chess_pieces_group.sprites()]):
                direction[3] = False
                return
            
            if ((0 <= coor[0] <= 7) and (0 <= coor[1] <= 7)):
                if self.check_boundary(coor[0], coor[1], False):
                    self.attack_movements.add(coor) 
                    direction[3] = False
            else:
                direction[3] = False
        
        for direction in directions:
            # check move 
            while direction[1]:
                move_coor = (
                    self.piece_coor[0] + direction[0] * direction[-1][0], 
                    self.piece_coor[1] + direction[0] * direction[-1][1]
                )

                check_move_boundary(direction, move_coor)
                direction[0] += 1
                
            while direction[3]:
                move_coor = (
                    self.piece_coor[0] + direction[2] * direction[-1][0], 
                    self.piece_coor[1] + direction[2] * direction[-1][1]
                )

                check_attack_boundary(direction, move_coor)
                direction[2] += 1
                              
class Knight(ChessPieceObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        
    def predict_piece_movements(self):
        directions = [(2, 1), (2, -1), (-2, 1), (-2, -1), (-1, 2), (-1, -2), (1, 2), (1, -2)]
        
        for x, y in directions:
            move_coor = (self.piece_coor[0] + x, self.piece_coor[1] + y)
            
            if self.check_boundary(move_coor[0], move_coor[1], True):
                self.predicted_movements.add(move_coor) 
                
            if self.check_boundary(move_coor[0], move_coor[1], False):
                self.attack_movements.add(move_coor)
                
        print(self.predicted_movements)
        print(self.attack_movements)
                       
class Bishop(ChessPieceObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        
    def predict_piece_movements(self):
        directions = [
            [1, True, 1, True, (-1, -1)], 
            [1, True, 1, True, (-1, 1)], 
            [1, True, 1, True, (1, -1)], 
            [1, True, 1, True, (1, 1)]
        ]
        
        def check_bishop_move_boundary(direction, coor):
            if self.check_boundary(coor[0], coor[1], True):
                self.predicted_movements.add(coor) 
            else:
                direction[1] = False
                
        def check_bishop_attack_boundary(direction, coor):
            # first check if any other ally pieces on the way if they are then return False
            if coor in set([piece.piece_coor if piece.side == self.player.side else None for piece in self.board.chess_pieces_group.sprites()]):
                direction[3] = False
                return
            
            if ((0 <= coor[0] <= 7) and (0 <= coor[1] <= 7)):
                if self.check_boundary(coor[0], coor[1], False):
                    self.attack_movements.add(coor) 
                    direction[3] = False
            else:
                direction[3] = False
        
        for direction in directions:
            # check move 
            while direction[1]:
                move_coor = (
                    self.piece_coor[0] + direction[0] * direction[-1][0], 
                    self.piece_coor[1] + direction[0] * direction[-1][1]
                )

                check_bishop_move_boundary(direction, move_coor)
                direction[0] += 1
                
            while direction[3]:
                move_coor = (
                    self.piece_coor[0] + direction[2] * direction[-1][0], 
                    self.piece_coor[1] + direction[2] * direction[-1][1]
                )

                check_bishop_attack_boundary(direction, move_coor)
                direction[2] += 1
                
        print(self.predicted_movements)
        print(self.attack_movements)
            
class Pawn(ChessPieceObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.piece = "pawn"
        self.first_move = True
        self.predict_movements = False
        self.last_row = None
        self.set_last_row = False
        
        self.set_popup = False
        self.set_layer = False
        
        self.promotion_surface = pygame.surface.Surface((320, 320))
        self.promotion_surface.fill((0, 0, 0))
        
        self.clicked = False
        
    def get_last_row(self):
        if not self.set_last_row:
            self.last_row = set(self.board.grids[0] if self.player.side == "lower" else self.board.grids[-1])
            self.set_last_row = True
    
    def select_chess_piece(self):
        # highlight the selected chess piece and predict its movements
        left_click = pygame.mouse.get_pressed(3)[0]
        mouse_pos = pygame.mouse.get_pos()
        
        # print(self.player.first_turn)
        
        if (left_click and 
            self.rect.collidepoint(mouse_pos) and 
            self.player.first_turn and 
            not self.clicked):
            
            self.clicked = True
            self.reset_piece()
            self.selected = True

            self.predict_movements = True
        
            self.player.selected_piece = self
            
            self.predict_piece_movements()
            
        if not left_click:
            self.clicked = False
            
       
    def promotion_popup(self):
        # promotion div
        
        if self.piece_coor in self.last_row and not self.set_popup:
            self.set_popup = True
            self.player.in_promotion = True
        
        if self.set_popup and self.player.in_promotion and not self.set_layer:
            self.set_layer = True
            promotion_popup = PromotionPopup()
            promotion_popup.player = self.player
            promotion_popup.board = self.board
            promotion_popup.surface = self.window
            promotion_popup.opened = True
            self.player.game_state.second_layer.add(promotion_popup)
                
        
    def predict_piece_movements(self):
        # player = self.find_player()
        
        # if first move --> can move the pawn up to 2 grids upwards
        self.predicted_movements.clear()
        number_move = 0
        
        if self.first_move:
            number_move = 2
        else:
            number_move = 1
            
        attack_directions = [(1, -1), (1, 1)]
        
        if self.side == "upper":
            for _ in range(number_move):
                if self.check_boundary(self.piece_coor[0] + (_ + 1), self.piece_coor[1], True):
                    self.predicted_movements.add((self.piece_coor[0] + (_ + 1), self.piece_coor[1]))

            for x, y in attack_directions:
                if self.check_boundary(self.piece_coor[0] + x, self.piece_coor[1] + y, False): 
                    self.attack_movements.add((self.piece_coor[0] + x, self.piece_coor[1] + y))   
                
        else:
            for _ in range(number_move):
                if self.check_boundary(self.piece_coor[0] - (_ + 1), self.piece_coor[1], True):
                    self.predicted_movements.add((self.piece_coor[0] - (_ + 1), self.piece_coor[1]))

            for x, y in attack_directions:
                if self.check_boundary(self.piece_coor[0] - x, self.piece_coor[1] + y, False): 
                    self.attack_movements.add((self.piece_coor[0] - x, self.piece_coor[1] + y))   
            
                
        # print(self.predicted_movements)  
        
    def update(self):
        super().update()
        
        self.get_last_row()
        self.promotion_popup()
                    

    
    
        