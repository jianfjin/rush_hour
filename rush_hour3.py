
# coding: utf-8

# In[3]:

import random
import pygame, sys, time
from pygame.locals import *

class Square(object):
    def __init__(self, index):
        self.index = index
        self.x = index % 6
        self.y = index / 6
        self.occupied = False
        self.car = None
    
    def __repr__(self):
        return 'square ' + str(self.index)
    
    def get_left(self, squares):
        """ get the square in the left """
        if self.x > 0:
            return squares[self.index - 1]
        else:
            return False
        
    def get_right(self, squares):
        """ get the square in the left """
        if self.x < 5:
            return squares[self.index + 1]
        else:
            return False
        
    def get_up(self, squares):
        """ get the square above """
        if self.y > 0:
            return squares[self.index - 6]
        else:
            return False
    
    def get_down(self, squares):
        """ get the square below """
        if self.y < 5:
            return squares[self.index + 6]
        else:
            return False

class Car(object):
    def __init__(self, name, x, y, width, height, orient):
        self.name = name
        self.x = x
        self.y = y
        self.head_x = None
        self.tail_x = None
        self.head_y = None
        self.tail_y = None
        self.width = width
        self.height = height
        self.orient = orient
        self.square = []
        self.freedom_left = 0
        self.freedom_right = 0
        self.freedom_up = 0
        self.freedom_down = 0
        self.head_square = None
        self.tail_square = None
        self.head = None
        self.tail = None
        
    def __repr__(self):
        return self.name
    
    def get_squares(self, squares):
        """get the squares occupied by the car"""
        if self.orient == 'h':
            # car is horizontal
            for x in xrange(self.x, self.x + self.width):
                # get the index of the occupied square
                index = x + self.y * 6
                self.square.append(squares[index])
                squares[index].occupied = True
                squares[index].car = self.name
        elif self.orient == 'v':
            # car is vertical
            for y in xrange(self.y, self.y + self.height):
                # get the index of the occupied square
                index = self.x + y * 6
                self.square.append(squares[index])
                squares[index].occupied = True
                squares[index].car = self.name
    
    def clear_squares(self, squares):
        """clear the squares after moving the car"""
        if self.orient == 'h':
            # car is horizontal
            for x in xrange(self.x, self.x + self.width):
                # get the index of the occupied square
                index = x + self.y * 6
                squares[index].occupied = False
                squares[index].car = None
        elif self.orient == 'v':
            # car is vertical
            for y in xrange(self.y, self.y + self.height):
                # get the index of the occupied square
                index = self.x + y * 6
                squares[index].occupied = False
                squares[index].car = None
        
    def get_head_tail(self, squares):    
        """ set the head and tail of the car """
        self.head = self.square[-1]
        self.tail = self.square[0]
        if self.orient == 'h':
            self.head_x = self.x + self.width - 1
            self.tail_x = self.x
            self.head_y = self.y
            self.tail_y = self.y
        elif self.orient == 'v':
            self.head_x = self.x
            self.tail_x = self.x
            self.head_y = self.y + self.height - 1
            self.tail_y = self.y 
   
    def get_freedom(self,squares):
        """get the empty squares before and after the car"""
        #print self.name, self.square
        if self.orient == 'h':
            self.freedom_left = 0
            self.freedom_right = 0
        
            # next right squares to car
            next_right = self.head.get_right(squares)
            #print next_right
            # next right square empty    
            while next_right and not next_right.occupied:
                self.freedom_right += 1
                next_right = next_right.get_right(squares)
            
            # next squares left to car
            next_left = self.tail.get_left(squares)
            #print next_left.__repr__()
            #print next_left.occupied
            # next left square empty    
            while next_left and not next_left.occupied:
                self.freedom_left += 1
                next_left = next_left.get_left(squares)
                #print next_left.__repr__()

        if self.orient == 'v':
            self.freedom_up = 0
            self.freedom_down = 0
            # next squares above car
            next_up = self.tail.get_up(squares)
            #print next_up, next_up.occupied
            while next_up and not next_up.occupied:
                self.freedom_up += 1
                next_up = next_up.get_up(squares)
            #print self.freedom_up
            # next squares below car
            next_down = self.head.get_down(squares)
            #print next_down
            while next_down and not next_down.occupied:
                self.freedom_down += 1
                next_down = next_down.get_down(squares)
                
            
