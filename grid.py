import pygame
import os


letX=pygame.image.load(os.path.join('res','x.png'))
letO=pygame.image.load(os.path.join('res','o.png'))

#font=pygame.font.Font('arialblack',50)

class Grid:
    def __init__(self):
        self.grid_lines=[((0,200), (600,200)),
                         ((0,400), (600,400)),
                         ((200,0), (200,600)),
                         ((400,0), (400,600)),
                         ((0,600),(600,600))]

        self.grid = [[0 for x in range (3)]for y in range(3)] #tworzenie macierzy
        #search directions N    NW      W      SW     S     SE    E     NE
        self.searchDir=[(0,-1),(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1)]
        self.playerWins=False
        self.result=''

    def draw(self, surface):
        for line in self.grid_lines:
            pygame.draw.line(surface,(100,120,199),line[0],line[1],2)

        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.getCellValue(x,y)=="X":
                    surface.blit(letX,(x*200,y*200))
                elif self.getCellValue(x,y)=="O":
                    surface.blit(letO,(x*200,y*200))

    def getCellValue(self,x,y):
        return self.grid[y][x]

    def setCellValue(self,x,y,value):
        self.grid[y][x] = value

    def getMouse(self,x,y,player):
        if self.getCellValue(x,y)==0:
            self.setCellValue(x,y,player)
            self.checkGrid(x,y,player)


    def isWithinBounds(self,x,y):  #bool
        return x>=0 and x<3 and y>=0 and y<3

    def checkGrid(self,x,y,player):
        count=1
        for index,(dirx,diry) in enumerate(self.searchDir):
            if self.isWithinBounds(x+dirx,y+diry) and self.getCellValue(x+dirx,y+diry)==player:
                count+=1
                x1=x+dirx
                y1=y+diry
                if self.isWithinBounds(x1+dirx,y1+diry) and self.getCellValue(x1+dirx,y1+diry)==player:
                    count+=1
                    if count==3:
                        break
                if count <3:
                    newDir=0
                    if index==0:
                        newDir=self.searchDir[4] # n to s
                    elif index==1:
                        newDir=self.searchDir[5]  #nw to se
                    elif index==2:
                        newDir=self.searchDir[6] # w to e
                    elif index==3:
                        newDir=self.searchDir[7] #sw to ne
                    elif index == 4:
                        newDir = self.searchDir[0]  # s to n
                    elif index == 5:
                        newDir = self.searchDir[1]  # se to nw
                    elif index == 6:
                        newDir = self.searchDir[2]  # e to w
                    elif index == 7:
                        newDir = self.searchDir[3]  # ne to sw

                    if self.isWithinBounds(x+newDir[0],y+newDir[1]) \
                        and self.getCellValue(x+newDir[0],y+newDir[1])==player:
                        count+=1
                        if count==3:
                            break
                    else:
                        count=1

        if count==3:
            print(player,"wins")
            print("R reset, Q quit")
            self.result=player
            self.playerWins=True
        elif self.gridFull():
            self.playerWins=self.gridFull()
            print("It's a draw! Reset [r], quit[q]")

            self.result=None

    #def check_winner(self,player):



    def gridFull(self):
        for row in self.grid:
            for val in row:
                if val==0:
                    return False
        return True


    def resetGame(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                self.setCellValue(x,y,0)


    def print_grid(self):
        for row in self.grid:
            print(row)