import random
from datetime import datetime, timedelta
from threading import Thread
from multiprocessing import Queue
import requests

import os
import sys
import time
import pygame
from pygame.rect import Rect

import colors

from game import Game
from text_object import TextObject
from game_object import GameObject
from button import Button
from slider import Slider
from sockets_listen import Socket
from sfx import *

import configparser

config = configparser.ConfigParser()
config.read('desktop/scripts/config.ini')

settings = configparser.ConfigParser()
settings.read('desktop/scripts/config.ini')

class Qu1s(Game):
    def __init__(self):
        Game.__init__(self)
        self.state = 'MENU'
        self.paused = False
        self.menu_buttons = []
        self.info = pygame.display.Info()
        self.max_width = self.info.current_w
        self.max_height = self.info.current_h
        
        # Адаптивность под разные разрешения на основе моего базового 1600х900
        self.coefficent = self.max_width/1600

        self.change_background = True
        self.change_players = True
        
        self.queue = Queue()
        
        self.room_code = ''
        self.players = []
        self.update()
        
        pygame.mixer.music.load(config['SOUNDS']['MAIN_THEME'])
        pygame.mixer.music.set_volume(config.getfloat('SOUNDS', 'MAIN_THEME_VOLUME'))
        pygame.mixer.music.play(-1)

    # Зануляем все отрисованные объекты
    def clearing(self, state):
        
        self.mouse_handlers = []
        self.player_objects = []
        self.menu_buttons = []
        self.objects = []
        self.state = state
        self.change_background = True
    
    def create_menu(self):
        
        def on_lobby(button):
            self.clearing('LOBBY')
            
        def on_settings(button):
            self.clearing('SETTINGS')
            
        def on_exit(button):
            self.clearing('EXIT')
            
            self.game_over = True
            self.is_game_running = False

        if self.change_background: 
            self.background_image = pygame.image.load(config['BACKGROUNDS']['MAIN_MENU'])

            self.background_image = pygame.transform.scale(self.background_image, (self.max_width, self.max_height))
            
            for i, (text, click_handler) in enumerate((('Start', on_lobby),('Settings', on_settings), ('Exit', on_exit))):
                b = Button( config.getint('SETTINGS', 'SCREEN_WIDTH')//8,
                            config.getint('SETTINGS', 'SCREEN_HEIGHT')//2.5 + (config.getint('BUTTONS', 'MENU_BUTTON_H')*self.coefficent + 5) * i,
                            config.getint('BUTTONS', 'MENU_BUTTON_W')*self.coefficent,
                            config.getint('BUTTONS', 'MENU_BUTTON_H')*self.coefficent,
                            text,
                            click_handler)
                self.objects.append(b)
                self.menu_buttons.append(b)
                self.mouse_handlers.append(b.handle_mouse_event)
                
            self.change_background = False
    
    def create_lobby(self):
        
        def on_play(button):
            self.clearing('START')

            # Начинает музыку с нуля, ставит на паузу
            pygame.mixer.music.rewind()
            pygame.mixer.music.pause()
            
        def on_return(button):
            
            self.clearing('MENU')
            self.players = []

            self.room_code = ''
            self.socket.close_room()


        # Если комната рисуется впервые
        if self.change_background or self.change_players: 
            
            if self.room_code == '':
                
                # Запускаем поток сокетов
                self.socket = Socket(self.queue)
                self.socket.setDaemon(True)
                self.socket.start()
                
                # Ждем, когда придет код комнаты
                #@todo Сделать выход в главное меню, если ждет код дольше 3ех секунд
                while self.queue.empty():
                    time.sleep(0.1)
                
                # Получаем код из очереди
                temp = self.queue.get()
                self.room_code = f"Код: {str(temp['code'])}"
                    #print(self.room_code)
            
            # Подгружаем фон и масштабируем на весь экран
            self.background_image = pygame.image.load(config['BACKGROUNDS']['LOBBY'])
            self.background_image = pygame.transform.scale(self.background_image, (self.max_width, self.max_height))
            
            start = Button(self.max_width - config.getint('BUTTONS', 'MENU_BUTTON_W'), 0,     # Положение кнопки на экране
                           config.getint('BUTTONS', 'MENU_BUTTON_W')*self.coefficent, # Размеры
                           config.getint('BUTTONS', 'MENU_BUTTON_H')*self.coefficent, # кнопки
                           'Start',                                 # Текст кнопки, нужен для импорта изображения
                           on_play)                                 # Функция обработчик при нажатии на кнопку
            
            back = Button(0, 0,
                          config.getint('BUTTONS', 'MENU_BUTTON_W'), 
                          config.getint('BUTTONS', 'MENU_BUTTON_H'),
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
            
            self.clearing('MENU')
            self.room_code = ''
            self.socket.close_room()
            
            # Музыка снимается с паузы
            pygame.mixer.music.unpause()
            
            
        if self.change_background: 
            
            # Подгружаем фон и масштабируем на весь экран
            self.background_image = pygame.image.load(config['BACKGROUNDS']['GAME'])
            self.background_image = pygame.transform.scale(self.background_image, (self.max_width, self.max_height))
            
            back = Button(0, 0,
                          config.getint('BUTTONS', 'MENU_BUTTON_W')*self.coefficent,
                          config.getint('BUTTONS', 'MENU_BUTTON_H')*self.coefficent,
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
            # Если игрок вышел без сохранения вернуть звук в исходную громкость
            button_hovered.set_volume(config.getfloat('SOUNDS', 'BUTTON_VOLUME'))
            button_clicked.set_volume(config.getfloat('SOUNDS', 'BUTTON_VOLUME'))
            pygame.mixer.music.set_volume(config.getfloat('SOUNDS', 'MAIN_THEME_VOLUME'))

            # Возвращаем исходные разрешения экрана, громкость звука
            settings['SETTINGS']['SCREEN_WIDTH'] = str(config.getint('SETTINGS', 'SCREEN_WIDTH'))
            settings['SETTINGS']['SCREEN_HEIGHT'] = str(config.getint('SETTINGS', 'SCREEN_HEIGHT'))
            settings['SOUNDS']['BUTTON_VOLUME'] = str(config.getfloat('SOUNDS', 'BUTTON_VOLUME'))
            settings['SOUNDS']['MAIN_THEME_VOLUME'] = str(config.getfloat('SOUNDS', 'MAIN_THEME_VOLUME'))

            self.clearing('MENU')

        def on_lower_resolution(button):
            self.current_resolution_index -= 1
            settings['SETTINGS']['SCREEN_WIDTH'] = str(self.resolutions[self.current_resolution_index][0])
            settings['SETTINGS']['SCREEN_HEIGHT'] = str(self.resolutions[self.current_resolution_index][1])
            self.clearing('SETTINGS')

        def on_higher_resolution(button):
            self.current_resolution_index += 1
            settings['SETTINGS']['SCREEN_WIDTH'] = str(self.resolutions[self.current_resolution_index][0])
            settings['SETTINGS']['SCREEN_HEIGHT'] = str(self.resolutions[self.current_resolution_index][1])
            self.clearing('SETTINGS')

        def on_volume_sfx(button):
            settings['SOUNDS']['BUTTON_VOLUME'] = str(button.value)
            # Делаем звук громче или тише в режиме реального времени
            button_hovered.set_volume(settings.getfloat('SOUNDS', 'BUTTON_VOLUME'))
            button_clicked.set_volume(settings.getfloat('SOUNDS', 'BUTTON_VOLUME'))

        def on_main_theme(button):
            settings['SOUNDS']['MAIN_THEME_VOLUME'] = str(button.value)

            # Делаем звук громче или тише в режиме реального времени
            pygame.mixer.music.set_volume(settings.getfloat('SOUNDS', 'MAIN_THEME_VOLUME'))


        def on_submit(button):
            settings['SETTINGS']['SCREEN_WIDTH'] = str(self.current_resolution[0])
            settings['SETTINGS']['SCREEN_HEIGHT'] = str(self.current_resolution[1])
            with open('desktop/scripts/config.ini', 'w') as configfile:
                settings.write(configfile)
            
            self.clearing('MENU')


        # Костыль для корректного отображения разрешения экрана в настройках
        self.current_resolution = (settings.getint('SETTINGS', 'SCREEN_WIDTH'), settings.getint('SETTINGS', 'SCREEN_HEIGHT'))
        self.resolutions = [(640, 480), (800, 600), (1024, 576), (1280, 720), (1366, 786), (1600, 900), (1920, 1080)]
        if self.current_resolution in self.resolutions:
            self.current_resolution_index = self.resolutions.index(self.current_resolution)
        else: 
            self.current_resolution_index = 0


        if self.change_background: 
            
            self.background_image = pygame.image.load(config['BACKGROUNDS']['SETTINGS'])
            self.background_image = pygame.transform.scale(self.background_image, (self.max_width, self.max_height))

            buttons = []

            back = Button(0, 0, # Положение кнопки на экране
                          config.getint('BUTTONS', 'MENU_BUTTON_W')*self.coefficent,
                          config.getint('BUTTONS', 'MENU_BUTTON_H')*self.coefficent, # Размеры кнопки
                          'Back', # Текст кнопки, нужен для импорта изображения
                          on_return) # Функция обработчик при нажатии на кнопку
            
            ### Размер экрана ###

            text = 'Разрешение экрана'
            text = TextObject(self.max_width//4*self.coefficent, 300*self.coefficent, 
                              text, color = colors.BLACK, font_name='Arial', font_size=20)
            self.objects.append(text)

            # Левая стрелка разрешения экрана
            left = Button(self.max_width//2 - 5,
                          300*self.coefficent - config.getint('BUTTONS', 'ARROW_BUTTON_H')*self.coefficent//3, # Положение кнопки на экране
                          config.getint('BUTTONS', 'ARROW_BUTTON_W')*self.coefficent,
                          config.getint('BUTTONS', 'ARROW_BUTTON_H')*self.coefficent, # Размеры кнопки
                          'LArrow', # Текст кнопки, нужен для импорта изображения
                          on_lower_resolution)  

            # Текст разрешения экрана
            text = f"{settings['SETTINGS']['SCREEN_WIDTH']}x{settings['SETTINGS']['SCREEN_HEIGHT']}"
            text = TextObject(self.max_width//2 + config.getint('BUTTONS', 'ARROW_BUTTON_W')*self.coefficent, 
                              300*self.coefficent, text, color = colors.BLACK, font_name='Arial', font_size=int(20*self.coefficent))
            self.objects.append(text)

            # Правая стрелка разрешения экрана
            right = Button(self.max_width//2 + (config.getint('BUTTONS', 'SLIDER_BUTTON_W')-config.getint('BUTTONS', 'ARROW_BUTTON_W'))*self.coefficent + 5,
                           300*self.coefficent - config.getint('BUTTONS', 'ARROW_BUTTON_H')*self.coefficent//3, # Положение кнопки на экране
                          config.getint('BUTTONS', 'ARROW_BUTTON_W')*self.coefficent,
                          config.getint('BUTTONS', 'ARROW_BUTTON_H')*self.coefficent, # Размеры кнопки
                          'RArrow', # Текст кнопки, нужен для импорта изображения
                          on_higher_resolution)
            #######################

            ### Громкость звука ###
            text = 'Громкость музыки'
            text = TextObject(self.max_width//4*self.coefficent, 400*self.coefficent, 
                              text, color = colors.BLACK, font_name='Arial', font_size=20)
            self.objects.append(text)

            song_volume = Slider(self.max_width//2, 
                           400*self.coefficent, # Положение кнопки на экране
                          config.getint('BUTTONS', 'SLIDER_BUTTON_W')*self.coefficent,
                          config.getint('BUTTONS', 'SLIDER_BUTTON_H')*self.coefficent, # Размеры кнопки
                          'Slider', 'main_theme', settings.getfloat('SOUNDS', 'MAIN_THEME_VOLUME'),
                          on_main_theme)

            text = 'Громкость спецэффектов'
            text = TextObject(self.max_width//4*self.coefficent, 500*self.coefficent, 
                              text, color = colors.BLACK, font_name='Arial', font_size=20)
            self.objects.append(text)
            
            sfx_volume = Slider(self.max_width//2, 
                           500*self.coefficent, # Положение кнопки на экране
                          config.getint('BUTTONS', 'SLIDER_BUTTON_W')*self.coefficent,
                          config.getint('BUTTONS', 'SLIDER_BUTTON_H')*self.coefficent, # Размеры кнопки
                          'Slider', 'button', settings.getfloat('SOUNDS', 'BUTTON_VOLUME'),
                          on_volume_sfx)

            buttons.append(song_volume)
            buttons.append(sfx_volume)
            #######################

            submit = Button(self.max_width - config.getint('BUTTONS', 'MENU_BUTTON_W')*self.coefficent, 0, # Положение кнопки на экране
                          config.getint('BUTTONS', 'MENU_BUTTON_W')*self.coefficent,
                          config.getint('BUTTONS', 'MENU_BUTTON_H')*self.coefficent, # Размеры кнопки
                          'Submit',                           # Текст кнопки, нужен для импорта изображения
                          on_submit) 
            
            
            buttons.append(back)
            buttons.append(submit)
            # Убираем кнопки, если достигли крайних значений разрешения экрана
            if self.current_resolution_index > 0:
                buttons.append(left)
            if self.current_resolution_index < 6:
                buttons.append(right)
            
            for i in buttons:
                self.objects.append(i)
                self.menu_buttons.append(i)
                self.mouse_handlers.append(i.handle_mouse_event)

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
            #@todo Отправка ответа на сервер
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

    def show_message(self, text, color=colors.WHITE, font_name=config['TEXT']['FONT_NAME'],
                     font_size=config.getint('TEXT', 'FONT_SIZE'), centralized=True):
        
        message = TextObject(config.getint('SETTINGS', 'SCREEN_WIDTH') // 2 - len(text),
                             config.getint('SETTINGS', 'SCREEN_HEIGHT') // 2 - len(text),
                             text, color, font_name, font_size)
        self.draw()
        message.draw(self.surface)
        pygame.display.update()
        pygame.mixer.music.fadeout(2000)
        time.sleep(config.getint('TEXT', 'MESSAGE_DURATION'))


