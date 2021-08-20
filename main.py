import pygame
import math
from queue import deque
from queue import PriorityQueue


'''
CHOOSE ALG BELOW 
'''
ALG = 'a*' #change alg here (a*, bfs, dfs)


WIDTH = 650 
WIN = pygame.display.set_mode((WIDTH, WIDTH)) #window
pygame.display.set_caption("Path Finder")


#Colors and Keys
RED = (255, 0, 0) 
GREEN = (0, 255, 0) #Node added to set
BLUE = (0, 0, 255) 
YELLOW = (255, 255, 0)#Path color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0) #Node is a barrier
PURPLE = (128, 0, 128) #End Node
ORANGE = (255, 165 ,0) #Start Node
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)#Node has been checked


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.width = width
        self.total_rows = total_rows
       
        self.x = row*width#pos
        self.y = col*width#pos
        self.color = WHITE #initializing color
        self.neighbors = []

    #returns pos of Node
    def get_pos(self):
        return self.row, self.col

    #resets Node
    def reset(self):
        self.color = WHITE

    #draws Node
    def draw_node(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        
        #row has neighbors below it and that neighbors is not a barrier
        if self.row < self.total_rows - 1 and grid[self.row+1][self.col].color != BLACK:
            self.neighbors.append(grid[self.row+1][self.col])

        if self.row > 0 and grid[self.row-1][self.col].color != BLACK: #UP NEIGHBOR
            self.neighbors.append(grid[self.row-1][self.col])

        if self.col < self.total_rows - 1 and grid[self.row][self.col+1].color != BLACK: #RIGHT NEIGHBOR
            self.neighbors.append(grid[self.row][self.col+1])

        if self.row > 0 and grid[self.row][self.col-1].color != BLACK: #LEFT NEIGHBOR
            self.neighbors.append(grid[self.row][self.col-1])

    #compares 2 Nodes
    def __lt__(self, other):
        return False


def create_DFS_path(start, end, prev, draw):
    path = []
    current = end
    
    while current != None:
        current.color = YELLOW
        path.append(current)
        current = prev[current]
        draw()

    path.reverse()
    if path[0] != start:
        return False


def alg_DFS(draw, grid, start, end):
    stack = []
    stack.append(start)

    visited = {node: False for row in grid for node in row}
    visited[start] = True
    prev = {node: None for row in grid for node in row}

    while len(stack) != 0:
        node = stack.pop()
        neighbors = node.neighbors

        for neighbor in neighbors:
            if not visited[neighbor]:
                stack.append(neighbor)
                visited[neighbor] = True
                prev[neighbor] = node

                if neighbor == end:
                    neighbor.color = PURPLE
                    create_DFS_path(start, end, prev, draw)
                    start.color = ORANGE
                    neighbor.color = PURPLE
                    return True
                else:
                    neighbor.color = GREEN

        draw()

    return False


def create_BFS_path(start, end, prev, draw):
    path = []
    current = end
    
    while current != None:
        current.color = YELLOW
        path.append(current)
        current = prev[current]
        draw()

    path.reverse()
    if path[0] != start:
        return False
        

def alg_BFS(draw, grid, start, end):
    q = deque()
    q.append(start)

    visited = {node: False for row in grid for node in row}
    visited[start] = True
    prev = {node: None for row in grid for node in row}

    while len(q) != 0:
        node = q.pop()
        neighbors = node.neighbors

        for neighbor in neighbors:
            if not visited[neighbor]:
                q.appendleft(neighbor)
                visited[neighbor] = True
                prev[neighbor] = node

                if neighbor == end:
                    neighbor.color = PURPLE
                else:
                    neighbor.color = GREEN

        draw()

    create_BFS_path(start, end, prev, draw)
    start.color = ORANGE
    end.color = PURPLE


#heuristic function - distance between current and end node
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    return abs(x1-x2) + abs(y1-y2)


def create_aStar_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.color = YELLOW
        draw()


def alg_aStar(draw, grid, start, end):
    count = 0 #used for tie breaker
    open_set = PriorityQueue() #used to get the smallest element (sorted via heapsort)
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float('inf') for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float('inf') for row in grid for node in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start} #stores what priority queue has stored

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2] #we want the node, which is at index 2
        open_set_hash.remove(current) #avoid dupes

        if current == end:
            create_aStar_path(came_from, end, draw)
            start.color = ORANGE
            end.color = PURPLE
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]: #if better path than current
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos()) #calc heuristic function from this Node

                if neighbor not in open_set_hash: #add node if not already in
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.color = GREEN #added to set
        
        draw()

        if current != start: 
            current.color = TURQUOISE #has been considered

    return False #path does not exist




