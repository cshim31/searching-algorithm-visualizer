import sys,pygame
INFINITY = 100000000

class Grid:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.h_cost = 0
        self.g_cost = 0
        self.f_cost = 0
        self.weight = 10
        self.neighbor = []
        self.parent = None
        self.color = 0
        self.is_Wall = False

    def append_neighbor(self,map,width,height):
        #y-axis
        if self.y-1>=0:
            self.neighbor.append(map[self.x][self.y-1])
        if self.y+1<height:
            self.neighbor.append(map[self.x][self.y+1])
        #x-axis
        if self.x-1>=0:
            self.neighbor.append(map[self.x-1][self.y])
        if self.x+1<width:
            self.neighbor.append(map[self.x+1][self.y])


    #h_cost = distance between target and object
    #g_cost = distance between origin and object
    #f_cost = h_cost + g_cost
    def updateDistance(self,h_cost,g_cost):
        self.h_cost = h_cost
        self.g_cost = g_cost+self.weight
        self.f_cost = self.h_cost+self.g_cost

    def setParent(self,parent):
        self.parent = parent

    def drawColor(self,screen,color,width,height):
        pygame.draw.rect(screen,color,(self.x*12,self.y*12,600/width,600/height))

    def setWall(self):
        self.is_Wall = True
        self.weight = INFINITY


    def reset(self):
        self.h_cost = 0
        self.g_cost = 0
        self.f_cost = 0
        self.weight = 10
        self.neighbor = []
        self.parent = None
        self.color = 0
        self.is_Wall = False
