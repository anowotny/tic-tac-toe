import pygame
from grid import Grid
import socket
import threading
import os
import time

pygame.font.init()
os.environ['SDL_VIDEO_WINDOW_POS'] = '100,100'


surface = pygame.display.set_mode((600,700))
pygame.display.set_caption('Tic tac toe game - PLAYER 1')



def message_to_screen(msg):
    screen_text=font.render(msg,True,(144,234,6))
    surface.blit(screen_text,[300,300])

def create_thread(target):
    thread=threading.Thread(target=target)
    thread.daemon=True
    thread.start()



host='127.0.0.1'
port=33355
connection_established=False
connection,addr=None,None
sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind((host,port))
sock.listen(1)

def receive_data():
    global turn
    while True:
        data = connection.recv(1024).decode()
        data=data.split('-')
        x = int(data[0])
        y = int(data[1])
        if data[2] == 'yourturn':
            turn = True
        if data[3] == 'False':
            grid.playerWins = True
        if grid.getCellValue(x,y)==0:
            grid.setCellValue(x,y,'O')
        print(data)

def wait_for_conn():
    global connection_established,connection,addr
    #if not connection_established:
    if not connection_established:
        print("Waiting for player 2...")

    connection, addr = sock.accept()  # czekaj na polaczenie
    print("Player 2 is connected!")
    connection_established=True
    receive_data()

create_thread(wait_for_conn)


grid = Grid()

running = True
player="X"
turn=True
playing='True'
font=pygame.font.SysFont("inkfree",35,True)
font1=pygame.font.SysFont("inkfree",50)
welcome=font.render("Welcome to Tic Tac Toe", True,(155,23,235))
text=font.render(" Waiting for Player 2...",True,(122,245,2))
player1=font1.render("Player 1",True,(255,255,255))
restart=font.render("R - restart, Q - quit", True, (255,255,255))
draw=font.render("It's a draw!",True,(0,0,200))
win=font.render("You win!",True,(0,255,0))
loose=font.render("You loose",True,(255,0,0))

while running:

    if not connection_established:
        surface.blit(welcome,(100,200))
        surface.blit(text,(100,300))
    pygame.display.flip()

    surface.fill((3, 16, 24))
    grid.draw(surface)
    surface.blit(player1,(220,610))
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.MOUSEBUTTONDOWN and connection_established: #or connectionestablished?
            if pygame.mouse.get_pressed()[0]:
                if turn and not grid.playerWins:
                    pos = pygame.mouse.get_pos()
                    cellX, cellY= pos[0]//200,pos[1]//200
                 #podzielic przez dl kwadratu
                    grid.getMouse(cellX,cellY,player)
                    if grid.playerWins:
                        playing='False'

                    send_data='{}-{}-{}-{}'.format(cellX,cellY,"yourturn",playing).encode()
                    connection.send(send_data)
                    turn=False

        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_r and grid.playerWins:
                grid.resetGame()
                grid.playerWins=False
                playing="True"
                print("Game resetted")
            elif event.key==pygame.K_q:
                running=False

    #if grid.playerWins:
     #   if grid.result == player:
      #      surface.blit(win, (220, 300))
       # elif grid.result == None:
        #    surface.blit(draw, (220, 300))
        #else:
         #   surface.blit(loose, (220, 300))
        #surface.blit(restart, (200, 340))

   # pygame.display.flip()