#creates grid
def make_grid(rows, width):
    grid = []
    cube_width = width//rows #width is the width of the grid

    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i,j,cube_width, rows) #creates nodes
            if i == 0 or i == rows-1 or j ==0 or j==rows-1:
                node.color = BLACK

            grid[i].append(node)

    return grid


#creates grid lines
def draw_gridlines(win, rows, width):
    cube_width = width//rows

    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i*cube_width), (width, i*cube_width)) #horizontal lines
        for j in range(rows):
            pygame.draw.line(win, GREY, (i*cube_width, 0), (i*cube_width, width)) #verticle lines


#main draw method
def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw_node(win) #draws nodes

    draw_gridlines(win, rows, width) #draws gridlines
    pygame.display.update()


def get_mouse_pos(pos, rows, width):
    cube_width = width//rows
    y, x = pos

    row = y//cube_width
    col = x//cube_width

    return row,col


def main(win, width, alg):
    ROWS = 30
    GRID = make_grid(ROWS, width)

    start, end = None, None

    clock = pygame.time.Clock()
    run = True

    alg = alg

    while run:
        clock.tick(60)
        draw(win, GRID, ROWS, width)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    ROWS -= 1
                    start = None
                    end = None
                    GRID = make_grid(ROWS, width)
                    

                elif event.button == 5:
                    ROWS += 1
                    start = None
                    end = None
                    GRID = make_grid(ROWS, width)
                    

            if pygame.mouse.get_pressed()[0]: #left click
                pos = pygame.mouse.get_pos()
                row, col = get_mouse_pos(pos, ROWS, width)
                node = GRID[row][col]
                
                #setting colors accordingly
                if not start and node != end:
                    start = node
                    start.color = ORANGE
                elif not end and node != start:
                    end = node
                    end.color = PURPLE
                elif node != start and node != end: #creates barrier
                    node.color = BLACK

            elif pygame.mouse.get_pressed()[2]: #right click
                pos = pygame.mouse.get_pos()
                row, col = get_mouse_pos(pos, ROWS, width)
                node = GRID[row][col]
                node.reset()

                #reseting start and end if clicked
                if node == start:
                    start = None
                elif node == end:
                    end = None
            

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    
                    for row in GRID:
                        for node in row:
                            node.update_neighbors(GRID) 
                    #A* alg
                    if alg == 'a*':
                        alg_aStar(lambda: draw(win, GRID, ROWS, width), GRID, start, end)#sending draw func as an argument
                    #bfs alg
                    elif alg == 'bfs':
                        alg_BFS(lambda: draw(win, GRID, ROWS, width), GRID, start, end)

                    elif alg == 'dfs':
                        alg_DFS(lambda: draw(win, GRID, ROWS, width), GRID, start, end)

                if event.key == pygame.K_r:
                    start = None
                    end = None
                    GRID = make_grid(ROWS, width)

    pygame.quit()


#Basic instructions
print('How to use:\n\t Left-mouse click will place the start node first, followed by the end, and finally the barriers')
print('\t Right-mouse click will remove start/end/barriers - Note: A start and end node must be present to start algorithm')
print('\t Scrolling with the mouse increases/decreases the rows and create new grid (Thereby, increasing the zoom)')
print('\t Hitting space will start the algorithm')
print('\t Hitting r will create a new grid')
print('\n To change algorithms, change variable "ALG" to one of the following: a*, bfs, dfs')


main(WIN, WIDTH, ALG)