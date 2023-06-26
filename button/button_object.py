import pygame
from objects import Object

class Button(Object):
    def __init__(
        self, 
        *args,
        text: str = "", 
        size: int = 10, 
        font: str = "freesansbold.ttf",
        color = (0, 0, 0),
        background = (255, 255, 255),
        source = None,
        image = None,
        bold: bool = False,
        italic: bool = False,
        pos_x: int = 0, 
        pos_y: int = 0,
        width: int = 0,
        height: int = 0,
        surface = None,
        **kwargs):
        
        super().__init__(*args, **kwargs)
        
        self.text = text
        self.size = size
        self.font = pygame.font.Font(font, self.size)
        self.color = color
        self.bg_color = background
        self.source = source
        self.image = image
        self.bold = bold
        self.italic = italic
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.surface = surface
        
        self.hidden = False
        self.run_count = 1
        self.button_name = ""
        
        self.clicked = False
        
    def click_detection(func):
        # self.run_count = 1
        def wrapper_function(self, *args, **kwargs):
            left_click = pygame.mouse.get_pressed(3)[0]
            mouse_pos = pygame.mouse.get_pos()
            
            pos_in_mask = mouse_pos[0] - self.rect.x, mouse_pos[1] - self.rect.y
            
            if (left_click and 
                self.rect.collidepoint(mouse_pos) and 
                self.mask.get_at(pos_in_mask) and 
                not self.clicked):
                
                self.clicked = True
                
                func(self, *args, **kwargs)
                

            # if self.clicked:
            #     self.clicked = False
                
        return wrapper_function  
                
    def update(self):
        self.handle_image()
        
        if not self.hidden:
            self.rendering_object()
            
        self.update_positions()
        
        


