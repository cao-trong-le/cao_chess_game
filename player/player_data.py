import pygame
from objects import (Object, MovingObject)

from game_screen.screen_object import WIDTH, HEIGHT
import copy

player_data = {
    "id": "BG_123",
    "player": True,
    "name": None,
    "width": 50,
    "height": 50,
    "pos_x": WIDTH // 2 - 50 // 2,
    "pos_y": HEIGHT - 100, 
    "source": "player/images",
    "image": ["blue_spaceship.png"],
    "velocity": 5,
    "rotate": 0,
    "firing_direction": (0, -1),
    "bullet_lines": 1,
    "bullet_num": 0,
    "max_health": 100,
    "cur_health": 100,
    "control_keys": {
        "up": pygame.K_w,
        "down": pygame.K_s,
        "left": pygame.K_a,
        "right": pygame.K_d,
        "fire": pygame.K_k,
        "slow_down": pygame.K_SPACE,
        "item_1": pygame.K_j,
        "item_2": pygame.K_l,
        "item_3": pygame.K_i,
        "pause": pygame.K_p,
    },
    "owner": None
}











