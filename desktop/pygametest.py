from socketIO_client import SocketIO
import requests
import pygame
import time


### Client connection ###
socketIO = SocketIO('192.168.43.217', 8080) 
    
players = []
submit_code = ''

def new_user(name):
    print('blyat', name)
    if name not in players:
        players.append(name)

def left_user(name):
    if name in players:
        players.remove(name)

def get_code(code):
    global submit_code
    submit_code = code


socketIO.emit('new_room')
socketIO.on('get_room_code', get_code)
socketIO.wait(seconds=1)

#########################


WIDTH = 480
HEIGHT = 360


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

font = pygame.font.Font('freesansbold.ttf', 20)

pygame.display.set_caption('PartyGame')

# Colors tulips
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)



running = True

while running:
    
    # Checking new users

    socketIO.on('new_user', new_user)
    socketIO.on('left_user', left_user)
    socketIO.wait(seconds=1)
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False
            
            
    ### HUD Draving ###
    x, y = 20, 20   
    text = font.render("Участники", True, BLACK)
    screen.blit(text, (WIDTH//2-text.get_width()//2, 10))
    
    pygame.draw.line(screen, BLACK, (0, 40), (WIDTH, 40), 1)
    
    # Names of players
    y = 60
    for name in players:
        pygame.draw.rect(screen, GREEN, (x, y, WIDTH-2*x, 30))
        new_text = font.render(str(name), True, BLACK)
        screen.blit(new_text, (x, y))
        y += 40
        
    pygame.draw.line(screen, BLACK, (0, HEIGHT-40), (WIDTH, HEIGHT-40), 1)
    
    text = font.render(f"Код комнаты - {submit_code}", True, BLACK)
    screen.blit(text, (WIDTH//2-text.get_width()//2, HEIGHT-30)) 
    ####################
    
    
    pygame.display.flip()
          
pygame.quit()