class Vertex:
    def __init__(self,key):
        self.id = key
        self.connectedTo = {}
        self.cars = []
        
    def addCar(self, cars):
        # hold current configuration of all cars
        for car in cars:
            tempCar = Car(car.name, car.x, car.y, car.width, car.height, car.orient)
            self.cars.append(tempCar)

    def addNeighbor(self,nbr,dist):
        # connect to a neighbor vertex
        self.connectedTo[nbr] = dist

    def __str__(self):
        return str(self.id) + ' connectedTo: ' + str([x.id for x in self.connectedTo])

    def getConnections(self):
        return self.connectedTo.keys()

    def getId(self):
        return self.id

    def getDist(self,nbr):
        # calculate the distance between two vertices
        dist = 0
        for i in xrange(len(self.cars)):
            if self.cars[i].orient == 'h':
                #print i, self.cars[i].name, nbr.cars[i].name
                dist += abs(self.cars[i].x - nbr.cars[i].x)
            elif self.cars[i].orient == 'v':
                dist += abs(self.cars[i].y - nbr.cars[i].y)
        return dist
    
    def getWeight(self,nbr):
        return self.connectedTo[nbr]

class Graph:
    def __init__(self):
        self.vertList = {}
        self.numVertices = 0

    def addVertex(self,key):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key)
        self.vertList[key] = newVertex
        return newVertex

    def getVertex(self,n):
        if n in self.vertList:
            return self.vertList[n]
        else:
            return None

    def __contains__(self,n):
        return n in self.vertList

    def addEdge(self,f,t,dist=0):
        if f not in self.vertList:
            nv = self.addVertex(f)
        if t not in self.vertList:
            nv = self.addVertex(t)
        self.vertList[f].addNeighbor(self.vertList[t], dist)

    def getVertices(self):
        return self.vertList.keys()

    def __iter__(self):
        return iter(self.vertList.values())
    
def move_cars(squares, car_in_row, car_in_col, moves):
    """move all cars to random possible new positions"""
    for row in car_in_row:      
        #print car_in_row[row]
        for car in car_in_row[row]:
            car.get_freedom(squares)
            if car.width == 2:
                # available positions excluding current position    
                #print car.name, car.x, car.y, car.head, car.tail
                #print car.freedom_left, car.freedom_right
                pos_available = range(car.x - car.freedom_left, car.x + 1 + car.freedom_right)
                #print pos_available
                pos_available.remove(car.x)
                #print pos_available
                # new car.x
                if pos_available != []:
                    car.clear_squares(squares)
                    x = random.choice(pos_available)
                    # the squares occupied by car
                    index = x + car.y * 6
                    if squares[index].occupied == False and                     squares[index+1].occupied == False:
                        car.x = x
                        car.square = [squares[index], squares[index+1]]
                    car.get_head_tail(squares)    
                    car.get_squares(squares)
                    #print car.name, car.x, car.y

            elif car.width == 3:
                #print car.name, car.x
                #print car.freedom_left, car.freedom_right
                # available positions excluding current position
                pos_available = range(car.x - car.freedom_left, car.x + 1 + car.freedom_right)
                pos_available.remove(car.x)
                # new car.x
                if pos_available != []:
                    car.clear_squares(squares)
                    x = random.choice(pos_available)
                    # the squares occupied by car
                    index = x + car.y * 6
                    if squares[index].occupied == False and                     squares[index+1].occupied == False and                     squares[index+2].occupied == False:
                        
                        car.x = x
                        car.square = [squares[index], squares[index+1], squares[index+2]]
                    car.get_head_tail(squares)
                    car.get_squares(squares)
                    #print car.name, car.x, car.y
            moves.append((car.name, (car.x, car.y)))            
    for col in car_in_col:
        #print car_in_col[col]
        for car in car_in_col[col]:  
            car.get_freedom(squares)
            if car.height == 2:
                # available positions excluding current position                       
                #print car.name, car.x, car.y
                #print car.freedom_up, car.freedom_down
                pos_available = range(car.y - car.freedom_up, car.y + 1 + car.freedom_down)
                #print pos_available
                pos_available.remove(car.y)
                #print pos_available
                # new car.y
                if pos_available != []:
                    car.clear_squares(squares)
                    y = random.choice(pos_available)
                    # the squares occupied by car
                    index = car.x + y * 6
                    if squares[index].occupied == False and                     squares[index+6].occupied == False:
                        car.y = y
                        car.square = [squares[index], squares[index+6]]
                    car.get_head_tail(squares)
                    car.get_squares(squares)
                    #print car.name, car.x, car.y

            elif car.height == 3:
                # available positions excluding current position
                #print car.name, car.x, car.y, car.head, car.tail
                #print car.freedom_up, car.freedom_down
                pos_available = range(car.y - car.freedom_up, car.y + 1 + car.freedom_down)
                #print pos_available
                pos_available.remove(car.y)
                #print pos_available
                # new car.y
                if pos_available != []:
                    car.clear_squares(squares)
                    y = random.choice(pos_available)
                    #print y
                    # the squares occupied by car
                    index = car.x + y * 6
                    #print index
                    if squares[index].occupied == False and                     squares[index+6].occupied == False and                     squares[index+12].occupied == False:
                        car.y = y
                        car.square = [squares[index], squares[index+6], squares[index+12]]
                    car.get_head_tail(squares)    
                    car.get_squares(squares)
                    #print car.name, car.x, car.y
        moves.append((car.name, (car.x, car.y)))
        #return moves

