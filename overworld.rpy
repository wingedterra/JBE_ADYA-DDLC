##ADYA Overworld Engine for Ren'Py##
##Moleworks 2015##
##A* Pathfinding adapted from "Find a Way" demo by Sean McKiernan (Mekire)##
##Released under the Attribution-NonCommercial 3.0 United States (CC BY-NC 3.0 US)##
#Primary classes:
        #Enemy
        #NPC
        #Player
        #Scenery
        #Portal
                
init python:
    import copy
    import math
    import random
    import pygame
    import operator
    #---CUSTOMIZABLE STUFF STARTS HERE---#
    HEIGHT = config.screen_height
    WIDTH  = config.screen_width
    TILESIZE = 128
    PLAYER_SIG = "+" #player signifier for maps, cannot use this signifier for any other layout items
    minSwipe = 80
    maxClick = 15
    longPressTime = 200
    config.keymap['screenshot'].append('x')
    config.keymap['screenshot'].remove('s')
    
    #--STILL CUSTOMIZABLE BUT NOT ADVISED--#
    
    x = config.layers.index('transient')
    
    config.layers = config.layers[:x] + ["mapEngine","npcPortraits"] + config.layers[x:]
    sys.setrecursionlimit(20000)
   

    
    ops = {"+": operator.add,
       "-": operator.sub,
       "*": operator.mul,
       "/": operator.div,
       "<=": operator.le,
       ">=": operator.ge,
       "<": operator.lt,
       ">": operator.gt}
       
    #---ALL CODE PAST THIS POINT.---#
    
    
