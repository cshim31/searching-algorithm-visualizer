from Map import Map


from tkinter import *
from tkinter import messagebox, Frame, Menu, ttk
#from tkinter import messagebox
#execute program
def main():
    running = True
    while(running):
        map = Map()
        map.constructMap()
        map.VisualizeUI()
        running = map.run()

if __name__ == "__main__":
    main()