def move_a_car(move, cars, squares):
    """move a car in one step"""
    car_name = move[0]
    for car in cars:
        if car.name == car_name:
            car.clear_squares(squares)
            car.x = move[1][0]
            car.y = move[1][1]                  
            car.square = []
            car.get_squares(squares)
            #print car.square
            #for square in car.square:
            #    print square.__repr__(), square.car, square.occupied
    
        
def get_dist(vertex1, vertex2):
    """get the distance between two graphs"""
    dist = 0
    for car in vertex2:
        if car.orient == 'h':
            dist += abs(vertex2[car].x - vertex1[car].x)
        if car.orient == 'v':
            dist += abs(vertex2[car].y - vertex1[car].y)

def checkWin(squares, R):
    """check the winning configuration"""
    occupied = 0
    for i in xrange(R.y*6, R.y*6+6):
        #print squares[i].index, squares[i].car, squares[i].occupied
        if squares[i].occupied:
            occupied += 1
      
    if occupied == 2:
        return True
    return False

def showCars(squares):
    for i in squares:
        if i % 6 < 5:
            print str(squares[i].car) + chr(9),
        elif i % 6 == 5:
            print str(squares[i].car) + ' \n'

def get_cars(cars):
    pos = {}
    for car in cars:
        x = car.x
        y = car.y
        name = car.name
        pos[name] = (x, y)
    return pos    

def bfs(s, g):
    """breadth first search"""
    level = {s:0}
    parent = {s:None}
    i = 1
    prev =[s]
    while prev:
        next = []
        for u in prev:
            for v in g.vertList[u].connectedTo:
                #print v.id
                if v.id not in level:
                    level[v.id] = i
                    parent[v.id] = u
                    next.append(v.id)
        prev = next
        i += 1
    return parent

def shortest_path(parent, source, target):    
    """get the shortest path of breadth-first search"""
    path = []
    while target != source:
        prev = parent[target]
        path.append(target)
        #parent.pop(target)
        target = prev
    path.append(target)    
    return path    
    
# initialize Graph
g = Graph()

# initialize 36 squares
squares = {}
for i in xrange(36):
    squares[i] = Square(i)  
    #print squares[i].__repr__()
    #print squares[i].x, squares[i].y

