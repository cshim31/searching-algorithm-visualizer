from Grid import Grid as grid
import Constant, Color
import math
import sys,pygame
import time
from tkinter import *
from tkinter import messagebox, Frame, Menu, ttk

class Map:
    def __init__(self):
        self.openNodes = []
        self.closedNodes = []
        self.map = []
        self.currentGrid = None
        self.startGrid = None
        self.targetGrid = None
        self.time = None
        self.isPathVisible = None
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
        #create neighbor
        for i in range(Constant.HEIGHT):
            for j in range(Constant.WIDTH):
                self.map[i][j].appendNeighbor(self.map)

    def findHCost(self,grid):
        return math.sqrt((grid.x-self.targetGrid.x)**2+(grid.y-self.targetGrid.y)**2)

    def validateDiagonality(self,currentGrid, neighborGrid):
        distance = math.sqrt((currentGrid.x - neighborGrid.x) ** 2 + (currentGrid.y - neighborGrid.y) ** 2)
        if distance > 1:
            return True
        return False

    def VisualizeUI(self):
        root = Tk()
        root.title("Path Finding Visualizer")
        root.geometry("400x150")
        startLabel = Label(root, text="Start",  font = ("Helvetica",12))
        startLabel.grid(row=0)
        startLabel.config(width=10)

        endLabel = Label(root, text="Target", font=("Helvetica", 12))
        endLabel.grid(row=1)
        endLabel.config(width = 10)

        startInput = Entry(root, width = 40)
        startInput.grid(row=0, column=1)
        endInput = Entry(root, width = 40)
        endInput.grid(row=1, column=1)

        self.isPathVisible = BooleanVar()
        visibleCheckButton = Checkbutton(root, text = "Show Path", variable = self.isPathVisible, onvalue = 1, offvalue = 0)
        visibleCheckButton.grid(row = 3, column = 1)

        showButton = Button(root, text="Show", command=lambda: self.submitInput(root, startInput, endInput),
                            font=("Helvetica", 10), width=8, height=1)
        showButton.place(x = 150, y = 85)
        exitButton = Button(root, text="Exit", command=lambda: quit,  font = ("Helvetica", 10), width = 8, height = 1)
        exitButton.place(x = 250, y = 85)

        pygame.display.update()
        pygame.init()
        root.mainloop()
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
                        mx = int(mx / 12)
                        my = int(my / 12)
                        if mx is not self.targetGrid.x and my is not self.targetGrid.y:
                            self.map[mx][my].drawColor(self.screen, Color.WHITE)
                            self.map[mx][my].setWall()
                        pygame.display.update()
        except SystemExit:
            pygame.quit()
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
            root.destroy()
            self.setup()

    def setup(self):
        currentGrid = self.startGrid
        self.closedNodes.append(currentGrid)
        neighbors = currentGrid.neighbor[:]
        for i in range(len(neighbors)):
            isDiagonal = self.validateDiagonality(currentGrid, neighbors[i])
            distance = self.findHCost(neighbors[i])
            neighbors[i].updateCost(distance, currentGrid.g_cost, isDiagonal)
            self.openNodes.append(neighbors[i])

    def excludeWall(self, neighbors):
        i = 0
        while i < len(neighbors):
            if neighbors[i].isWall:
                del neighbors[i]
                i-=1
            i+=1
        return neighbors

    def run(self):
        running = True
        self.time = time.time()
        while (running):
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

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

                while currentGrid != None:
                    currentGrid.drawColor(self.screen, Color.LIME)
                    pygame.display.update()
                    currentGrid = currentGrid.parent

                timeTaken = time.time() - self.time
                status = messagebox.askokcancel(title="Done!", message =  "Program has taken " + str(timeTaken) + " \nWould you like to continue?")
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
                    if isDiagonal :
                        if neighbors[i].g_cost > (currentGrid.g_cost + currentGrid.diagonalWeight):
                            print("updating cost from ", neighbors[i].g_cost, " to ", currentGrid.g_cost + currentGrid.diagonalWeight)
                            distance = self.findHCost(neighbors[i])
                            neighbors[i].updateCost(distance, currentGrid.g_cost, isDiagonal)
                            neighbors[i].setParent(currentGrid)

                    if not isDiagonal :
                         if neighbors[i].g_cost > (currentGrid.g_cost + currentGrid.weight):
                            print("updating cost from ", neighbors[i].g_cost, " to ", currentGrid.g_cost + currentGrid.weight)
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