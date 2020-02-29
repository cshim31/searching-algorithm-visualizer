import math
import sys,pygame
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

    def append_neighbor(self, map):
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
        #diagonal
   #     if self.x-1>=0 and self.y-1>=0:
   #         self.neighbor.append(map[self.x - 1][self.y-1])
   #     if self.x+1<width and self.y+1<height:
   #         self.neighbor.append(map[self.x - 1][self.y-1])

    #h_cost = distance between target and object
    #g_cost = distance between origin and object
    #f_cost = h_cost + g_cost
    def updateDistance(self,h_cost,g_cost):
        self.h_cost = h_cost
        self.g_cost = g_cost+self.weight
        self.f_cost = self.h_cost+self.g_cost

    def setParent(self,parent):
        self.parent = parent



width = 50
height = 50
openNodes = []
closedNodes = []
map = [0 for i in range(width)]
for i in range(width):
    map[i] = [0 for i in range(height)]

current = None
start = None
end = None

    # constructure map
for i in range(width):
    for j in range(height):
        map[i][j] = Grid(i,j)

        #create neighbor
for i in range(height):
    for j in range(width):
        map[i][j].append_neighbor(map)

        # define start and end
start = map[2][2]
end = map[49][49]

def Diagonal_distance(obj):
    return math.sqrt((obj.x-end.x)**2+(obj.y-end.y)**2)
        #set up the data
closedNodes.append(start)
current = start
neighbors = current.neighbor
for i in range(len(neighbors)):
    distance = Diagonal_distance(neighbors[i])
    neighbors[i].updateDistance(distance,current.g_cost)
    openNodes.append(neighbors[i])
      #  show()

    #return shortest distance to target

def graphic():
    size = w,h = 1000,1000
    pygame.init()
    screen = pygame.display.set_mode(size)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

def run():
    while(True):
        #find smallest f_cost grid
        graphic()
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
            break
        neighbors = current.neighbor
        #update cost of neighbor grids
        for i in range(len(neighbors)):
            if neighbors[i] in closedNodes:
                continue
            if neighbors[i].g_cost>(current.g_cost+current.weight):
                distance = Diagonal_distance(neighbors[i])
                neighbors[i].updateDistance(distance, current.g_cost)
                neighbors[i].setParent(current)
            if neighbors[i] not in openNodes:
                openNodes.append(neighbors[i])
#execute program
def main():
    run()
main()

    #def show():

