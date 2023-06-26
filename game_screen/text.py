import pygame

class Text:
    def __init__(
        self, 
        text: str = "", 
        size: int = 10, 
        font: str = "freesansbold",
        color = (0, 0, 0),
        bold: bool = False,
        italic: bool = False,
        pos_x: int = 0, 
        pos_y: int = 0,
        width: int = 0,
        height: int = 0,
        outline: int = 0,
        surface = None
    ):  
        self.text = text
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.surface = surface
        self.color = color
        self.outline = outline
        self.font = pygame.font.SysFont(font, size, bold, italic)
        self.get_size = True
        
    def text_size(self):
        return (self.width, self.height)
        
    def display_text(self):
        text_surf = self.font.render(self.text, True, self.color)
        text_rect = text_surf.get_rect()
        text_rect.topleft = (self.pos_x, self.pos_y)
        text_rect.center = (self.pos_x + self.width // 2, self.pos_y + self.height // 2)
        text_rect.width = self.width
        text_rect.height = self.height
        
        if not self.get_size:
            self.width = text_rect.width
            self.height = text_rect.height
            self.get_size = False
            
        if self.outline > 0:
            bg_rect = pygame.Rect(self.pos_x, self.pos_y, self.width, self.height)
                
            pygame.draw.rect(
                surface=self.surface, 
                color=(0, 0, 0),
                rect=bg_rect,
                width=self.outline,
                border_radius=2
            )
        
        self.surface.blit(text_surf, text_rect)
        
        
        # pygame.draw.rect(
        #     surface=self.surface, 
        #     color=(0, 0, 0),
        #     rect=text_surf
        # )
        
        