# initialize cars
A = Car('A', 4, 0, 2, 1, 'h')
B = Car('B', 2, 1, 2, 1, 'h')
C = Car('C', 4, 1, 2, 1, 'h')
E = Car('E', 4, 2, 1, 3, 'v')
F = Car('F', 5, 2, 1, 3, 'v')
G = Car('G', 0, 3, 2, 1, 'h')
H = Car('H', 2, 3, 2, 1, 'h')
I = Car('I', 3, 4, 1, 2, 'v')
J = Car('J', 4, 5, 2, 1, 'h')
R = Car('R', 1, 2, 2, 1, 'h')


# show the squares occupied by cars
cars = [A, B, C, E, F, G, H, I, J, R]
for car in cars:
    car.get_squares(squares)
    print car.__repr__()
    for square in car.square:
        print square.__repr__()
        print square.occupied
print 'Intialized \n'
showCars(squares)

# cars in each row and column
car_in_row = {}
car_in_col = {}
for car in cars:
    if car.orient == 'h':
        if car.y in car_in_row:
            car_in_row[car.y].append(car)
        else:
            car_in_row[car.y] = [car]
    elif car.orient == 'v':
        if car.x in car_in_col:
            car_in_col[car.x].append(car)
        else:
            car_in_col[car.x] = [car]
#print car_in_row
#print car_in_col
       
# status of squares in each row and column    
square_in_row = {}
square_in_col = {}
for i in squares:
    if squares[i].y in square_in_row:
        square_in_row[squares[i].y].append(squares[i])
    else:
        square_in_row[squares[i].y] = [squares[i]]
    if squares[i].x in square_in_col:
        square_in_col[squares[i].x].append(squares[i])
    else:
        square_in_col[squares[i].x] = [squares[i]]

# the head and tail position of each car        
for car in cars:
    car.get_head_tail(squares)

# move the cars randomly    

moves = []
status = checkWin(squares, R)
while not status:
    move_cars(squares, car_in_row, car_in_col, moves)
    status = checkWin(squares, R)
    #print status  
     
print 'Final\n'    
showCars(squares)    
print len(moves)

# initialize cars
newA = Car('A', 4, 0, 2, 1, 'h')
newB = Car('B', 2, 1, 2, 1, 'h')
newC = Car('C', 4, 1, 2, 1, 'h')
newE = Car('E', 4, 2, 1, 3, 'v')
newF = Car('F', 5, 2, 1, 3, 'v')
newG = Car('G', 0, 3, 2, 1, 'h')
newH = Car('H', 2, 3, 2, 1, 'h')
newI = Car('I', 3, 4, 1, 2, 'v')
newJ = Car('J', 4, 5, 2, 1, 'h')
newR = Car('R', 1, 2, 2, 1, 'h')

newCars = [newA, newB, newC, newE, newF, newG, newH, newI, newJ, newR]
# for car in newCars:
#     print car.name, car.x, car.y, car.orient
    
# the first vertex is the initial positions of the cars
v = {}
g.addVertex(0)
v[0] = g.getVertex(0)
v[0].addCar(newCars)
# for index in xrange(len(v[0].cars)):
#     print index, v[0].cars[index].name, v[0].cars[index].x, v[0].cars[index].y
    

newSquares = {}
for i in xrange(36):
    newSquares[i] = Square(i)  
    #print newSquares[i].__repr__(), newSquares[i].occupied

for car in newCars:
    car.clear_squares(newSquares)
    car.get_squares(newSquares)
#showCars(newSquares)

k  = 1
for move in moves:
    #print move
    v[k] = g.addVertex(k)  
    move_a_car(move, newCars, newSquares)
    v[k].addCar(newCars)
    #print k
    #showCars(newSquares)
    k += 1   
print k-1 

# connect the vertices to the nearest neighbors
for i in xrange(len(v) - 1):
    nbr = {}
    for j in xrange(i+1, len(v)):
        dist = v[i].getDist(v[j])
        #v[i].addNeighbor(v[j], dist)
        if j not in nbr:
            nbr[j] = dist
            #print j, nbr[j]
    minDist = min(nbr.values())    
    for k in nbr:     
        if nbr[k] == minDist:
            #print k
            g.addEdge(i, k, nbr[k])
            #print i, k, nbr[k]

#s = dijkstra(g, 0, k-1)
#print s
parent = bfs(0, g)
path = shortest_path(parent, 0, len(v)-1)
print path
print len(path)

