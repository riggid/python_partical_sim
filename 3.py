import os, time, math, sys
import time
import math

##def prnt(x,y,h):                      #old code to print
##    print('\n'*int((h - y)),end='') 
##    print(" "*int(x) + '*')

def circleBres(xc,yc,r,lst):
    x,y = 0,r
    d = 3 - 2 * r
    drawCircle(xc, yc, x, y, lst)
    while (y >= x):
        # // for each pixel we will
        # // draw all eight pixels

        x+=1

        #  check for decision parameter
        #  and correspondingly
        #  update d, x, y
        if (d > 0):
            y-=1
            d = d + 4 * (x - y) + 10

        else:
            d = d + 4 * x + 6
        drawCircle(xc, yc, x, y,lst)

def drawCircle(xc, yc ,x, y,lstname):
    lst = []
    lst.append([xc+x, yc+y]) 
    lst.append([xc-x, yc+y])
    lst.append([xc+x, yc-y])
    lst.append([xc-x, yc-y])
    lst.append([xc+y, yc+x])
    lst.append([xc-y, yc+x])
    lst.append([xc+y, yc-x])
    lst.append([xc-y, yc-x])
    res = [list(t) for t in set(tuple(element) for element in lst)]
    for i in res:
        lstname.append(i)

def get_line(start, end):

    # Setup initial conditions
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1

    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)

    # Rotate line
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    # Swap start and end points if necessary and store swap state
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
    # Reverse the list if the coordinates were swapped
    if swapped:
        swapped = True

    # Recalculate differentials
    dx = x2 - x1
    dy = y2 - y1

    # Calculate error
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1

    # Iterate over bounding box generating points between start and end
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = [y, x] if is_steep else [x, y]
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx

    # Reverse the list if the coordinates were swapped
    if swapped:
        points.reverse()
    return points

def insertion(vertices,lines,triangles,rectangles,circles):      
    for i in range(0,len(triangles),3):
        lines.append(vertices[triangles[i]])
        lines.append(vertices[triangles[i+2]])
        for j in range(2):
            lines.append(vertices[triangles[i+j]])
            lines.append(vertices[triangles[i+j+1]])

    for i in range(0,len(rectangles),4):
        lines.append(vertices[rectangles[i]])
        lines.append(vertices[rectangles[i+3]])
        for j in range(3):
            lines.append(vertices[rectangles[i+j]])
            lines.append(vertices[rectangles[i+j+1]])

    for i in range(0,len(lines),2):
        start = lines[i][0],lines[i][1]
        end = lines[i+1][0],lines[i+1][1]
        cline = get_line(start,end)
        for i in cline:
            PoP.append(i)
            VoP.append([10,10])
            state.append('static')

    for i in range(0,len(circles),3):
        circleBres(circles[i],circles[i+1],circles[i+2],PoP)
            
        for i in range(len(PoP)-len(VoP)):
            VoP.append([10,10])
            state.append('dynamic')

def PositionUpdate(pos,vel,acc,dt):
            vel[0] += acc[0] * dt
            vel[1] += acc[1] * dt
            pos[0] += vel[0] * dt                                                       # Change postion in x direction
            pos[1] += vel[1] * dt                                                       # in y direction
            if (pos[1] > b-1 or pos[1] <= 1):
                vel[1] = -vel[1]
    ##          state[i] = 'static'
    ##        if(pos[1] > b-3 or pos[1] < 2):
    ##            char = ' _ '
            if(pos[0]*2 > l-3 or pos[0] < 2):
                vel[0] = -vel[0]





# Settings

l = 90 #effective length is half(45) 
b = 30
a = b/l
maxh = 29
char = "."
t1 = time.time()
dt = 0.0
lastFrame = 0.0
svel,shig = 0,0
rvel = [10,10]
framecount = 0
PoP,VoP,state,aa,grid,lines = [],[],[],[],[],[]


vertices =[
    # A0     B1    C2     D3      E4    F5      G6      H7   
    
        [1,1],[45,1],[45,29],[1,29]
    ]
triangles = []


rectangles = [
              0,1,2,3  
    ]


circles = [
            5,5,3
]

insertion(vertices,lines,triangles,rectangles,circles)

grid = [[' ' for x in range(l)] for y in range(b)]
hit = False

timer = 0

while(1):
    currentFrame = time.time() - t1
    dt = currentFrame - lastFrame
    lastFrame = currentFrame
    timer += dt
    for i in range(len(PoP)):
        acc = [0,0]
        if state[i] == 'dynamic':
            PositionUpdate(PoP[i],VoP[i],acc,dt)
        elif state[i] == 'static':
            pass
        else:
            PositionUpdate(PoP[i],VoP[i],acc,dt)
    
        x = int(PoP[i][0]-1) 
        y = int(b-PoP[i][1]-1)
        grid[y][2*x] = char
        aa.append([2*x,y])

    if timer > 0.1:
        timer = 0.0
        for row in grid:
            print(''.join(row))

    for i in range(0,len(aa)):
        x = aa[i][0]
        y = aa[i][1]
        grid[y][x] = ' '
    inPoS = []
    aa = []

##    char = '.'

    