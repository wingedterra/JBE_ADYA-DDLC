##Author: Sean McKiernan (Mekire)
init python:
    def rook(x,y):
        return x+y
    
    
    
    class Star(object):
        #This class is the astar algorithm itself.  The goal is to make it
        #flexible enough that it can be used in isolation.#
        def __init__(self,start,end,barriers):
            #Arguments start and end are coordinates to start solving from and to.
            #move_type is a string cooresponding to the keys of the ADJACENTS and
            #HEURISTICS constant dictionaries. barriers is a set of cells which the
            #agent is not allowed to occupy.#
            self.start,self.end = start,end
            self.moves = [(TILESIZE,0),(-TILESIZE,0),(0,TILESIZE),(0,-TILESIZE)]
            self.heuristic = rook
            self.barrier_list = barriers
            self.get_barriers()
            self.setup()
    
        def setup(self):
            #Initialize sets,dicts and others#
            self.closed_set = set((self.start,)) #Set of cells already evaluated
            self.open_set   = set() #Set of cells to be evaluated.
            self.came_from = {} #Used to reconstruct path once solved.
            self.gx = {self.start:0} #Cost from start to current position.
            self.hx = {} #Optimal estimate to goal based on heuristic.
            self.fx = {} #Distance-plus-cost heuristic function.
            self.current = self.start
            self.current = self.follow_current_path()
            self.solution = []
            self.solved = False
            
        def check_size(self,dimension):
            spaces = int(dimension/TILESIZE) - 1
            return spaces
        def snapToGrid(self, coord):
            multBy = int(coord/TILESIZE)
            coord = TILESIZE * multBy
            return coord
    
        def get_barriers(self):
            self.barriers = [] #reset barriers
            for b in self.barrier_list: #search list of all passed barriers
                if b.rect.x%TILESIZE <> 0: #make sure barrier coordinates are on grid, so entire tile is disabled if a barrier collides.
                    x = self.snapToGrid(b.rect.x)
                else:
                    x = b.rect.x
                    
                if b.rect.y%TILESIZE <> 0:
                    y = self.snapToGrid(b.rect.y)
                else:
                    y = b.rect.y
                    
                if b.rect.width > TILESIZE: #if the barrier is wider than one tile, check how many tiles need to be added
                    spaces = self.check_size(b.rect.width)
                    i = 0
                    while i < spaces:
                        self.barriers.append((x + i, y))
                        i+=1
                if b.rect.height > TILESIZE: #same for height
                    spaces = self.check_size(b.rect.height)
                    i = 0
                    while i < spaces:
                        self.barriers.append((x, y + i))
                        i+=1
    
    
                    
                self.barriers.append((x, y))
             
            
    
        def get_neighbors(self):
            #Find adjacent neighbors with respect to how our agent moves.#
            #self.get_barriers()
            neighbors = set()
            for (i,j) in self.moves: #check all adjacents according to move type
                check = (self.current[0]+i,self.current[1]+j) #cell to check is current cell with adjacent rules applied
                if check not in self.barriers or self.closed_set: #if this cell is not in closed set or barriers
                    neighbors.add(check) #add it to neighbors
            return neighbors
    
        def follow_current_path(self):
            #In the very common case of multiple points having the same heuristic
            #value, this function makes sure that points on the current path take
            #presidence.  This is most obvious when trying to use astar on an
            #obstacle free grid.#
            next_cell = None #initially don't know what our next move is
            for cell in self.get_neighbors():
                tentative_gx = self.gx[self.current]+1 #tentatively get distance cost of one cell ahead
                if cell not in self.open_set: #if a neighboring cell is not open
                    self.open_set.add(cell) #add it to open set 
                    tentative_best = True  #declare it tentatively a best match
                elif cell in self.gx and tentative_gx < self.gx[cell]: #else if the cell has been evaluated for gx and its cost is less than our tentative
                    tentative_best = True #ditto
                else:
                    tentative_best = False # if neither of those scenarios are true, no tentative best match found
    
                if tentative_best: #if tentative best is found, apply some data to cell
                    x,y = abs(self.end[0]-cell[0]),abs(self.end[1]-cell[1]) #x and y are horizontal and vertical distance between chosen cell and end. Used for later heuristic.
                    self.came_from[cell] = self.current #add cell to path history
                    self.gx[cell] = tentative_gx #set distance cost of chosen cell to tentative distance cost
                    self.hx[cell] = self.heuristic(x,y) #get optimal heuristic from chosen cell to end and apply it to cell.
                    self.fx[cell] = self.gx[cell]+self.hx[cell] #assign distance + cost to cell's fx
                    if not next_cell or self.fx[cell]<self.fx[next_cell]: #if cost to end of chosen cell is less than the cost of the next cell (therefor closer),
                        next_cell = cell #that cell is our next cell
            return next_cell
    
        def get_path(self,cell):
            self.solution.append(cell)
    
        def evaluate(self):
            #Core logic for executing the astar algorithm.#
            if self.open_set and not self.solved: #only evaluate if there cells in the open set and the path has not been solved
                for cell in self.open_set:
                    if (self.current not in self.open_set) or (self.fx[cell]<self.fx[self.current]): #if current cell isn't open or the total cost of chosen cell is less than current
                        self.current = cell #set current cell to chosen cell
                self.get_path(self.current) #go back over path
                self.open_set.discard(self.current) #remove current cell from open set
                self.closed_set.add(self.current) #add to closed set
                self.current = self.follow_current_path() #select next cell and apply to current in order to move
            #elif not self.solution:
                #self.solution = None
