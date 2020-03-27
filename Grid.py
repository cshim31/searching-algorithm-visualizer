import sys,pygame
<<<<<<< HEAD
from tkinter import messagebox

#initial graphic setting
pygame.init()
screen = pygame.display.set_mode((600,600))
screen.fill((255,255,255))
#data variables
width = 50
height = 50
openNodes = []
closedNodes = []
map = []

current = None
start = None
end = None

#graphic variables
red = (255,0,0)
lime = (0,255,0)
blue = (0,0,255)
black = (0,0,0)
whilte = (255,255,255)
=======

INFINITY = 100000000
>>>>>>> Updated

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

<<<<<<< HEAD
=======

>>>>>>> Updated

    #h_cost = distance between target and object
    #g_cost = distance between origin and object
    #f_cost = h_cost + g_cost
    def updateDistance(self,h_cost,g_cost):
        self.h_cost = h_cost
        self.g_cost = g_cost+self.weight
        self.f_cost = self.h_cost+self.g_cost

    def setParent(self,parent):
        self.parent = parent

<<<<<<< HEAD
    def drawColor(self,color):
=======
    def drawColor(self,screen,color,width,height):
>>>>>>> Updated
        pygame.draw.rect(screen,color,(self.x*12,self.y*12,600/width,600/height))

    def setWall(self):
        self.is_Wall = True
        self.weight = INFINITY

<<<<<<< HEAD
# construct the map
map = [0 for i in range(width)]
for i in range(width):
    map[i] = [0 for i in range(height)]

for i in range(width):
    for j in range(height):
        map[i][j] = Grid(i,j)
     #   map[i][j].setColor(black)
#create neighbor
for i in range(height):
    for j in range(width):
        map[i][j].append_neighbor(map)

# define start and end
start = map[2][2]
end = map[49][1]

#Distance to target
def Diagonal_distance(obj):
    return math.sqrt((obj.x-end.x)**2+(obj.y-end.y)**2)

#Initialization
current = start
closedNodes.append(current)
neighbors = current.neighbor
for i in range(len(neighbors)):
    distance = Diagonal_distance(neighbors[i])
    neighbors[i].updateDistance(distance,current.g_cost)
    openNodes.append(neighbors[i])
      #  show()

for event in pygame.event.get():
    if event.type == pygame.QUIT: sys.exit()


def run():
    while(True):
        #find smallest f_cost grid
        index = 0
        for i in range(len(openNodes)):
            if openNodes[index].f_cost>openNodes[i].f_cost:
                index = i
            #find smallest g_cost grid when multiple same f_cost grid exists
            if openNodes[index].f_cost == openNodes[i].f_cost:
                if openNodes[index].h_cost>openNodes[i].h_cost:
                    index = i
        current = openNodes[index]
        openNodes.remove(current)
        closedNodes.append(current)
        print("(",current.x,",",current.y,")")

        #target found
        if current is end:
            while current.parent:
                current.drawColor(blue)
                pygame.display.update()
                current = current.parent
            messagebox.askokcancel('done')
            break

        neighbors = current.neighbor
        #update cost of neighbor grids
        for i in range(len(neighbors)):
            if neighbors[i] in closedNodes:
                continue

            #not in openNode
            if neighbors[i] not in openNodes:
                distance = Diagonal_distance(neighbors[i])
                neighbors[i].updateDistance(distance, current.g_cost)
                openNodes.append(neighbors[i])
                neighbors[i].setParent(current)

            #Already in openNode
            if neighbors[i].g_cost>(current.g_cost+current.weight):
                distance = Diagonal_distance(neighbors[i])
                neighbors[i].updateDistance(distance, current.g_cost)
                neighbors[i].setParent(current)


        #graphic
        for i in range(len(openNodes)):
            openNodes[i].drawColor(lime)
        for i in range(len(closedNodes)):
            closedNodes[i].drawColor(red)
        end.drawColor(black)
        pygame.display.update()
#execute program
def main():
    run()
main()

    #def show():
=======
    def reset(self):
        self.h_cost = 0
        self.g_cost = 0
        self.f_cost = 0
        self.weight = 10
        self.neighbor = []
        self.parent = None
        self.color = 0
        self.is_Wall = False
>>>>>>> Updated
