import random
from datetime import datetime, timedelta
from threading import Thread
from multiprocessing import Queue
import requests

import os
import time
import pygame
from pygame.rect import Rect

import colors
import config as c

from game import Game
from text_object import TextObject
from game_object import GameObject
from button import Button
from sockets_listen import Socket


class Qu1s(Game):
    def __init__(self):
        Game.__init__(self, 'Breakout', c.frame_rate)
        self.state = 'MENU'
        self.paused = False
        self.menu_buttons = []
        self.info = pygame.display.Info()
        self.max_width = self.info.current_w
        self.max_height = self.info.current_h
        self.change_background = True
        self.queue = Queue()
        
        self.room_code = ''

        self.update()
        

    def create_menu(self):
        
        def on_lobby(button):
            self.menu_buttons = []
            self.objects = []

            self.state = 'LOBBY'
            self.change_background = True
            
        def on_settings(button):
            self.menu_buttons = []
            self.objects = []

            self.state = 'SETTINGS'
            self.change_background = True
            
        def on_exit(button):
            self.menu_buttons = []
            self.objects = []
            
            self.state = 'EXIT'
            self.game_over = True
            self.is_game_running = False

            
            
        if self.change_background: 
            self.background_image = pygame.image.load('desktop/images/backgrounds/main_menu.jpg')
            #self.background_image = pygame.image.load('../images/backgrounds/main_menu.jpg')
            self.background_image = pygame.transform.scale(self.background_image, (self.max_width, self.max_height))
            
            for i, (text, click_handler) in enumerate((('Start', on_lobby),('Settings', on_settings), ('Exit', on_exit))):
                b = Button(c.menu_offset_x,
                        c.menu_offset_y + (c.menu_button_h + 5) * i,
                        c.menu_button_w,
                        c.menu_button_h,
                        text,
                        click_handler)
                self.objects.append(b)
                self.menu_buttons.append(b)
                self.mouse_handlers.append(b.handle_mouse_event)
                
            self.change_background = False
    
    def create_lobby(self):
        
        def on_play(button):
            self.menu_buttons = []
            self.objects = []

            self.state = 'START'
            self.change_background = True
            
        def on_return(button):
            self.menu_buttons = []
            self.objects = []

            self.state = 'MENU'
            self.change_background = True
        

        if self.change_background: 
            
            if self.room_code == '':
                self.sockets = Thread(target = Socket(self.queue,))
                self.sockets.daemon = True
                self.sockets.start()

                while not self.queue.empty():
                    self.room_code = self.queue.get()['code']
                
            self.background_image = pygame.image.load('desktop/images/backgrounds/lobby.jpg')
            #self.background_image = pygame.image.load('../images/backgrounds/lobby.jpg')
            self.background_image = pygame.transform.scale(self.background_image, (self.max_width, self.max_height))
            
            for i, (text, click_handler) in enumerate((('Start', on_play),('Back', on_return))):
                b = Button(c.menu_offset_x,
                        c.menu_offset_y + (c.menu_button_h+5) * i,
                        c.menu_button_w,
                        c.menu_button_h,
                        text,
                        click_handler)
                self.objects.append(b)
                self.menu_buttons.append(b)
                self.mouse_handlers.append(b.handle_mouse_event)
                
            self.change_background = False

    def create_game(self):
        
        def on_return(button):
            self.menu_buttons = []
            self.objects = []

            self.state = 'MENU'
            self.change_background = True
            
        if self.change_background: 
            self.background_image = pygame.image.load('desktop/images/backgrounds/game.jpg')

            for i, (text, click_handler) in enumerate((('Back', on_return), )):
                b = Button(c.menu_offset_x,
                        c.menu_offset_y + (c.menu_button_h+5) * i,
                        c.menu_button_w,
                        c.menu_button_h,
                        text,
                        click_handler)
                self.objects.append(b)
                self.menu_buttons.append(b)
                self.mouse_handlers.append(b.handle_mouse_event)
            
            self.change_background = False
       
    def create_settings(self):
        
        def on_return(button):
            self.menu_buttons = []
            self.objects = []

            self.state = 'MENU'
            self.change_background = True
            
        if self.change_background: 
            self.background_image = pygame.image.load('desktop/images/backgrounds/settings.jpg')

            for i, (text, click_handler) in enumerate((('Back', on_return), )):
                b = Button(c.menu_offset_x,
                        c.menu_offset_y + (c.menu_button_h+5) * i,
                        c.menu_button_w,
                        c.menu_button_h,
                        text,
                        click_handler)
                self.objects.append(b)
                self.menu_buttons.append(b)
                self.mouse_handlers.append(b.handle_mouse_event)  
                
        self.change_background = False
       
    def update(self):
        
        if not self.queue.empty():
            temp = self.queue.get()
            print('QUEUE:',temp)
            Socket.test(temp)
            
        if self.state == 'MENU':
            self.create_menu()
            
        elif self.state == 'LOBBY':
            self.create_lobby()
            
        elif self.state == 'START':
            self.create_game()
        
        elif self.state == 'SETTINGS':
            self.create_settings()
            
        if self.game_over:
            self.show_message('GAME OVER!', centralized=True)

    def show_message(self, text, color=colors.WHITE, font_name='Arial', font_size=20, centralized=False):
        
        
        message = TextObject(c.screen_width // 2, c.screen_height // 2, lambda: text, color, font_name, font_size)
        self.draw()
        message.draw(self.surface, centralized)
        pygame.display.update()
        time.sleep(c.message_duration)


