from Grid import Grid as grid
import Constant, Color

import math
import sys,pygame
import time
from tkinter import *
from tkinter import messagebox, Frame, Menu, ttk
from tkinter import ttk

class AStar:
    def __init__(self,map,startGrid,targetGrid,isPathVisible,screen):
        self.map = map
        self.startGrid = startGrid
        self.targetGrid = targetGrid
        self.isPathVisible = isPathVisible
        self.screen = screen
        self.openNodes = []
        self.closedNodes = []
        self.time = None

    def setup(self):
    # create neighbor
        for i in range(Constant.HEIGHT):
            for j in range(Constant.WIDTH):
                self.map[i][j].appendNeighbor(self.map)

        currentGrid = self.startGrid
        self.closedNodes.append(currentGrid)
        neighbors = currentGrid.neighbor[:]
        for i in range(len(neighbors)):
            isDiagonal = self.validateDiagonality(currentGrid, neighbors[i])
            distance = self.findHCost(neighbors[i])
            neighbors[i].updateCost(distance, currentGrid.g_cost, isDiagonal)
            self.openNodes.append(neighbors[i])


    def findHCost(self, grid):
        return math.sqrt((grid.x - self.targetGrid.x) ** 2 + (grid.y - self.targetGrid.y) ** 2)


    def validateDiagonality(self, currentGrid, neighborGrid):
        distance = math.sqrt((currentGrid.x - neighborGrid.x) ** 2 + (currentGrid.y - neighborGrid.y) ** 2)
        if distance > 1:
            return True
        return False


    def excludeWall(self, neighbors):
        i = 0
        while i < len(neighbors):
            if neighbors[i].isWall:
                del neighbors[i]
                i -= 1
            i += 1
        return neighbors

    def run(self):
        self.setup()
        running = True
        self.time = time.time()
        while (running):
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

            # Unreachable to target
            if not self.openNodes:
                root = Tk()
                root.withdraw()
                status = messagebox.askokcancel(title="Failed",
                                                message="Program has failed reaching to target node.\n"
                                                        + "Would you like to retry?")
                root.destroy()

                if status:
                    pygame.quit()
                    return True

                if not status:
                    pygame.quit()
                    sys.exit()
                    return False

            # Compare f cost of each grid in open nodes and find the path
            # Compare h cost of each grid in open nodes and find the path
            j = 0
            for i in range(len(self.openNodes)):
                if self.openNodes[j].f_cost > self.openNodes[i].f_cost:
                    j = i
                if self.openNodes[j].f_cost == self.openNodes[i].f_cost:
                    if self.openNodes[j].h_cost > self.openNodes[i].h_cost:
                        j = i
            currentGrid = self.openNodes[j]

            # target found
            if currentGrid is self.targetGrid:
                currentGrid = currentGrid.parent
                numGrid = 1
                while currentGrid != None:
                    currentGrid.drawColor(self.screen, Color.LIME)
                    pygame.display.update()
                    currentGrid = currentGrid.parent
                    numGrid += 1

                timeTaken = time.time() - self.time
                root = Tk()
                root.withdraw()
                status = messagebox.askokcancel(title="Done!", message="Program has taken " + str(
                    timeTaken) + " seconds and "+str(numGrid)+" steps\nWould you like to continue?")
                root.destroy()

                if status:
                    pygame.quit()
                    return True

                if not status:
                    pygame.quit()
                    sys.exit()
                    return False

            self.openNodes.remove(currentGrid)
            self.closedNodes.append(currentGrid)
            neighbors = self.excludeWall(currentGrid.neighbor[:])

            # update cost of neighbor grids
            for i in range(len(neighbors)):
                if neighbors[i] in self.closedNodes:
                    continue

                isDiagonal = self.validateDiagonality(currentGrid, neighbors[i])

                # not in openNode
                if neighbors[i] not in self.openNodes:
                    distance = self.findHCost(neighbors[i])
                    neighbors[i].updateCost(distance, currentGrid.g_cost, isDiagonal)
                    self.openNodes.append(neighbors[i])
                    neighbors[i].setParent(currentGrid)

                # Already in openNode
                if neighbors[i] in self.openNodes:
                    if isDiagonal:
                        if neighbors[i].g_cost > (currentGrid.g_cost + currentGrid.diagonalWeight):
                            print("updating cost from ", neighbors[i].g_cost, " to ",
                                  currentGrid.g_cost + currentGrid.diagonalWeight)
                            distance = self.findHCost(neighbors[i])
                            neighbors[i].updateCost(distance, currentGrid.g_cost, isDiagonal)
                            neighbors[i].setParent(currentGrid)

                    if not isDiagonal:
                        if neighbors[i].g_cost > (currentGrid.g_cost + currentGrid.weight):
                            print("updating cost from ", neighbors[i].g_cost, " to ",
                                  currentGrid.g_cost + currentGrid.weight)
                            distance = self.findHCost(neighbors[i])
                            neighbors[i].updateCost(distance, currentGrid.g_cost, isDiagonal)
                            neighbors[i].setParent(currentGrid)
            # graphic
            if self.isPathVisible.get():
                for i in range(len(self.openNodes)):
                    self.startGrid.drawColor(self.screen, Color.LIME)
                    self.openNodes[i].drawColor(self.screen, Color.BLUE)

                for i in range(len(self.closedNodes)):
                    self.startGrid.drawColor(self.screen, Color.LIME)
                    self.closedNodes[i].drawColor(self.screen, Color.SKYBLUE)
                pygame.display.update()