import pygame
import colors

screen_width = 1600
screen_height = 900

frame_rate = 100

status_offset_y = 50

font_name = 'Arial'
font_size = 20

effect_duration = 20

message_duration = 2

button_text_color = colors.WHITE,
button_normal_back_color = colors.INDIANRED1
button_hover_back_color = colors.INDIANRED2
button_pressed_back_color = colors.INDIANRED3

menu_offset_x = 200
menu_offset_y = 350
menu_button_w = 187
menu_button_h = 62


pygame.mixer.pre_init(44100, -16, 2, 4096)
pygame.mixer.init()
button_hovered = pygame.mixer.Sound('desktop/sounds/button_hovered.wav')
button_hovered.set_volume(0.5)

button_clicked = pygame.mixer.Sound('desktop/sounds/button_clicked.wav')
button_clicked.set_volume(0.5)