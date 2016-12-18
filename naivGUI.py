from __future__ import print_function
from PIL import ImageTk
from pygments.formatters import img
from tkinter import *
from tkinter import ttk
import math
import scipy.io as sio
import sys
import numpy
from math import hypot
import _tkinter



def getPath(*args):
    flag = 0
    newV = []
    goTo = []
    temp = []
    final = []
    newV = []
    trucks = []
    inks = []
    source=0
    v = [['0', 0, 0], ['1', 2, 4], ['2', -3, 2], ['3', 5, -8], ['4', 6, 1], ['5', 6, 5], ['6', 10, 2], ['7', -4, 6],
         ['8', -5, -5], ['9', -1, -3], ['10', 10, -5]]
    newV.append(v[0])
    k=channels.get()
    try:
        int(k)
    except:
        return paths.set('Channels can be only a positive number,\n please try again!')
    if(int(k)<=0):
        return paths.set('Channels can be only a positive number,\n please try again!')
    else:
        if(p1.get()==1):goTo.append(v[1][0])
        if(p2.get()==1):goTo.append(v[2][0])
        if(p3.get()==1):goTo.append(v[3][0])
        if(p4.get()==1):goTo.append(v[4][0])
        if(p5.get()==1):goTo.append(v[5][0])
        if(p6.get()==1):goTo.append(v[6][0])
        if(p7.get()==1):goTo.append(v[7][0])
        if(p8.get()==1):goTo.append(v[8][0])
        if(p9.get()==1):goTo.append(v[9][0])
        if(p10.get()==1):goTo.append(v[10][0])
        if(len(goTo)==0):return paths.set('You should choose at least one vertex,\n please try again!')

    #print(goTo)
    k=int(k)
    max = 0
    path = [['0' for x in range(1)] for y in range(k)]
    #print(path)
    for x in goTo:
        for y in v:
            if y[0] == x:
                newV.append(y)
    #print("nexV",newV)
    for x in newV:
        temp = []
        for y in newV:
            dis = math.hypot(x[1] - y[1], x[2] - y[2])
            temp.append(dis)
            if(dis > max):
                max = dis
        final.append(temp)
    #print("Final", final)
    for x in final:
        print(x)
    trucks = numpy.zeros(k)
    #print("Trucks", trucks)

    for x in goTo:
        inks.append(x)
    k = len(goTo)
    print(goTo)

    while k != 0:
        i = 0
        for x in trucks:
            print(i)
            min = max
            for y in goTo:
                place = inks.index(y) + 1  # index of the next v
                dis = final[int(x)][int(place)]  # distnation fron place to next v.
                if dis <= min:
                    min = dis
                    nextV = y
                    nextIndex = place
            print("The next V is:", nextV, " And the index it's:", nextIndex);
            source=source+min;
            path[i].append(nextV)
            if len(goTo) != 1:
                goTo.remove(nextV)
                trucks[i] = nextIndex
                i = i + 1
                k = len(goTo)
            else:
                trucks[i] = nextIndex
                flag = 1
                break
        if flag == 1:
            break

    print(path)
    #print(trucks)
    paths.set(path)


root = Tk()
root.title("Optimal Paths")

mainframe = ttk.Frame(root, padding="10 10 10 10")
mainframe.grid(column=10, row=10, sticky=(N, W, E, S))
mainframe.columnconfigure(10, weight=10)
mainframe.rowconfigure(10, weight=10)

channels= StringVar()
paths = StringVar()

feet_entry = ttk.Entry(mainframe, width=10, textvariable=channels)
feet_entry.grid(column=2, row=1, sticky=(W, E))
ttk.Label(mainframe, textvariable=paths).grid(column=2, row=2, sticky=N)
ttk.Button(mainframe, text="Get Paths", command=getPath).grid(column=3, row=12, sticky=W)


ttk.Label(mainframe, text="channels").grid(column=3, row=1, sticky=W)

p1 = IntVar()
p2 = IntVar()
p3 = IntVar()
p4 = IntVar()
p5 = IntVar()
p6 = IntVar()
p7 = IntVar()
p8 = IntVar()
p9 = IntVar()
p10 = IntVar()
ttk.Checkbutton(mainframe, text="1 (2,4)", variable=p1).grid(row=5, column=2, sticky=W)
ttk.Checkbutton(mainframe, text="2 (-3,2)", variable=p2).grid(row=5, column=3, sticky=W)
ttk.Checkbutton(mainframe, text="3 (5,-8)", variable=p3).grid(row=6, column=2, sticky=W)
ttk.Checkbutton(mainframe, text="4 (6,1)", variable=p4).grid(row=6, column=3, sticky=W)
ttk.Checkbutton(mainframe, text="5 (6,5)", variable=p5).grid(row=7, column=2, sticky=W)
ttk.Checkbutton(mainframe, text="6 (10,2)", variable=p6).grid(row=7, column=3, sticky=W)
ttk.Checkbutton(mainframe, text="7 (-4,6)", variable=p7).grid(row=8, column=2, sticky=W)
ttk.Checkbutton(mainframe, text="8 (-5,-5)", variable=p8).grid(row=8, column=3, sticky=W)
ttk.Checkbutton(mainframe, text="9 (-1,-3)", variable=p9).grid(row=9, column=2, sticky=W)
ttk.Checkbutton(mainframe, text="10 (10,-5)", variable=p10).grid(row=9, column=3, sticky=W)

for child in mainframe.winfo_children(): child.grid_configure(padx=8, pady=8)

feet_entry.focus()
root.bind('<Return>', getPath)

root.mainloop()