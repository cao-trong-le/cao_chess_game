import pygame
import time
import copy
from game_screen.button_object import Button
from game_screen.text import Text
from helper.__function_tracker import run_once

# from main import player_group, bullet_group, enemy_group, bonus_group

WIDTH, HEIGHT = 320, 320
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Silly Game")


upper_bar = pygame.Rect(0, 0, WIDTH, 50)
game_window = pygame.Rect(0, 50, WIDTH, 600)
lower_bar = pygame.Rect(0, HEIGHT - 50, WIDTH, 50)


# divide the main window into 2 sections
# samples and main
sample_section = pygame.Surface((200, 500))
sample_section.fill((200, 123, 12))

design_section = pygame.Surface((500, 500))
design_section.fill((230, 123, 12))


# create a screen selection section

class GameScreen:
    # game setting
    def __init__(self):
        self.fps = 60
        self.volume = 0
        self.volume_on = True
        self.pause = False
        self.quit = False
        
        self.startover = False
        self.pressed_key = pygame.key.get_pressed
        
     
        # objects 
        self.clock = pygame.time.Clock()
        self.start_time = time.time()
        self.elapsed_time = 0
        
        # screen option
        
        self.screens = {
            "menu": False, 
            "gameover": False,
            "play": True,
            "maps": False,
            "settings": False,
            "exit": False,
            "design": False,
            "testing": False,
        }
        
        self.gamestate = None
     
        pygame.mouse.set_visible(False)
        
        from game_screen.buttons import pause_button, score_text
            
        pygame.draw.rect(WIN, (123, 34, 23), upper_bar)
        pause_button.draw_button()
        
        # draw score text
        score_text.display_text()
                
    def switch_mode(self):
        # set delete mode
        if pygame.key.get_pressed()[pygame.K_d]:
            self.map.map_mode = "delete"
            
        # set draw mode
        if pygame.key.get_pressed()[pygame.K_e]:
            self.map.map_mode = "draw"
            
        # set starting mode
        if pygame.key.get_pressed()[pygame.K_a]:
            self.map.map_mode = "start"
            if self.map.get_starting_point():
                self.map.get_starting_point().hitbox_color = (0, 0, 0)
                
        # set ending mode
        if pygame.key.get_pressed()[pygame.K_s]:
            self.map.map_mode = "end"
            if self.map.get_ending_point():
                self.map.get_ending_point().hitbox_color = (0, 0, 0)
    
    @run_once
    def set_gamestate(self):
        from game_state.game_state import GameStateObject
        
        self.gamestate = GameStateObject()
        
    def update_gamestate(self):
        if self.gamestate:
            self.gamestate.update()
        
        
    def game_background(self):
        WIN.fill((255, 255, 255))
    
    def gameover_screen(self):
        from game_screen.buttons import play_again_button
        
        if self.screens["gameover"]:
            WIN.fill((0, 233, 23))
            play_again_button.draw_button()
            
            # menu button
    
    def switcher(self, screen_name):
        for key in self.screens.keys():
            if self.screens[key]:
                self.screens[key] = False
            break
            
        self.screens[screen_name] = True
            
    def start_menu_screen(self):
        from game_screen.buttons import (
            play_button, 
            maps_button, 
            settings_button, 
            exit_button,
            hidden_screen_button,
        )
        
        if self.screens["menu"]:
            WIN.fill((0, 233, 23))
            
            # play button
            play_button.draw_button()
            
            # select maps button
            maps_button.draw_button()
            
            # exit button
            exit_button.draw_button()
            
            # testing button
            hidden_screen_button.draw_button()
            
            # settings button
            settings_button.draw_button()
            
   
    def quit_game(self):
        if ((self.pressed_key()[pygame.K_LALT] or self.pressed_key()[pygame.K_RALT]) and 
            self.pressed_key()[pygame.K_F4]):
            self.quit = True
            
        # elif self.pressed_key[pygame.K_p]:
        #     self.quit = True
            
    def event_handler(self):
        from game_screen.buttons import (
            play_again_button, 
            pause_button,
            play_button,
            maps_button,
            settings_button,
            exit_button,
            hidden_screen_button
        )
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
                
            if event.type == pygame.KEYDOWN:   
                if self.pressed_key()[pygame.K_p]:
                    self.freeze_screen()
                    self.quit_game()
                    
            if exit_button.button_on_click(event):
                self.quit_game()
                            
    def set_current_time(self):
        self.elapsed_time = int(time.time() - self.start_time) 
        

    def render_screen(self):
        while not self.quit:
            self.clock.tick(self.fps)
       
            self.event_handler()
            # self.set_current_time()
            
            # print(self.elapsed_time)
            
            if self.screens["menu"]:
                self.start_menu_screen()
            
            elif self.screens["gameover"]:
                self.gameover_screen()
                
            elif self.screens["testing"]:
                self.testing_screen()
            
            elif self.screens["play"]:
                self.game_background()
                self.switch_mode()
                self.set_gamestate()
                self.update_gamestate()

                
            pygame.display.update()
                
        pygame.quit()

        

        