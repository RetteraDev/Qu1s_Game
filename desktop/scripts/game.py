from collections import defaultdict
from pygame.locals import *
import configparser
import pygame
import sys

config = configparser.ConfigParser()
config.read('desktop/scripts/config.ini')

class Game:
    def __init__(self):
                
        self.frame_rate = config.getint('SETTINGS', 'FRAME_RATE')
        self.game_over = False
        
        self.player_objects = []
        self.objects = []
        
        pygame.init()
        
        max_width = config.getint('SETTINGS', 'SCREEN_WIDTH')
        max_height = config.getint('SETTINGS', 'SCREEN_HEIGHT')
        
        pygame.font.init()
        
        try:
            if config.getboolean('SETTINGS','FULLSCREEN'):
                self.surface = pygame.display.set_mode((max_width, max_height), pygame.FULLSCREEN)
            else:
                info = pygame.display.Info()
                self.surface = pygame.display.set_mode((max_width, max_height))

        except pygame.error:
            info = pygame.display.Info()
            max_width = info.current_w
            max_height = info.current_h
            
            config['SETTINGS']['SCREEN_WIDTH'] = str(max_width)
            config['SETTINGS']['SCREEN_HEIGHT'] = str(max_height)
            with open('desktop/scripts/config.ini', 'w') as configfile:
                config.write(configfile)
                
            if config.getboolean('SETTINGS','FULLSCREEN'):
                self.surface = pygame.display.set_mode((max_width, max_height), pygame.FULLSCREEN)
            else:
                info = pygame.display.Info()
                self.surface = pygame.display.set_mode((max_width, max_height))
            
        pygame.display.set_caption(config['SETTINGS']['CAPTION'])
        self.clock = pygame.time.Clock()
        self.keydown_handlers = defaultdict(list)
        self.keyup_handlers = defaultdict(list)
        self.mouse_handlers = []

    def update(self):
        for o in self.objects:
            o.update()
        
        for o in self.player_objects:
            o.update()

    def draw(self):
        for o in self.objects:
            o.draw(self.surface)

        for o in self.player_objects:
            o.draw(self.surface)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                for handler in self.keydown_handlers[event.key]:
                    handler(event.key)
            elif event.type == pygame.KEYUP:
                for handler in self.keyup_handlers[event.key]:
                    handler(event.key)
            elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
                for handler in self.mouse_handlers:
                    handler(event.type, event.pos)

    def run(self):
        
        while not self.game_over:
            self.surface.blit(self.background_image, (0, 0))

            self.handle_events()
            self.update()
            self.draw()

            pygame.display.update()
            self.clock.tick(self.frame_rate)
