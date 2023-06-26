from objects import MovingObject
import pygame


class MouseObject(MovingObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.rect.x = self.obj.get("pos_x")
        self.rect.y = self.obj.get("pos_y")
        self.width = 45
        self.height = 45
        self.source = "mouse_cursor/images"
        self.image = ["brush_cursor_3.png"]
        self.image_changed = True
        
        # create a mouse
        
    def moving_mouse(self):
        self.pos_x, self.pos_y = pygame.mouse.get_pos()
        # print(self.pos_x, self.pos_y)
        
    def update(self):
        self.handle_image()
        self.rendering_object()
        self.moving_mouse()
        self.update_positions()
        
