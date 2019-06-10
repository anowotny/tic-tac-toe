import pygame
from grid import Grid
import socket
import threading
import os

pygame.init()
os.environ['SDL_VIDEO_WINDOW_POS'] = '900,100'

surface = pygame.display.set_mode((600,700))
pygame.display.set_caption('Tic tac toe game - PLAYER 2')
font=pygame.font.SysFont("inkfree",50)
font1=pygame.font.SysFont("inkfree",35,True)


def create_thread(target):
    thread=threading.Thread(target=target)
    thread.daemon=True
    thread.start()

host='127.0.0.1'
port=33355

sock=socket.socket()
sock.connect((host,port))

def receive_data():
    global turn
    while True:
        data=sock.recv(1024).decode()
        data=data.split('-')

        x = int(data[0])
        y = int(data[1])
        if data[2] == 'yourturn':
            turn = True
        if data[3] == 'False':
            grid.playerWins = True
        if grid.getCellValue(x,y)==0:
            grid.setCellValue(x,y,'X')

        print(data)

create_thread(receive_data)
print("Success! I have been connected!")
grid = Grid()

running = True
player="O"

turn=False
playing='True'
player2=font.render("Player 2",True,(255,255,255))
restart=font.render("R - restart, Q - quit", True, (255,255,255))
draw=font1.render("It's a draw!",True,(0,0,200))
win=font1.render("You win!",True,(0,255,0))
loose=font1.render("You loose",True,(255,0,0))

while running:

    surface.fill((3, 16, 24))
    grid.draw(surface)
    surface.blit(player2,(220,610))
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.MOUSEBUTTONDOWN and not grid.playerWins:
            if pygame.mouse.get_pressed()[0]:
                if turn and not grid.playerWins:
                    pos = pygame.mouse.get_pos()
                    cellX,cellY=pos[0]//200,pos[1]//200 #podzielic przez dl kwadratu
                    grid.getMouse(cellX,cellY,player)
                    if grid.playerWins:
                        playing='False'

                    send_data='{}-{}-{}-{}'.format(cellX,cellY,"yourturn",playing).encode()
                    sock.send(send_data)
                    turn=False

        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_r and grid.playerWins or event.key==pygame.K_r and grid.gridFull():
               grid.resetGame()
               grid.playerWins=False
               playing='True'
               print("Game resetted")
            if event.key==pygame.K_q:
                running=False


   # if grid.playerWins:
    #    if grid.playerWins:
     #       playing = 'False'
      #      if grid.result == player:
       #         surface.blit(win, (220, 300))
        #    elif grid.result == None:
         #       surface.blit(draw, (220, 300))
          #  else:
           #     surface.blit(loose, (220, 300))
        #surface.blit(restart, 200, 340)
    pygame.display.flip()