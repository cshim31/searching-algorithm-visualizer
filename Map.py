from Grid import Grid as grid
import Constant, Color
from AStar import AStar
from BFS import BFS
from DFS import DFS
from Dijkstra import Dijkstra

import math
import sys,pygame
import time
from tkinter import *
from tkinter import messagebox, Frame, Menu, ttk
from tkinter import ttk
class Map:
    def __init__(self):
        self.map = []
        self.startGrid = None
        self.targetGrid = None
        self.isPathVisible = None
        self.algorithmType = None
        self.Algorithms = [
            ("DFS", "DFS", 100, 110),
            ("BFS", "BFS", 250, 110),
            ("A* Finding", "A*", 400, 110),
            ("Dijkstra", "Dijkstra", 550, 110),
        ]
        # Graphic variables
        self.screen = pygame.display.set_mode(Constant.WINDOW_SIZE)
        self.screen.fill(Color.GRAY)

    def clear(self):
        self.openNodes = []
        self.closedNodes = []

    def constructMap(self):
        self.map = [[0 for i in range(Constant.WIDTH)] for i in range(Constant.HEIGHT)]

        for i in range(Constant.WIDTH):
            for j in range(Constant.HEIGHT):
                self.map[i][j] = grid(i,j)
                self.map[i][j].drawColor(self.screen, Color.BLACK)

    def VisualizeUI(self):
        root = Tk()
        root.title("Path Finding Visualizer Setting")
        root.geometry("630x210")

        instructLabel = Label(root, text = "Type in (x,y), where 0 <= x,y < 50")
        instructLabel.grid(row = 0, column = 1)
        startLabel = Label(root, text="Start",  font = ("Helvetica",12))
        startLabel.grid(row=1)
        startLabel.config(width=10)

        startInput = Entry(root, width=70)
        startInput.grid(row=1, column=1)

        startEXLabel = Label(root,text = "EX: (1,1)", font = ("Helvetica",8))
        startEXLabel.grid(row= 2, column=1)

        endLabel = Label(root, text="Target", font=("Helvetica", 12))
        endLabel.grid(row=3)
        endLabel.config(width = 10)

        endInput = Entry(root, width=70)
        endInput.grid(row=3, column=1)

        endEXLabel = Label(root, text="EX: (49,49)", font=("Helvetica", 8))
        endEXLabel.grid(row=4, column=1)

        algorithmLabel = Label(root,text = "Algorithm: ", font = ("Helvetica",10))
        algorithmLabel.grid(row= 5, column=0)

        self.algorithmType = StringVar(None,"A*")
        for text,value,x,y in self.Algorithms:
            algorithmButton = Radiobutton(root, text = text, variable = self.algorithmType, value = value)
            algorithmButton.place(x = x, y = y)

        visibleLabel = Label(root, text="Visibility: ", font=("Helvetica", 10))
        visibleLabel.grid(row=6, column=0, pady = 5)

        self.isPathVisible = BooleanVar()
        visibleCheckButton = Checkbutton(root, text = "Show Path", variable = self.isPathVisible, onvalue = 1, offvalue = 0)
        visibleCheckButton.grid(row = 6, column = 1, pady = 5)



        showButton = Button(root, text="Show", command=lambda: self.submitInput(root,startInput, endInput),
                            font=("Helvetica", 10), width=8, height=1)
        showButton.place(x = 400, y = 165)

        exitButton = Button(root, text="Exit", command= quit,  font = ("Helvetica", 10), width = 8, height = 1)
        exitButton.place(x = 500, y = 165)
        pygame.display.update()
        pygame.init()
        root.mainloop()

    def submitInput(self,root,e1,e2):
        i = 0
        j = 0
        startPoint = e1.get()
        targetPoint = e2.get()
        # Exception Handler
        if not "," in startPoint:
            messagebox.showwarning(title='Error!', message='Please type in number seperated by comma')
        elif (int(startPoint.split(',')[0]) < 0 or int(startPoint.split(',')[1]) < 0):
            messagebox.showwarning(title='Error!', message='Please type in non negative number')
        elif (int(startPoint.split(',')[0]) >= Constant.WIDTH or int(startPoint.split(',')[1]) >= Constant.HEIGHT):
            messagebox.showwarning(title='Error!', message='Number exceeds limit (limit: x:50,y:50)')

        if not "," in targetPoint:
            messagebox.showwarning(title='Error!', message='Please type in number seperated by comma')
        elif (int(targetPoint.split(',')[0]) < 0 or int(targetPoint.split(',')[1]) < 0):
            messagebox.showwarning(title='Error!', message='Please type in non negative number')
        elif (int(targetPoint.split(',')[0]) >= Constant.WIDTH or int(targetPoint.split(',')[1]) >= Constant.HEIGHT):
            messagebox.showwarning(title='Error!', message='Number exceeds limit (limit: x:50,y:50)')

        # Accepted Input
        else:
            i = int(startPoint.split(',')[0])
            j = int(startPoint.split(',')[1])
            self.startGrid = self.map[i][j]
            self.startGrid.drawColor(self.screen, Color.LIME)

            i = int(targetPoint.split(',')[0])
            j = int(targetPoint.split(',')[1])
            self.targetGrid = self.map[i][j]
            self.targetGrid.drawColor(self.screen, Color.LIME)
            pygame.display.update()
            root.wm_withdraw()
            root.destroy()

    def listenConfiguration(self):
        running = True
        try:
            while running:
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        running = False
                        pygame.quit()
                        sys.exit()
                        break

                    elif e.type == pygame.KEYDOWN:
                        if e.key == pygame.K_SPACE:
                            running = False
                            break

                    elif pygame.mouse.get_pressed()[0]:
                        mx, my = pygame.mouse.get_pos()
                        mx = int((mx - 25) / 11)
                        my = int((my - 25) / 11)
                        if mx + 1 < Constant.WIDTH and my < Constant.HEIGHT:
                            self.map[mx][my].drawColor(self.screen, Color.WHITE)
                            self.map[mx][my].setWall()
                            self.map[mx + 1][my].drawColor(self.screen, Color.WHITE)
                            self.map[mx + 1][my].setWall()
                        pygame.display.update()
        except SystemExit:
            pygame.quit()

    def run(self):
        self.listenConfiguration()
        algorithm = self.algorithmType.get()
        if (algorithm == "A*"):
            AStarAlgorithm = AStar(self.map,self.startGrid,self.targetGrid,self.isPathVisible,self.screen)
            return AStarAlgorithm.run()

        elif (algorithm == "BFS"):
            BFSAlgorithm = BFS(self.map,self.startGrid,self.targetGrid,self.isPathVisible,self.screen)
            return BFSAlgorithm.run()

        elif (algorithm == "DFS"):
            DFSAlgorithm = DFS(self.map, self.startGrid, self.targetGrid, self.isPathVisible,self.screen)
            return DFSAlgorithm.run()

        elif (algorithm == "Dijkstra"):
            DijkstraAlgorithm = Dijkstra(self.map, self.startGrid, self.targetGrid, self.isPathVisible,self.screen)
            return DijkstraAlgorithm.run()

        else:
            return