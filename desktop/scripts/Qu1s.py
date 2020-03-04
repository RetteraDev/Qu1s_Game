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
        Game.__init__(self, 'Qu1s', c.frame_rate)
        self.state = 'MENU'
        self.paused = False
        self.menu_buttons = []
        self.info = pygame.display.Info()
        self.max_width = self.info.current_w
        self.max_height = self.info.current_h
        
        self.change_background = True
        self.change_players = True
        
        self.queue = Queue()
        
        self.room_code = ''
        self.players = []
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
            self.player_objects = []
            self.menu_buttons = []
            self.objects = []

            self.state = 'START'
            self.change_background = True
            
        def on_return(button):
            self.player_objects = []
            self.menu_buttons = []
            self.objects = []
            
            self.state = 'MENU'
            self.change_background = True
            self.room_code = ''

        # Если комната рисуется впервые
        if self.change_background or self.change_players: 
            
            if self.room_code == '':
                
                self.sockets = Thread(target = Socket(self.queue).run)
                self.sockets.daemon = True
                self.sockets.start()
                self.sockets.running = False
                
                while self.queue.empty():
                    time.sleep(0.1)
                    
                temp = self.queue.get()
                self.room_code = f"Код: {str(temp['code'])}"
                    #print(self.room_code)
            
            self.background_image = pygame.image.load('desktop/images/backgrounds/lobby.jpg')
            #self.background_image = pygame.image.load('../images/backgrounds/lobby.jpg')
            self.background_image = pygame.transform.scale(self.background_image, (self.max_width, self.max_height))
            
            start = Button(self.max_width - c.menu_button_w, 0, # Положение кнопки на экране
                           c.menu_button_w, c.menu_button_h,    # Размеры кнопки
                           'Start',                             # Текст кнопки, нужен для импорта изображения
                           on_play)                             # Функция обработчик при нажатии на кнопку
            
            back = Button(0, 0,
                          c.menu_button_w, c.menu_button_h,
                          'Back',
                          on_return)
            
            # Вывод кода комнаты
            code = TextObject(self.max_width//2-5-len(self.room_code), 5, self.room_code, color = colors.GREEN, font_name='Arial', font_size=20)
            self.objects.append(code)
            
            for i in [start, back]:
                self.objects.append(i)
                self.menu_buttons.append(i)
                self.mouse_handlers.append(i.handle_mouse_event)

            self.change_background = False
            
            
            # Если в комнате изменились игроки
            if self.change_players:
                
                # Вывод игроков
                self.posX_text, self.posY_text = 20, 80
                for player in self.players:
                    new_player = TextObject(self.posX_text, self.posY_text, str(player), color = colors.GREEN, font_name='Arial', font_size=20)
                    self.posY_text += 20
                    self.player_objects.append(new_player)
                self.change_players = False      

    def create_game(self):
        
        def on_return(button):
            self.menu_buttons = []
            self.objects = []

            self.state = 'MENU'
            self.change_background = True
            self.room_code = ''
            
        if self.change_background: 
            self.background_image = pygame.image.load('desktop/images/backgrounds/game.jpg')

            back = Button(0, 0,
                          c.menu_button_w, c.menu_button_h,
                          'Back',
                          on_return)
            self.objects.append(back)
            self.menu_buttons.append(back)
            self.mouse_handlers.append(back.handle_mouse_event)
            
            self.change_background = False
        
        if self.change_players:
            self.posX_text, self.posY_text = 20, 80
            for name in self.players:
                name = TextObject(self.posX_text, self.posY_text, lambda: name, color = colors.GREEN, font_name='Arial', font_size=20)
                self.posY_text += 20
                self.player_objects.append(name)
            self.change_players = False
        
        
    def create_settings(self):
        
        def on_return(button):
            self.menu_buttons = []
            self.objects = []

            self.state = 'MENU'
            self.change_background = True
            
        if self.change_background: 
            self.background_image = pygame.image.load('desktop/images/backgrounds/settings.jpg')

            back = Button(0, 0,
                          c.menu_button_w, c.menu_button_h,
                          'Back',
                          on_return)
            self.objects.append(back)
            self.menu_buttons.append(back)
            self.mouse_handlers.append(back.handle_mouse_event)
            
                
        self.change_background = False
       
    def update(self):

        if not self.queue.empty():
            temp = self.queue.get()
                
            if 'players' in temp:
                self.players = temp['players']
                self.change_players = True
                self.player_objects = []

            elif 'answer' in temp:
                print('QUEUE:',temp)
            # Socket.test(temp)
            
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

    def show_message(self, text, color=colors.WHITE, font_name='Arial', font_size=20, centralized=True):
        
        message = TextObject(c.screen_width // 2, c.screen_height // 2, text, color, font_name, font_size)
        self.draw()
        message.draw(self.surface)
        pygame.display.update()
        time.sleep(c.message_duration)