# show the shortest path
sqrs = {}
crs = {}
carPos = {}
for k in path[::-1]:
    print k
    crs[k] = v[k].cars
    sqrs[k] = {}
    carPos[k] = get_cars(crs[k])
    for i in xrange(36):
        sqrs[k][i] = Square(i)
    for car in crs[k]:
        car.clear_squares(sqrs[k])
        car.get_squares(sqrs[k])
    showCars(sqrs[k])
    status = checkWin(sqrs[k], newR)
    if status:
        break

#print carPos


# In[1]:

def show_animation(moves):
    """show the animation of the movement of the cars"""
    # set up pygame
    pygame.init()

    # set up the window
    WINDOWWIDTH = 300
    WINDOWHEIGHT = 300
    windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
    pygame.display.set_caption('Rush Hour')

    # set up the colors
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    PURPLE = (128, 0, 128)
    TEAL = (0, 128, 128)
    LIME = (0, 128, 0)
    GRAY = (128, 128, 128)
    WHITE = (255, 255, 255)
    PINK = (255, 200, 200)
    DBLUE = (0, 0, 128)
    # setup squares
    squareWidth = 50
    squareHeight = 50
    squares = {}
    for i in xrange(36):
        squares[i] = {'rect':pygame.Rect((i%6)*squareWidth, (i/6)*squareHeight, squareWidth, squareHeight), 'color':BLACK}

    # setup cars
    cars = {}
    cars['A'] = {'rect':pygame.Rect(4*squareWidth, 0*squareHeight, squareWidth * 2, squareHeight), 'color':GREEN}
    cars['B'] = {'rect':pygame.Rect(2*squareWidth, 1*squareHeight, squareWidth * 2, squareHeight), 'color':BLUE}
    cars['C'] = {'rect':pygame.Rect(4*squareWidth, 1*squareHeight, squareWidth * 2, squareHeight), 'color':PURPLE}
    cars['E'] = {'rect':pygame.Rect(4*squareWidth, 2*squareHeight, squareWidth, squareHeight * 3), 'color':PINK}
    cars['F'] = {'rect':pygame.Rect(5*squareWidth, 2*squareHeight, squareWidth, squareHeight * 3), 'color':LIME}
    cars['G'] = {'rect':pygame.Rect(0*squareWidth, 3*squareHeight, squareWidth * 2, squareHeight), 'color':GRAY}
    cars['H'] = {'rect':pygame.Rect(2*squareWidth, 3*squareHeight, squareWidth * 2, squareHeight), 'color':TEAL}
    cars['I'] = {'rect':pygame.Rect(3*squareWidth, 4*squareHeight, squareWidth, squareHeight * 2), 'color':YELLOW}
    cars['J'] = {'rect':pygame.Rect(4*squareWidth, 5*squareHeight, squareWidth * 2, squareHeight), 'color':DBLUE}
    cars['R'] = {'rect':pygame.Rect(1*squareWidth, 2*squareHeight, squareWidth * 2, squareHeight), 'color':RED}

    # print cars['R']['rect'].w
    # print cars['R']['rect'].h
    # print cars['A']['rect'].x
    # print cars['A']['rect'].y

    # run the game loop
    for m in sorted(moves):
        # check for the QUIT event
        #print m
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        # draw the white background onto the surface
        windowSurface.fill(WHITE)        
        # draw the squares
        for i in squares:    
            pygame.draw.rect(windowSurface, squares[i]['color'], squares[i]['rect'], 1)
        # update the cars
        carsToMove = moves[m]
        for car in carsToMove:
            name = car
            x = carsToMove[car][0]
            y = carsToMove[car][1]
            cars[name]['rect'].x = x * squareWidth
            cars[name]['rect'].y = y * squareHeight
            # draw cars
            pygame.draw.rect(windowSurface, cars[name]['color'], cars[name]['rect'])
        # draw the window onto the screen
        pygame.display.update()
        time.sleep(1.0)
        # check for quit
        if m == len(moves) - 1:
            event.type = QUIT
    


# In[4]:

show_animation(carPos)


# In[ ]:



