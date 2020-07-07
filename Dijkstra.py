"""
    Dijkstra explores all the grid and updates distance from current grid and origin
"""
from Grid import Grid as grid
import Constant, Color
import math
import threading
import sys,pygame
import time
from tkinter import *
from tkinter import messagebox, Frame, Menu, ttk
from tkinter import ttk
class Dijkstra:
    def __init__(self, map, startGrid, targetGrid, isPathVisible, screen):
        self.map = map
        self.startGrid = startGrid
        self.targetGrid = targetGrid
        self.grid = startGrid
        self.isPathVisible = isPathVisible
        self.screen = screen
        self.time = None
        self.isVisited = []
        self.priority_queue = []

    def setup(self):
        # create neighbor
        self.isVisited = [[0 for i in range(Constant.WIDTH)] for i in range(Constant.HEIGHT)]
        for i in range(Constant.HEIGHT):
            for j in range(Constant.WIDTH):
                self.map[i][j].appendNeighbor(self.map)
                self.isVisited[i][j] = False

        currentGrid = self.startGrid
        neighbors = currentGrid.neighbor[:]
        for i in range(len(neighbors)):
            isDiagonal = self.validateDiagonality(currentGrid, neighbors[i])
            neighbors[i].updateCost(0, currentGrid.g_cost, isDiagonal)

    #def getSmallIndex(self):

    #def dijkstra(self):

    #def run(self):
        self.setup()
        self.time = time.time()
        selt.dijkstra()
