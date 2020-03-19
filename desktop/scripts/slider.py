from game_object import GameObject
from text_object import TextObject
import sfx
import pygame



class Slider(GameObject):
    def __init__(self, x, y, w, h, text, name, value, on_click=lambda x: None):

        self.button_name = text
        self.slider_name = name
        
        self.constantX, self.constantY = x, y
        self.w, self.h = w, h
        
        super().__init__(x, y, w, h)
        self.state = 'normal'
        self.on_click = on_click
        
        self.min_value = self.constantX + self.w//6
        self.max_value = self.constantX + self.w - self.w//6
        
        # Ставим слайдер по оси X в положение согласно конфигу
        self.x, self.y = x + (self.max_value-self.min_value)*value - self.w//3, y
        
        self.image = pygame.image.load(f"desktop/Buttons/{self.button_name}.png")
        
        self.normal_slider = pygame.image.load(f"desktop/Buttons/{self.button_name}.png")
        self.normal_slider = pygame.transform.scale(self.normal_slider, (int(w), int(h)))
        
        self.clicked_slider = pygame.image.load(f"desktop/Buttons/{self.button_name}_clicked.png")
        self.clicked_slider = pygame.transform.scale(self.clicked_slider, (int(w), int(h)))
        
        self.hovered_slider = pygame.image.load(f"desktop/Buttons/{self.button_name}_hovered.png")
        self.hovered_slider = pygame.transform.scale(self.hovered_slider, (int(w), int(h)))
        
        self.slider_BG = pygame.image.load(f"desktop/Buttons/{self.button_name}_BG.png")
        self.slider_BG = pygame.transform.scale(self.slider_BG, (int(w), int(h)))
        
        self.hovered_slider_play = True
        self.clicked_one_time = False
        
        
    @property
    def back_color(self):
        return dict(normal=self.normal_slider,
                    clicked=self.clicked_slider,
                    hovered=self.hovered_slider)[self.state]

    def draw(self, surface):
        surface.blit(self.slider_BG, (self.constantX, self.constantY))
        surface.blit(self.back_color, (self.x, self.y))

    def handle_mouse_event(self, type, pos):
        if type == pygame.MOUSEMOTION:
            self.handle_mouse_move(pos)
            
        elif type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_down(pos)
            
        elif type == pygame.MOUSEBUTTONUP:
            self.handle_mouse_up(pos)
            
    def handle_mouse_move(self, pos):
        # Если курсор в поле слайдера и не нажата кнопка мыши
        if self.bounds.collidepoint(pos) and not pygame.mouse.get_pressed()[0]:
            if self.state != 'clicked':
                self.state = 'hovered'
        else:
            self.state = 'normal'
            
        # Для плавной накрутки слайдера
        if self.clicked_one_time:
            pos = pygame.mouse.get_pos()
            x, y = pos[0], pos[1]
            
            # Для всех положений мышки больше, либо равных правому крайнему положению слайдера
            if x >= self.max_value:
                self.x = self.max_value - self.w//2

            # Для всех положений мышки меньше, либо равных левому крайнему положению слайдера
            elif x <= self.min_value:
                self.x = self.min_value - self.w//2
                
            # Все остальные положения слайдера
            else:
                self.x = x-self.w//2
            
            # Для вычисления значение слайдера от 0 до 1
            if x > self.max_value:
                x = self.max_value
            elif x < self.min_value:
                x = self.min_value
                
            self.value = ((x-self.min_value)/(self.max_value-self.min_value))
            self.on_click(self)
        

    def handle_mouse_down(self, pos):
        if self.bounds.collidepoint(pos):
            self.state = 'clicked'
            self.clicked_one_time = True
            
        if self.clicked_one_time:
            pos = pygame.mouse.get_pos()
            x, y = pos[0], pos[1]
            
            # Для всех положений мышки больше, либо равных правому крайнему положению слайдера
            if x >= self.max_value - 5:
                self.x = self.max_value - self.w//2

            # Для всех положений мышки меньше, либо равных левому крайнему положению слайдера
            elif x <= self.min_value + 5:
                self.x = self.min_value - self.w//2 + 5
                
            # Все остальные положения слайдера
            else:
                self.x = x-self.w//2
            
            # Для вычисления значение слайдера от 0 до 1
            if x > self.max_value:
                x = self.max_value
            elif x < self.min_value:
                x = self.min_value
                
            self.value = ((x-self.min_value)/(self.max_value-self.min_value))
            self.on_click(self)
            
    def handle_mouse_up(self, pos):
        
        # Если курсор в поле слайдера или не нажата кнопка мыши
        if self.bounds.collidepoint(pos) or not pygame.mouse.get_pressed()[0]:
            if self.clicked_one_time:
                self.state = 'normal'
                self.clicked_one_time = False
                sfx.button_clicked.play(0)


