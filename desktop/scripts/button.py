import pygame


from game_object import GameObject
from text_object import TextObject
import config as c


class Button(GameObject):
    def __init__(self, x, y, w, h, text, on_click=lambda x: None):
        self.button_name = text
        self.x = x
        self.y = y
        super().__init__(x, y, w, h)
        self.state = 'normal'
        self.on_click = on_click
        self.image = pygame.image.load(f"desktop/Buttons/{self.button_name}.png")
        
        self.normal = pygame.image.load(f"desktop/Buttons/{self.button_name}.png")
        self.clicked = pygame.image.load(f"desktop/Buttons/{self.button_name}_clicked.png")
        self.hovered = pygame.image.load(f"desktop/Buttons/{self.button_name}_hovered.png")


    @property
    def back_color(self):
        return dict(normal=self.normal,
                    clicked=self.clicked,
                    hovered=self.hovered)[self.state]

    def draw(self, surface):
        surface.blit(self.back_color, (self.x, self.y))

    def handle_mouse_event(self, type, pos):
        if type == pygame.MOUSEMOTION:
            self.handle_mouse_move(pos)
            
        elif type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_down(pos)
            
        elif type == pygame.MOUSEBUTTONUP:
            self.handle_mouse_up(pos)

    def handle_mouse_move(self, pos):
        if self.bounds.collidepoint(pos):
            if self.state != 'clicked':
                self.state = 'hovered'
        else:
            self.state = 'normal'

    def handle_mouse_down(self, pos):
        if self.bounds.collidepoint(pos):
            self.state = 'clicked'
            
    def handle_mouse_up(self, pos):
        if self.state == 'clicked':
            self.on_click(self)
            self.state = 'hovered'