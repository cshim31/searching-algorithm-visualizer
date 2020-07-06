from Grid import Grid as grid
import Constant, Color
import math
import threading
import sys,pygame
import time
from tkinter import *
from tkinter import messagebox, Frame, Menu, ttk
from tkinter import ttk

class DFS:
    def __init__(self, map, startGrid, targetGrid, isPathVisible, screen):
        self.map = map
        self.startGrid = startGrid
        self.targetGrid = targetGrid
        self.grid = startGrid
        self.isPathVisible = isPathVisible
        self.screen = screen
        self.time = None
        self.isVisited = []

    def setup(self, map):
        # create neighbor
        self.isVisited = [[0 for i in range(Constant.WIDTH)] for i in range(Constant.HEIGHT)]
        for i in range(Constant.HEIGHT):
            for j in range(Constant.WIDTH):
                map[i][j].appendNeighbor(map)
                self.isVisited[i][j] = False

    def setVisited(self, isVisited, grid):
        isVisited[grid.x][grid.y] = True

    def getVisited(self, isVisited,grid):
        return isVisited[grid.x][grid.y]

    def pushStack(self, stack, grid):
        isVisited = self.isVisited
        neighbors = grid.neighbor[:]
        for i in range (len(neighbors)):
            if self.getVisited(isVisited, neighbors[i]):
                continue
            stack.append(neighbors[i])
            self.setVisited(isVisited, neighbors[i])
            neighbors[i].setParent(grid)

    def dfs(self,grid):
        stack = []
        isVisited = self.isVisited
        if grid.isWall:
            return

        # target found
        if grid is self.targetGrid:
            self.grid = grid
            numGrid = 0
            while self.grid is not None:
                self.grid.drawColor(self.screen, Color.LIME)
                pygame.display.update()
                numGrid += 1
                self.grid = self.grid.parent
            timeTaken = time.time() - self.time
            root = Tk()
            root.withdraw()
            status = messagebox.askokcancel(title="Done!", message="Program has taken " + str(
                timeTaken) + " seconds and " + str(numGrid) + " steps\nWould you like to continue?")
            root.destroy()

            if status:
                pygame.quit()
                return True

            if not status:
                pygame.quit()
                sys.exit()
                return False

        self.setVisited(isVisited,grid)
        self.pushStack(stack,grid)

        if self.isPathVisible.get():
            self.startGrid.drawColor(self.screen, Color.BLUE)
            grid.drawColor(self.screen, Color.SKYBLUE)
            pygame.display.update()

        while stack:
            self.dfs(stack.pop())


    def run(self):
        #sys.setrecursionlimit(1500)
        self.setup(self.map)
        self.time = time.time()
        return self.dfs(self.startGrid)
