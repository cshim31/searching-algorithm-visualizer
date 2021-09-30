import sys,pygame
import Constant
import Color
class Grid:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.h_cost = 0
        self.g_cost = 0
        self.f_cost = 0
        self.neighbor = []
        self.parent = None
        self.color = 0
        self.isWall = False
        self.isStart = False
        self.isTarget = False
        self.weight = 10
        self.diagonalWeight = 14

    def appendNeighbor(self,map):
        if self.y - 1 >= 0:
            self.neighbor.append(map[self.x][self.y - 1])
        if self.y + 1 < Constant.HEIGHT:
            self.neighbor.append(map[self.x][self.y + 1])
        if self.x - 1 >= 0:
            self.neighbor.append(map[self.x - 1][self.y])
        if self.x + 1 < Constant.WIDTH:
            self.neighbor.append(map[self.x + 1][self.y])

        if self.x - 1 >= 0 and self.y - 1 >= 0:
            self.neighbor.append(map[self.x - 1][self.y - 1])
        if self.x + 1 < Constant.WIDTH and self.y - 1 >= 0:
            self.neighbor.append(map[self.x + 1][self.y - 1])
        if self.x - 1 >= 0 and self.y + 1 < Constant.HEIGHT:
            self.neighbor.append(map[self.x - 1][self.y + 1])
        if self.x + 1 < Constant.WIDTH and self.y + 1 < Constant.HEIGHT:
            self.neighbor.append(map[self.x + 1][self.y + 1])

    #h_cost = distance between target and current object
    #g_cost = distance between origin and current object
    #f_cost = h_cost + g_cost
    def updateCost(self,h_cost,g_cost, isDiagonal):
        if isDiagonal :
            self.h_cost = h_cost
            self.g_cost = g_cost + self.diagonalWeight
            self.f_cost = self.h_cost + self.g_cost

        if not isDiagonal :
            self.h_cost = h_cost
            self.g_cost = g_cost + self.weight
            self.f_cost = self.h_cost + self.g_cost

    def setParent(self,parent):
        self.parent = parent

    def drawColor(self,screen,color):
        pygame.draw.rect(screen,Color.WHITE,(self.x * 11 + Constant.GRID_PADDING,self.y * 11 + Constant.GRID_PADDING,550/Constant.WIDTH,550/Constant.HEIGHT))
        pygame.draw.rect(screen,color,(self.x * 11 + Constant.GRID_PADDING + 1,self.y * 11 + Constant.GRID_PADDING + 1,550/(Constant.WIDTH + 10),550/(Constant.HEIGHT + 10)))

    def setWall(self):
        self.isWall = True
        self.weight = Constant.INFINITY
        self.diagonalWeight = Constant.INFINITY


    def reset(self):
        self.h_cost = 0
        self.g_cost = 0
        self.f_cost = 0
        self.weight = 10
        self.neighbor = []
        self.parent = None
        self.color = 0
        self.is_Wall = False