# Function to detect swipes
# -1 is that it was not detected as a swipe or click
# It will return 1 , 2 for horizontal swipe
# If the swipe is vertical will return 3, 4
# If it was a click it will return 0
    def getSwipeType():
            x,y=pygame.mouse.get_rel()
            if abs(x)<=minSwipe:
                    if abs(y)<=minSwipe:
                            if abs(x) < maxClick and abs(y)< maxClick:
                                    return 0
                            else:
                                    return -1
                    elif y>minSwipe: #down
                            return 3
                    elif y<-minSwipe: #up
                            return 4
            elif abs(y)<=minSwipe:
                    if x>minSwipe: #right
                            return 1
                    elif x<-minSwipe: #left
                            return 2
            return 0

    #Control if there is a longPress
    def longPress(downTime):
            if pygame.time.get_ticks()-longPressTime>downTime:
                    return True
            else:
                    return False

    class NonUniformRandom(object):
                def __init__(self, list_of_values_and_probabilities):

                    #expects a list of [ (value, probability), (value, probability),...]

                    self.the_list = list_of_values_and_probabilities
                    self.the_sum = sum([ v[1] for v in list_of_values_and_probabilities])
    
                def pick(self):

                    #return a random value taking into account the probabilities

                    import random
                    r = random.uniform(0, self.the_sum)
                    s = 0.0
                    for k, w in self.the_list:
                        s += w
                        if r < s: return k
                    return k
                    
    def closeMap():
        ui.layer("mapEngine")
        ui.clear()
        ui.close()
        

    
    class OverworldDisplayable(renpy.Displayable):
        class Enemy():
            
            #ENEMY CLASS
                        #init
                        #getRange
                        #chooseMove
                        #move
                        #stop
                        #snapToGrid
                        #snapToRange
                        #walk_animation
                        #checkLOS
                        #chase
                        #start_chasing
                        #checkObstacles
                        #update
        
            def __init__(self, x, y, range, roaming, sprites, facing, battleLabel):
                self.northFrames = sprites[0]
                self.southFrames = sprites[1]
        
                self.eastFrames = sprites[2]
                self.westFrames = sprites[3]
                self.roaming = roaming
                self.age = 0
                self.zLayer = 2
                self.facing = facing
                if facing == 'up':
                    self.image = Image(self.northFrames[0])
                    self.frames = self.northFrames
                elif facing == 'down':
                    self.image = Image(self.southFrames[0])
                    self.frames = self.southFrames
                if facing == 'left':
                    self.image = Image(self.westFrames[0])
                    self.frames = self.westFrames
                if facing == 'right':
                    self.image = Image(self.eastFrames[0])
                    self.frames = self.eastFrames
                self.exclamation = Image("exclamation.png")
                self.Walking = False

                self.rect = pygame.Rect((x, y), (sprites[4][0], sprites[4][1]))
                self.range = range #keep note of range for later dynamic range generation
                self.getRange()
                self.actionChoices = NonUniformRandom( [('stand', 15), ('walk', 1)] )
                self.posLocked = False
                self.destX = None #The x coordinate of our destination
                self.destY = None #The y coordinate of our destination
                self.goToLabel = battleLabel #label jumped to to initiate battle
                
                #initialize whether enemy is chasing, correcting itself, or finding a path.
                self.chasing = False
                self.correcting = False
                self.caught = False
                self.pathfinder = None
                self.pathPos = None
            
            def getRange(self):
                #Determine area wherein enemy can roam
                if self.range is not None:
                    self.rangeRight = self.rect.x + (self.range[0]/2)
                    self.rangeLeft = self.rect.x - (self.range[0]/2)
                    self.rangeBottom = self.rect.y + (self.range[1]/2)
                    self.rangeTop = self.rect.y - (self.range[1]/2)
                    
            def chooseMove(self, obstacles,player):
                #Randomly select next movement
                if not self.posLocked:
                    dirChoices = ['up','down','left','right']
                    #first, figure out where player is, to explicitly avoid that direction
                    if self.__class__ == OverworldDisplayable.NPC:
                        if player.rect.bottom <= self.rect.top and abs(player.rect.x-self.rect.x) <= TILESIZE:
                            dirChoices.remove('up')
                        elif player.rect.top >= self.rect.bottom and abs(player.rect.x-self.rect.x) <= TILESIZE:
                            dirChoices.remove('down')
                        elif  player.rect.right <= self.rect.left and abs(player.rect.y-self.rect.y) <= TILESIZE:
                            dirChoices.remove('left')
                        elif player.rect.left >= self.rect.right and abs(player.rect.y-self.rect.y) <= TILESIZE:
                            dirChoices.remove('right')

                    tempRect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height) #set up a temporary rect to predict all the points of intersect   
                    for o in obstacles:
                        tempRect.y =self.rect.y - TILESIZE
                        if o.rect.colliderect(tempRect) and 'up' in dirChoices:
                            dirChoices.remove('up')
                        tempRect.y =self.rect.y + TILESIZE
                        if o.rect.colliderect(tempRect)  and 'down' in dirChoices:
                            dirChoices.remove('down')
                        tempRect.y = self.rect.y
                        tempRect.x =self.rect.x - TILESIZE
                        if o.rect.colliderect(tempRect)  and 'left' in dirChoices:
                            dirChoices.remove('left')
                        tempRect.x =self.rect.x + TILESIZE
                        if o.rect.colliderect(tempRect)  and 'right' in dirChoices:
                            dirChoices.remove('right')
                        tempRect.x = self.rect.x
                        
                    #finally, check range
                    if self.rect.y - TILESIZE < self.rangeTop and 'up' in dirChoices:
                            dirChoices.remove('up')
                    if self.rect.y + TILESIZE > self.rangeBottom and 'down' in dirChoices:
                            dirChoices.remove('down')
                    if self.rect.x - TILESIZE < self.rangeLeft  and 'left' in dirChoices:
                            dirChoices.remove('left')
                    if self.rect.x + TILESIZE > self.rangeRight  and 'right' in dirChoices:
                            dirChoices.remove('right')
                            
                    #just in case this eliminated all our options, set our action to stand if the array is empty
                    if len(dirChoices) == 0:
                        moveChoice = "stand"
                    else:
                        moveChoice = self.actionChoices.pick() #choose whether to stand or walk. Heavily weighted to stand.
                        
                        
                    if moveChoice == 'walk': # if walk was chosen, now must choose a direction. Stand will simply wait for next loop.
                        dirChoice = random.choice(dirChoices)
                        
                        if dirChoice == 'up':
                            self.destX = self.rect.x
                            self.destY = self.rect.y - TILESIZE
                                
                        elif dirChoice == 'down':
                            self.destX = self.rect.x
                            self.destY = self.rect.y + TILESIZE

                        elif dirChoice == 'left':
                            self.destX = self.rect.x - TILESIZE
                            self.destY = self.rect.y

                        elif dirChoice == 'right':
                            self.destX = self.rect.x + TILESIZE
                            self.destY = self.rect.y
                            
                            
                                
                        self.snapToGrid([self.destX, self.destY]) #snap our new destination to the tile grid
                        self.posLocked = True #lock on to target, so move chooser won't change path   

            def move(self):

                #Move towards destination
                if self.destX is not None and self.destY is not None: #Do we have a destination?
                    if not self.Walking:
                        self.Walking = True
                    if self.destX == self.rect.x and self.destY == self.rect.y:#Are we there?
                        if not self.chasing or self.caught: #if we're not chasing something, or if we caught it
                                self.stop() #stop!
                        elif self.chasing: #if we're chasing something, chances are our destination is just the next step on a path, so handle that differently
                            if len(self.pathfinder.solution) > 0: #if we have a path to chase
                                
                                self.destX = self.pathfinder.solution[self.pathPos][0] #change our destination to the position of the next cell in the path
                                self.destY = self.pathfinder.solution[self.pathPos][1]
                                if len(self.pathfinder.solution) > (self.pathPos+1): #move up the path if there's room
                                    self.pathPos+=1
        
                    else: #if we're not there yet, keep going
                                        
                        if self.destX < self.rect.x: #if the destination is to our left...
                            self.rect.x-= 8 #move left
                            if self.frames <> self.westFrames: #make sure our frames match up, just in case something happened.
                                self.frames = self.westFrames
                                
                        if self.destX > self.rect.x: #do the same for right...
                            self.rect.x+= 8
                            if self.frames <> self.eastFrames:
                                self.frames = self.eastFrames
                                
                        if self.destY < self.rect.y: #...up..
                            self.rect.y-= 8
                            if self.frames <> self.northFrames:
                                self.frames = self.northFrames
                        
                        if self.destY > self.rect.y: #...down
                            self.rect.y+= 8
                            if self.frames <> self.southFrames:
                                self.frames = self.southFrames
        
                                
                else: #if we have no desination set, just skip this method
                    pass
        
            def stop(self):
                #Stop everything
                self.Walking = False
                self.posLocked = False
                self.destX = None
                self.destY = None
                self.chasing = False
                self.snapToRange()
                        
            def snapToGrid(self,array):
                #Intermittently make sure we're on the grid. This should prevent most collision issues with roaming.
                for i in array: 
                    if i%TILESIZE <> 0: #is our coordinate divisible by the tilesize? If not..
                        multBy = int(i/TILESIZE) #divide it and get int, to get closest multiple
                        i = TILESIZE*multBy #multiply this by tilesize to get closest tile
                        
            def snapToRange(self):
                #snap NPC's back into range if they are nudged out
                if self.rect.y < self.rangeTop:
                    self.rect.y = self.rangeTop
                if self.rect.y > self.rangeBottom:
                    self.rect.y = self.rangeBottom
                if self.rect.x < self.rangeLeft:
                    self.rect.x = self.rangeLeft
                if self.rect.x > self.rangeRight:
                    self.rect.x = self.rangeRight
                
            def walk_animation(self):        
                if self.age < (len(self.frames) - 1):
                    pass
                else:
                    self.age = 0
                self.image = Image(self.frames[int(self.age)])
        
            def checkLOS(self,player,obstacles):
                #check if player is within line of sight
                
                if self.frames == self.eastFrames or self.frames == self.westFrames:
                    comp_coord1 = self.rect.x
                    comp_coord1b = self.rect.y
                    comp_coord3 = player.rect.x
                    comp_coord3b = player.rect.y
                elif self.frames == self.northFrames or self.frames == self.southFrames:
                    comp_coord1 = self.rect.y
                    comp_coord1b = self.rect.x
                    comp_coord3 = player.rect.y
                    comp_coord3b = player.rect.x
                if self.frames == self.eastFrames or self.frames == self.southFrames:
                    tileOp = ops["+"]
                    comp = ops["<="]
                    
                elif self.frames == self.westFrames or self.frames == self.northFrames:
                    tileOp = ops["-"]
                    comp = ops[">="]

                    
                if comp(comp_coord3, (tileOp(comp_coord1,(TILESIZE * 3)))) and comp((comp_coord1b - (self.rect.height/2)), comp_coord3b) and comp(comp_coord3b, (comp_coord1b + (self.rect.height/2))):
                    #check if player is within certain distance of where enemy is facing, and not off to the side    
                    for o in obstacles:
                            if self.frames == self.northFrames or self.frames == self.southFrames:
                                comp_coord2 = o.rect.y
                            else:
                                comp_coord2 = o.rect.x
                            if comp(comp_coord1, comp_coord2) and comp(comp_coord2, comp_coord3): #check if an obstacle is between player and enemy
                                self.stop() #if so, player can't be seen
                            else: #if view is unobstructed, start chasing
                                self.start_chasing()
                                
        
                else:
                    self.chasing = False #not in range, so don't chase
                    
                    

            def chase(self,player, obstacles):
                #Update pathfinding to follow player
                
                if self.chasing: #check if chase has been initiated first
                    self.pathfinder = Star((self.rect.x,self.rect.y),(player.rect.x,player.rect.y),obstacles) #either way, update our pathfinder
                    self.pathfinder.setup() #setup all the variables
                    self.pathfinder.evaluate() #evaluate path
                    self.pathPos = 0
                    
                    if len(self.pathfinder.solution) > 0:
                        self.destX = self.pathfinder.solution[self.pathPos][0] #set our destination to the first cell in our path
                        self.destY = self.pathfinder.solution[self.pathPos][1]
                    
                else:
                    pass
        
            def start_chasing(self):
                self.chasing = True
                self.posLocked = True
                self.walking = True
                self.correcting = False
                
                
            def checkObstacles(self,obstacles,player):
                #Handle obstacle collison
            
                hit_list = pygame.sprite.spritecollide(self, obstacles, False) #if something is hit, change route
                if len(hit_list) == 0:
                    self.correcting = False # if nothing is hitting us, assume path has been corrected
                for obst in hit_list:
                    if not self.correcting and obst is not self:
                        if self.__class__ == OverworldDisplayable.Enemy: #only do dynamic range on enemy
                            self.getRange() #get a new range, in case the chase sequence brought us out of ours
                        self.stop()
                        self.correcting = True #only check once, just long enough to get out of range and not in a loop
                        self.chooseMove(obstacles,player) #roll again

        
            def update(self,obstacles,player):
            
                        if not self.caught and self.roaming: #skip all movement procedures for static NPC's       
                            
                            self.checkObstacles(obstacles,player)
                            if not self.chasing:
                                self.checkLOS(player, obstacles)
                            self.chase(player, obstacles)
                            if not self.chasing:
                                self.chooseMove(obstacles,player)
                            self.move()

                        if self.Walking:
                            self.age += 1 #increment walking frame
                            self.walk_animation() #animate
                        elif not self.Walking:
                            self.image = Image(self.frames[0])
            
                        if self.chasing and not self.rect.colliderect(player.rect): #if enemy is chasing and hasn't reached player yet
                            self.Walking = True #make sure they're walking
                            
                        if not self.posLocked:
                            #self.snapToGrid([self.rect.x, self.rect.y])
                            self.snapToRange()
        
        class NPC(Enemy):
            #NPC CLASS
                #subclass of Enemy. Inherits all non-chase related functions.
            def __init__(self, x, y, range, roaming, sprites, facing, battleLabel):
            
                OverworldDisplayable.Enemy.__init__(self, x, y, range, roaming, sprites, facing, battleLabel)
                
                self.actionChoices = NonUniformRandom( [('stand', 47), ('walk', 1)] ) #NPC's are much more weighted to stand in place
                self.actionLabel = battleLabel #share battlelabel var with enemy, but use it for action instead
                
            def stop(self):
                self.Walking = False
                self.posLocked = False
                self.destX = None
                self.destY = None
                self.chasing = False
                
            def face_player(self,player):
                    if player.frames == player.eastFrames:
                        self.frames = self.westFrames
                    elif player.frames == player.westFrames:
                        self.frames = self.eastFrames
                    elif player.frames == player.northFrames:
                        self.frames = self.southFrames
                    elif player.frames == player.southFrames:
                        self.frames = self.northFrames
                    self.image = Image(self.frames[0])
        
            def update(self,obstacles,player):
        
                            
                    if self.roaming:
                        self.chooseMove(obstacles,player)
                        self.move()
                        self.checkObstacles(obstacles,player)
                    
        
        
                    if self.Walking:
                        self.age += 1
                        self.walk_animation()
                    elif not self.Walking:
                        self.image = Image(self.frames[0])
        
                    if self.rect.colliderect(player.rect):
                        self.stop()
                    if not self.posLocked:
                        self.snapToGrid([self.rect.x, self.rect.y])
                        if self.roaming:
                            self.snapToRange()
                        
        
        class Player():
            #PLAYER CLASS
                #init
                #walk_animation
                #check_walking
                #collide
                #update
            def __init__(self, x, y, facing, sprites):
                self.facing = facing
                self.xvel = 0
                self.yvel = 0
                self.up, self.down, self.left, self.right = False, False, False, False #make sure we're not initially moving
                
                self.age = 0
                self.caught = False
                
                self.northFrames = sprites[0]
                self.southFrames = sprites[1]
        
                self.eastFrames = sprites[2]
                self.westFrames = sprites[3]

                self.standing = {'right': self.eastFrames[0], 'left': self.westFrames[0],
                                 'up': self.northFrames[0], 'down': self.southFrames[0]}
                    
                    
                if facing == 'up':
                    self.frames = self.northFrames
                elif facing == 'down':
                    self.frames = self.southFrames
                elif facing == 'left':
                    self.frames = self.westFrames
                else:
                    self.frames = self.eastFrames
                self.walking = False
                
                self.image = Image(self.standing[self.facing])
                self.rect = pygame.Rect((x, y), (sprites[4][0], sprites[4][1]))
                self.zLayer = 2
                self.destX = None
                self.destY = None
                
            def walk_animation(self):        
                if self.age < 5:
                    pass
                else:
                    self.age = 0
                self.image = Image(self.frames[int(self.age // 1)])
                
            def check_walking(self): #make sure player is walking when appropriate
                if self.yvel == 0 and self.xvel == 0:
                    self.walking = False
                    
            def collide(self, walls):
                self.rect.centerx += self.xvel #move horizontally
                block_hit_list = pygame.sprite.spritecollide(self, walls, False)

                for _block in block_hit_list: #check the objects we hit
                    if _block.__class__ <> OverworldDisplayable.Portal: #portals are except from collision check
                        if self.xvel >0: #check movement direction
                            self.rect.right = _block.rect.left #keep player pressed against appropriate wall
                        else:
                            self.rect.left = _block.rect.right


                self.rect.centery += self.yvel #do the same for vertical movement

                # Check and see if we hit anything
                block_hit_list = pygame.sprite.spritecollide(self, walls, False)

                for _block in block_hit_list:
                    if _block.__class__ <> OverworldDisplayable.Portal:
                        if self.yvel > 0:
                            self.rect.bottom = _block.rect.top
                        else:
                            self.rect.top = _block.rect.bottom
           
            def update(self, walls):

                if self.walking:
                    if self.facing == 'left':
                        self.frames = self.westFrames
                    elif self.facing == 'right':
                        self.frames = self.eastFrames
                    elif self.facing == 'up':
                        self.frames = self.northFrames
                    elif self.facing == 'down':
                        self.frames = self.southFrames
                    self.age += 0.25
                    self.walk_animation()
                elif not self.walking:
                    self.image = Image(self.standing[self.facing])
                
                #set velocity according to movement direction
                vel = 8
                if self.up:
                    self.yvel = -vel
                elif self.down:
                    self.yvel = vel
                if self.left:
                    self.xvel = -vel
                elif self.right:
                    self.xvel = vel
                if not self.up and not self.down:
                    self.yvel = 0
                    self.destY = None
                if not self.left and not self.right:
                    self.xvel = 0
                    self.destX = None
                self.collide(walls)

                
                self.check_walking()
                  

        class Scenery(): 
             #SCENERY, A class for objects like buildings and trees
             def __init__(self, x, y, image, width, height, zLayer, hasRoof, label, actionLabel):
        
                self.image = Image(image)
        
        
                self.rect = pygame.Rect((x, y), (width, height))
        
                self.zLayer = zLayer #what layer in the z ordering will this item be on?
                self.hasRoof = hasRoof #does it have a roof?
                self.goToLabel = label #Where the player will be redirected on contact
                self.actionLabel = actionLabel #An action, usually a description, fired when the player inspects the object
        
        class Portal(): 
            #PORTAL, An invisible object that jumps a player to another map
            def __init__(self, x, y,label):
                self.image = pygame.Surface((TILESIZE, TILESIZE))
                self.image.set_alpha(128)
                self.image.fill((255,255,255))
                self.rect = self.image.get_rect()
                self.rect.x = x
                self.rect.y = y
                self.goToLabel = label
                
        def getOffset(self): #get player's current position for re-entering map
            self.playerX = self.player.rect.x
            self.playerY = self.player.rect.y
            
                
    
        def __init__(self, map_layout = None, tileList = None, portals = None, portal_tiles = None, enemy_layout =None, enemySprites = None, NPCSprites = None, groundLayout = None, playerSprites = None, playerX = None, playerY = None, scrolling = True):
    
            renpy.Displayable.__init__(self)
            self.zList = []
    
            
            self.goTo = None

            self.buildings = []
            self.rooves = []
            

            self.enemyList = []
            self.npcList = []
            self.portalList = []
            
            
            self.playerList = []            
            self.sceneryList = []
            self.NPCObstacles = [] #NPC's treat player as obstacle, enemy and player do not
            
            self.playerX = playerX
            self.playerY = playerY
            
            self.talking = False 
            self.scrolling = scrolling
            
            #start generating map from assets
            if map_layout is not None:
                x = 0 #start at top left corner
                y = 0
                bldngCount = 0
                roofCount = 0
                
                for row in map_layout: #go into a row
                    for col in row: #now each individual item
                        if col == PLAYER_SIG: #player signifier is constant
                            if playerX is None and playerY is None: #check if a previous position hasn't been passed in
                                self.player = OverworldDisplayable.Player(x , y, "down", playerSprites)
                            else: #if not, put in default position
                                self.player = OverworldDisplayable.Player(playerX , playerY, "down", playerSprites)
                                
                            self.playerList.append(self.player)
                            self.NPCObstacles.append(self.player)
                            self.zList.append(self.player)
                        for tile in tileList:
                            if col == tile[0]: #make buildings
                                self.buildings.append(OverworldDisplayable.Scenery(x,y, tile[1] + ".png", tile[2][0], tile[2][1], 2, tile[4], tile[5], tile[6]))
                                self.sceneryList.append(self.buildings[bldngCount])
                                self.NPCObstacles.append(self.buildings[bldngCount])
                                self.zList.append(self.buildings[bldngCount])
    
                                if self.buildings[bldngCount].hasRoof: #if building has roof, make roof as well
                                    self.rooves.append(OverworldDisplayable.Scenery(x,y, tile[1] + "_roof.png", tile[3][0], tile[3][1], 3, False, None, None))
                                    self.zList.append(self.rooves[roofCount])
                                    #adjust building position to match
                                    self.buildings[bldngCount].rect.x += (self.rooves[roofCount].rect.width - self.buildings[bldngCount].rect.width)/2 
                                    self.buildings[bldngCount].rect.y += (self.rooves[roofCount].rect.height - self.buildings[bldngCount].rect.height)
                                    roofCount +=1
                                bldngCount += 1
    
                        x += TILESIZE #move over one tile after placing
                        
                    y += TILESIZE #row cleared, move down
                    x = 0 #reset x position
            

            #do the same for portals
            if portals is not None:
                x = 0
                y = 0
                
                for row in portals:
                    for col in row:
                        for tile in portal_tiles:
                            if col == tile[0]:
                                self.portalList.append(OverworldDisplayable.Portal(x,y, tile[1]))
                                self.sceneryList.append(OverworldDisplayable.Portal(x,y, tile[1]))
                        x += TILESIZE
                        
                    y += TILESIZE
                    x = 0
            
            #then NPC's and enemies    
            if enemy_layout is not None:
                x = 0
                y = 0
                enemyCount = 0
                NPCCount = 0
                for row in enemy_layout:
                    for col in row:
                        for tile in enemySprites:
                            if col == tile[0] and not tile[6].won:
                                self.enemyList.append(OverworldDisplayable.Enemy(x, y, tile[1], tile[2], tile[3], tile[4], tile[5]))
                                self.zList.append(self.enemyList[enemyCount])
                                self.NPCObstacles.append(self.enemyList[enemyCount])
                                enemyCount+= 1
                        for n in NPCSprites:
                            if col == n[0]:
                                self.npcList.append(OverworldDisplayable.NPC(x, y,n[1], n[2], n[3], n[4], n[5]))
                                self.zList.append(self.npcList[NPCCount])
                                self.sceneryList.append(self.npcList[NPCCount])
                                self.NPCObstacles.append(self.npcList[NPCCount])
                                NPCCount+= 1
                            
                
                        x += TILESIZE
                        
                    y += TILESIZE
                    x = 0
            #finally, make ground tiles
            if groundLayout is not None:
                x = 0
                y = 0
                groundCount = 0
                self.groundList = []
                for row in groundLayout:
                    for col in row:
                        for tile in tileList:
                            if col == tile[0]:
                                self.groundList.append(OverworldDisplayable.Scenery(x,y, tile[1] + ".png", tile[2][0], tile[2][1], 2, tile[4], tile[5],tile[6]))
                                groundCount +=1
    
                                
                        x += TILESIZE
                        
                    y += TILESIZE
                    x = 0
                
    
        def render(self, width, height, st, at):
            ret = renpy.display.render.Render(width, height) #The main rendering screen, don't blit directly to this!
            map_child = renpy.Render(width, height, st, at) #The map itself, a separate child object blitted to ret. Blit to this!
            
            self.zList.sort(key=lambda x: x.rect.y, reverse=False) #sort everything according to y position. This determines the order in which they will be rendered.
            for g in self.groundList: #ground is rendered first, with no sorting.
                 map_child.blit(renpy.render(g.image, g.rect.width, g.rect.height, st, at), (g.rect.x, g.rect.y))
            for zl in self.zList: #layer 2 has pretty much everything else
                if zl.zLayer == 2:
                    map_child.blit(renpy.render(zl.image, zl.rect.width, zl.rect.height, st, at), (zl.rect.x, zl.rect.y))
            for zl in self.zList: #and finally, higher altitude items like roofs
                if zl.zLayer == 3:
                    map_child.blit(renpy.render(zl.image, zl.rect.width, zl.rect.height, st, at), (zl.rect.x, zl.rect.y))
            
            #update everything, unless we're talking. Trying to update while talking results in a stack overflow, and is a little too busy anyway.        
            if not self.talking:
                self.player.update(self.sceneryList)

            for e in self.enemyList:
                if not self.talking:
                    e.update(self.sceneryList, self.player)
                if e.chasing:
                    #if an enemy is chasing, render a tiny "!" above their head
                    map_child.blit(renpy.render(e.exclamation, 36, 30, st, at),((e.rect.x + 18),(e.rect.y - (e.rect.height/4))))
                
                if e.rect.colliderect(self.player.rect):
                            e.stop()
                            e.caught = True

                            e.chasing = False
                            
                            self.goTo = e.goToLabel
                            renpy.timeout(0)                   
            for n in self.npcList:
                if not self.talking:
                    n.update(self.NPCObstacles, self.player)
            
            for s in self.sceneryList: #handle collision with important buildings
                if hasattr(s, 'hasRoof') and  s.goToLabel is not None: #if it's a building and has a goToLabel
                    if s.rect.bottom == self.player.rect.top and s.rect.left<self.player.rect.x<s.rect.right and self.player.frames == self.player.northFrames: #and we collided with it
                        renpy.sound.play("door.ogg", channel=1) #play a sound
                        self.goTo = s.goToLabel #keep note of the label we'll be returning
                        renpy.timeout(0) #and end the displayable
            
            #do something similar for portals            
            for p in self.portalList:
                if self.player.rect.colliderect(p.rect):    
                    self.goTo = p.goToLabel
                    renpy.timeout(0)
                    
            if self.scrolling: #if it's a scrolling area, update the child render's coordinates
                x,y = self.panMap()
            else:
                x,y = 0,0 #if not, keep them in place
            ret.blit(map_child, (x, y)) #render the child at new coordinates
            renpy.redraw(self, .03) 
            return ret
        def panMap(self): #Get the necessary offset to keep player centered
            newY = (HEIGHT *.5) - self.player.rect.y
            newX = (WIDTH *.5) - self.player.rect.x
            return (newX, newY)
            
        def talk(self,vil):
            if hasattr(vil, 'actionLabel') and  vil.actionLabel is not None: 
                #make sure we're close to the object
                if abs(self.player.rect.centery - vil.rect.centery) <= ((vil.rect.height +self.player.rect.height)/2) and abs(self.player.rect.centerx - vil.rect.centerx) <= ((vil.rect.width +self.player.rect.width)/2):
                    if hasattr(vil, 'frames'):
                        vil.face_player(self.player) #NPC's should face player
                    #stop all player activity
                    self.player.walking = False
                    self.player.up = False
                    self.player.down = False
                    self.player.right = False
                    self.player.left = False
                    self.player.image = Image(self.player.frames[0]) #set image to standing frame
                    self.talking = True
                    if vil.__class__ == OverworldDisplayable.Scenery: #if we're examining a building, we must be facing the front to interact.
                        if self.player.facing == 'up' and self.player.rect.top >= vil.rect.bottom:
                            renpy.call_in_new_context(vil.actionLabel)
                    else:
                        renpy.call_in_new_context(vil.actionLabel) #NPC's will face you, so just call label.
                    self.talking = False #once the label returns control to the displayable, we're done talking.
        # Handles events.
        def event(self, ev, x, y, st):
            import pygame
            if self.goTo:
                self.getOffset()
                return (self.goTo, self.playerX, self.playerY)
            
            if 'touch' in config.variants: #controls are for touch only        
                # Mouse presed
                if (ev.type == pygame.MOUSEBUTTONDOWN):
                        mouseDownTime = pygame.time.get_ticks()
                        mouseDownPos = pygame.mouse.get_pos()
                        pygame.mouse.get_rel()
        
                # Mouse released
                if (ev.type == pygame.MOUSEBUTTONUP):
                        pos = pygame.mouse.get_pos() #get position of mouse
                        off = self.panMap() #get offset of the child
                        pos2 = ((pos[0] - off[0]),(pos[1] - off[1])) #adjust for offset, so we're getting reasonably close coordinates
                        for vil in self.sceneryList: #prioritize NPC interaction
                            if math.hypot((self.player.rect.x - vil.rect.x), (self.player.rect.y - vil.rect.y)) <= (TILESIZE * 2): #make sure player is close to NPC
                                if vil.rect.collidepoint(pos2): #make sure mouse is on NPC when clicked
                                        self.talk(vil)
                            
                        swipe = getSwipeType() #determine if the player swiped, and in which direction
                        if(swipe != -1):
                                changed = None
                                if (swipe == 1): #right swipe
                                    self.player.xvel = TILESIZE
                                    self.player.collide(self.sceneryList)
                                    self.player.facing = 'right'
                                    self.player.walking = True
                                if (swipe == 2): #left swipe
                                    self.player.xvel = -TILESIZE
                                    self.player.collide(self.sceneryList)
                                    self.player.facing = 'left'
                                    self.player.walking = True
                                    
                                if (swipe == 3): #down swipe
                                    self.player.yvel = TILESIZE
                                    self.player.collide(self.sceneryList)
                                    self.player.facing = 'down'
                                    self.player.walking = True
    
                                if (swipe == 4): #upward swipe
                                    self.player.yvel = -TILESIZE
                                    self.player.collide(self.sceneryList)
                                    self.player.facing = 'up'
                                    self.player.walking = True
    
                                #snap result to grid
                                self.snapToGrid([self.player.rect.x,self.player.rect.y])
                                        
            if ev.type == pygame.QUIT: #stop any residual keypresses if the close button is pressed
                #YesNo screen must NOT be modal for this to work.
                self.player.walking = False
                self.player.up = False
                self.player.down = False
                self.player.right = False
                self.player.left = False
                
                
            #and finally, directions.
                
                                        
            if ev.type == pygame.KEYDOWN and not self.player.caught and not self.talking:
    
                if ev.key == pygame.K_UP or ev.key == pygame.K_w:
                    self.player.facing, self.player.up = 'up', True
                    self.player.walking = True
   
                if ev.key == pygame.K_RIGHT or ev.key == pygame.K_d:
                    self.player.facing, self.player.right = 'right', True
                    self.player.walking = True
                
                if ev.key == pygame.K_LEFT or ev.key == pygame.K_a:
                    self.player.facing, self.player.left = 'left', True
                    self.player.walking = True
                    
                if ev.key == pygame.K_DOWN or ev.key == pygame.K_s:
                    self.player.facing, self.player.down = 'down', True
                    self.player.walking = True

                if ev.key in [pygame.K_RSHIFT, pygame.K_LSHIFT, pygame.K_SPACE] and not self.talking and not self.goTo:
                    for vil in self.sceneryList:
                        self.talk(vil)

                        
            if ev.type == pygame.KEYUP:
                
                if ev.key == pygame.K_RIGHT or ev.key == pygame.K_d:
                    self.player.right = False
                if ev.key == pygame.K_LEFT or ev.key == pygame.K_a:
                    self.player.left = False
                if ev.key == pygame.K_UP or ev.key == pygame.K_w:
                    self.player.up = False
                if ev.key == pygame.K_DOWN or ev.key == pygame.K_s:
                    self.player.down = False
                for keyups_above in [pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN, pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]:
                    if ev.key != keyups_above:
                        pass
                  
