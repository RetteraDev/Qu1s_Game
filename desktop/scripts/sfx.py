import configparser
import pygame


config = configparser.ConfigParser()
config.read('desktop/scripts/config.ini')

pygame.mixer.pre_init(44100, -16, 2, 4096)
pygame.mixer.init()
button_hovered = pygame.mixer.Sound(config['SOUNDS']['BUTTON_HOVERED'])
button_hovered.set_volume(config.getfloat('SOUNDS', 'BUTTON_VOLUME'))

button_clicked = pygame.mixer.Sound(config['SOUNDS']['BUTTON_CLICKED'])
button_clicked.set_volume(config.getfloat('SOUNDS', 'BUTTON_VOLUME'))

slider_hovered = pygame.mixer.Sound(pygame.mixer.Sound(config['SOUNDS']['BUTTON_HOVERED']))