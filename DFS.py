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

    def setup(self):
        # create neighbor
        self.isVisited = [[0 for i in range(Constant.WIDTH)] for i in range(Constant.HEIGHT)]
        for i in range(Constant.HEIGHT):
            for j in range(Constant.WIDTH):
                self.map[i][j].appendNeighbor(map)
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

    def showPopUp(self, targetFound):
        title = ""
        message = ""
        if targetFound:
            timeTaken = time.time() - self.time
            numGrid = 0
            while self.grid is not None:
                self.grid.drawColor(self.screen, Color.LIME)
                pygame.display.update()
                numGrid += 1
                self.grid = self.grid.parent
            title = "Done!"
            message = "Program has taken " + str(
            timeTaken) + " seconds and " + str(numGrid) + " steps\nWould you like to continue?"

        if not targetFound:
            title = "Failed"
            message = "Program has failed reaching to target\nWould you like to continue?"

        root = Tk()
        root.withdraw()
        status = messagebox.askokcancel(title=title, message= message)
        root.destroy()

        if status:
            pygame.quit()
            return True

        if not status:
            pygame.quit()
            sys.exit()
            return False

    def dfs(self,grid):
        print(grid.x," ",grid.y)
        time.sleep(0.01)
        stack = []
        isVisited = self.isVisited
        if grid.isWall:
            return False

        # target found
        if grid is self.targetGrid:
            self.grid = grid
            print("target Found ! x: ", grid.x, " y: ", grid.y)
            return True

        self.setVisited(isVisited,grid)
        self.pushStack(stack,grid)

        if self.isPathVisible.get():
            self.startGrid.drawColor(self.screen, Color.BLUE)
            grid.drawColor(self.screen, Color.SKYBLUE)
            pygame.display.update()

        while stack:
            targetFound = self.dfs(stack.pop())
            if targetFound:
                return True

        return False

    def run(self):
        #sys.setrecursionlimit(1500)
        self.setup(self.map)
        self.time = time.time()
        targetFound = self.dfs(self.startGrid)
        if targetFound:
            return self.showPopUp(targetFound)
        if not targetFound:
            return self.showPopUp(not targetFound)
