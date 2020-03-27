from Grid import Grid as tile

import math
import sys,pygame
from tkinter import *
from tkinter import messagebox, Frame, Menu, ttk
#from tkinter import messagebox

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
yellow = (255,255,0)
lime = (0,255,0)
blue = (0,0,255)
skyblue = (0,204,255)
black = (0,0,0)
white = (255,255,255)
screen = None

#I/O peripheral
e1 = None
e2 = None
root = None
# construct the map
def construct(openNodes,closedNodes):
    global map
    global width, height

    map = [0 for i in range(width)]
    for i in range(width):
        map[i] = [0 for i in range(height)]

    for i in range(width):
        for j in range(height):
            map[i][j] = tile(i,j)
            map[i][j].reset()
    clear()

    #create neighbor
    for i in range(height):
        for j in range(width):
            map[i][j].append_neighbor(map,width,height)

    # default start and end
    global current, start, end

    start = map[0][0]
    end = map[49][49]

def setup():

    global current,start
    global closedNodes,openNodes
    current = start
    closedNodes.append(current)
    neighbors = current.neighbor
    for i in range(len(neighbors)):
        distance = Diagonal_distance(neighbors[i])
        neighbors[i].updateDistance(distance, current.g_cost)
        openNodes.append(neighbors[i])

def clear():
    global openNodes
    global closedNodes
    openNodes = []
    closedNodes = []

def Diagonal_distance(tile):
    global end
    return math.sqrt((tile.x-end.x)**2+(tile.y-end.y)**2)

def show():
    global map
    global start,end
    global e1,e2
    i = 0
    j = 0

        #Exception Handler
    if not "," in e1.get():
        messagebox.showwarning(title='Error!', message='Please type in number seperated by comma')
    elif(int(e1.get().split(',')[0])<0 or int(e1.get().split(',')[1])<0):
        messagebox.showwarning(title='Error!', message='Please type in non negative number')
    elif(int(e1.get().split(',')[0])>=50 or int(e1.get().split(',')[1])>=50):
        messagebox.showwarning(title='Error!', message='Number exceeds limit (limit: x:50,y:50)')
    #Exception Handler
    elif not "," in e2.get():
        messagebox.showwarning(title='Error!', message='Please type in number seperated by comma')
    elif(int(e2.get().split(',')[0])<0 or int(e2.get().split(',')[1])<0):
        messagebox.showwarning(title='Error!', message='Please type in non negative number')
    elif (int(e2.get().split(',')[0]) >= 50 or int(e2.get().split(',')[1]) >= 50):
        messagebox.showwarning(title='Error!', message='Number exceeds limit (limit: x:50,y:50)')
    else:
        i = int(e1.get().split(',')[0])
        j = int(e1.get().split(',')[1])
        start = map[i][j]
        start.drawColor(screen,red,width,height)

        i = int(e2.get().split(',')[0])
        j = int(e2.get().split(',')[1])
        end = map[i][j]
        end.drawColor(screen,red,width,height)
        root.quit
        pygame.display.update()
        setup()

def user_interface():
    # initial graphic setting
    global map
    global width, height
    global screen
    global e1,e2,root

    screen = pygame.display.set_mode((600, 600))
    screen.fill(white)
    pygame.display.update()

    root = Tk()
    Label(root, text="Start Node").grid(row=0)
    Label(root, text="End Node").grid(row=1)

    e1 = Entry(root)
    e2 = Entry(root)
    e1.grid(row=0,column=1)
    e2.grid(row=1,column=1)

    Button(root,text="Show",command=show).grid(row=3,column=1)
    Button(root, text="Exit", command=quit).grid(row=3, column=0)

    root.mainloop()
    pygame.init()
    running = True

    while(running):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                running = False
                break

            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    running = False
                    break

            elif pygame.mouse.get_pressed()[0]:
                mx,my = pygame.mouse.get_pos()
                mx= int(mx/12)
                my = int(my/12)
                print(mx,my)
                map[mx][my].drawColor(screen,black,width,height)
                map[mx][my].setWall()
                pygame.display.update()


def run(openNodes,closedNodes):
    running = True
    while(running):
        global map
        global width, height
        global current, start, end
        global screen

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        # target found
        if current is end:
            # print("Printing path nodes")
            # print("Parent: (",current.x,",",current.y,")")
            current = current.parent
            while current != None:
                current.drawColor(screen, blue, width, height)
                pygame.display.update()
                current = current.parent

            status = messagebox.askokcancel(title="Done!", message="Would you like to continue?")
            if status:
                running = False
                return True
            else:
                pygame.quit()
                sys.exit()
                return False

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
        print("Node: (",current.x,",",current.y,")")

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
            if(openNodes[i].is_Wall) :
                continue
            if(openNodes[i] is end):
                continue
            openNodes[i].drawColor(screen,black,width,height)
        for i in range(len(closedNodes)):
            if (closedNodes[i].is_Wall):
                continue
            if (closedNodes[i] is start):
                continue
            closedNodes[i].drawColor(screen,yellow,width,height)
        pygame.display.update()


#execute program
def main():
    running = True

    while(running):
        construct(openNodes, closedNodes)
        user_interface()
        running = run(openNodes,closedNodes)

if __name__ == "__main__":
    main()
