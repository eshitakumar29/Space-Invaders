"""
Subcontroller module for Alien Invaders
This module contains the subcontroller to manage a single level or wave in
the Alien Invaders game. 
# December 12, 2019
"""
from game2d import *
from consts import *
from models import *
import random

class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.
    This subcontroller has a reference to the ship, aliens, and any laser bolts
    on screen. It animates the laser bolts, removing any aliens as necessary.
    It also marches the aliens back and forth across the screen until they are
    all destroyed or they reach the defense line (at which point the player
    loses).
    """

    # GETTERS AND SETTERS
    def getShipX(self):
        """
        Returns the x attribute of the ship
        """

        return self._ship.x

    def setShipX(self,value):
        """
        Sets the x attribute of the ship to value
        Parameter value: a new x attribute to ship
        Precondition: value is an integer between 0 and GAME_WIDTH
        """

        assert type(value)==int
        assert value>0
        assert value<GAME_WIDTH
        self._ship.x=value

    def getShipBoltY(self):
        """
        Returns the y attribute of the bolt fired by the ship
        """

        return self.shipBolt.y

    def setShipBoltY(self,value):
        """
        Sets the y attribute of the bolt fired by the ship to value
        Parameter value: a new y attribute of the bolt fired by the ship
        Precondition: value is an integer between 0 and GAME_HEIGHT
        """

        assert type(value)==float
        assert value<GAME_HEIGHT
        assert value>0
        self.shipBolt.y=value

    def getShipHit(self):
        """
        Returns True if the ship has been hit by an alien bolt; False otherwise
        """

        return self.shipHit

    def setShipHit(self,value):
        """
        Sets the attribute for whether the ship has been hit by an alien bolt
        Parameter value: a value signifying if the ship has been hit by an
        alien bolt or not
        Precondition: value is a boolean variable
        """

        assert type(value)==bool
        self.shipHit=value

    def getContinue(self):
        """
        Returns True if the user has pressed the s key after the ship has been
        hit by an alien bolt, assuming that the user has not lost all their
        lives; False otherwise
        """

        return self.con

    def setContinue(self,value):
        """
        Sets the attribute for if the game can continue after the ship has been
        hit by an alien bolt
        Parameter value: a value signifying if the user has pressed the s key
        after the ship has been hit by an alien bolt, assuming that the user
        has not lost all their lives
        Precondition: value is a boolean variable
        """

        assert type(value)==bool
        self.con=value

    def getShipLives(self):
        """
        Returns the attribute lives from ship, which is a value containing the
        number of lives the ship has
        """

        return self._ship.lives

    def setShipLives(self,value):
        """
        Sets the lives attribute of the ship
        Parameter value: a new lives attribute of the ship
        Precondition: value is an integer>= 0 and <=SHIP_LIVES
        """
        assert type(value)==int
        assert value<=SHIP_LIVES
        assert value>=0
        self._ship.lives=value

    def getComplete(self):
        """
        Returns True if the game is complete, either by the all of the aliens
        being hit and removed from self._bolts or the ship has lost all of its
        lives; False otherwise
        """

        return self.complete

    def setComplete(self,value):
        """
        Sets the attribute for if the game is completed
        Parameter value: a value signifying if the game is complete, either by
        all of the aliens being hit and removed from self._bolts, or that the
        ship has lost all of its lives
        Precondition: value is a boolean variable
        """
        assert type(value)==bool
        self.complete=value

    def getScore(self):
        """
        Returns the attribute for the score of the game
        """

        return self.score

    def setScore(self,value):
        """
        Sets the score of the game
        Parameter value: a new value for the score of the game
        Precondition: value is an integer>= 0
        """
        assert type(value)==int
        assert value>=0
        self.score=value

    def getBarrierStrength(self):
        """
        Returns the attribute for the strength of the DEFENSE_LINE or the
        barrier
        """

        return self.barrierStrength

    def setBarrierStrength(self,value):
        """
        Sets the attribute for the strength of the DEFENSE_LINE or the
        barrier
        Parameter value: a new value for the strength of the DEFENSE_LINE or
        the barrier
        Precondition: value is an integer>= 0 and <=100
        """
        assert type(value)==int
        assert value>=0
        assert value<=100
        self.barrierStrength=value

    # INITIALIZER TO CREATE SHIP AND ALIENS
    def __init__(self):
        self._ship=Ship(x=390)
        self._ship.lives=SHIP_LIVES
        self.shipShoot=False
        self.shipBolt=0
        self.shipHit=False
        self.con=False
        self.complete=False
        self.score=0
        self.barrierStrength=100
        self.totalAliens=0
        self.pew1=Sound('pew1.wav')
        self.pew2=Sound('pew2.wav')
        self.blast1=Sound('blast1.wav')
        self.blast2=Sound('blast2.wav')
        self.blast3=Sound('blast3.wav')
        self._bolts=[]
        self.steps = 0
        self.alienShoot = False
        self._aliens=[[]]
        self._time = 0
        self.direction = 'right'
        self.givenSteps = random.randint(1,BOLT_RATE)

        self.drawAliens()
        
        # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def alienUpdate(self,dt):
        if(self.shipHit==False):
            bottom = self.pickRandomAlien()
            if bottom is not None:
                bolt_x = bottom.x
            if self._time > ALIEN_SPEED:
                if self.direction == 'right' and (self._aliens[0][len(self.
                _aliens[0])-1] is None or self._aliens[0][len(self._aliens[0])
                -1].x != GAME_WIDTH - ALIEN_H_SEP - 0.5*ALIEN_WIDTH):
                    self.moveAliensRight()
                    if bottom is not None:
                        self.createAlienBolt(bottom,bolt_x)
                    self._time=0

                if self.direction == 'left' and (self._aliens[0][0] is None or
                self._aliens[0][0].x != ALIEN_H_SEP+0.5*ALIEN_WIDTH):
                    self.moveAliensLeft()
                    if bottom is not None:
                        self.createAlienBolt(bottom,bolt_x)
                    self._time=0

                if self.findNonemptyRight() is None or self.findNonemptyRight().x>=GAME_WIDTH - ALIEN_H_SEP - 0.5*ALIEN_WIDTH or self.findNonemptyLeft() is None or self.findNonemptyLeft().x <= ALIEN_H_SEP + 0.5*ALIEN_WIDTH:
                    self.moveAliensDown()
                    if bottom is not None:
                        self.createAlienBolt(bottom,bolt_x)
                    self._time=0

                    if self.direction == 'right':
                        self.direction = 'left'
                    else: self.direction = 'right'

            if self.shipBolt != 0:
                self.checkAlienCollision()

            self._time += dt

    def shipUpdate(self,input):
        """
        Runs multiple times during the game. It moves the ship, fires ship
        bolts, checks for collisions between alien bolts and the ship,
        determines if the game is over or paused, and resumes the game if
        game was paused but the user pressed s
        """
        self.checkDefense()
        if(self.totalAliens==0):
            self.setShipHit(True)
            self.setComplete(True)
        if self._bolts!=[]:
            for bolts in self._bolts:
                if Ship.shipCollision(int(bolts.x),int(bolts.y),int(self.
                getShipX())):
                    if(self.getShipLives()==1):
                        self.blast3.play()
                    else:
                        self.blast2.play()
                    self.setShipHit(True)
        if(self.getShipHit()==False):
            self.shipMoving(input)
        if(self.getShipHit()==True):
            self.shipBolt=0
            self.shipShoot=False
            self._bolts=[]
            if input.is_key_down('s'):
                self.setShipLives(self.getShipLives()-1)
                if(self.getShipLives()==1):
                    self.setComplete(True)
                self.setShipHit(False)
                self.setContinue(True)
    
    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self,view):
        """
        Draws the ship, aliens, defensive line, alien bolts, and ship bolt
        game objects to the view
        Parameter view: an attribute that references to the window
        Precondition: view is a model controller
        """
        for row in self._aliens:
            for alien in row:
                if alien is not None:
                    alien.draw(view)
        self.drawShip().draw(view)
        self.drawDefensive().draw(view)
        if(self.shipShoot==True):
            self.drawShipBolt().draw(view)
            if(self.getShipHit()==False):
                self.moveShipBolts()
        if(self.getShipHit()==False):
            for bolt in self._bolts:
                bolt.draw(view)
                self.moveAlienBolt(bolt)
    
    # HELPER METHODS FOR COLLISION DETECTION
    def drawShip(self):
        """
        Draws the ship object to view
        """

        return self._ship

    def drawDefensive(self):
        """
        Draws the defense line to view
        """

        self._dline=GPath(points=[0,DEFENSE_LINE,GAME_WIDTH,DEFENSE_LINE],
        linewidth=1,linecolor='#65686D')
        return self._dline

    def drawShipBolt(self):
        """
        Draws the bolt fired by the ship to view
        """

        return self.shipBolt

    def moveShipBolts(self):
        """
        Moves the y attribute of the bolt fired by the ship using getters and
        setters
        """

        if(self.getShipBoltY()<GAME_HEIGHT-BOLT_HEIGHT):
            self.setShipBoltY(self.getShipBoltY()+BOLT_SPEED)
        else:
            self.shipBolt=0
            self.shipShoot=False

    def checkDefense(self):
        """
        Checks to see if any of the aliens have crossed the DEFENSE_LINE
        """
        self.totalAliens=0
        for row in range(ALIEN_ROWS):
            for col in range(ALIENS_IN_ROW):
                if(self._aliens[row][col]!=None and self._aliens[row][col].
                y<DEFENSE_LINE):
                    self.setShipLives(1)
                    self.setComplete(True)
                    self.setShipHit(True)
                if(self._aliens[row][col]!=None):
                    self.totalAliens+=1

    def shipMoving(self,input):
        """
        Completes all of the actions when the ship is not hit by an alien bolt:
        moving the ship, firing the ship bolts, and playing the audio
        Parameter input: an attribute that is called through update
        Precondition: input is an instance of GInpup
        """

        self.setContinue(False)
        if input.is_key_down('left'):
            self._ship.moveShipLeft()
        if input.is_key_down('right'):
            self._ship.moveShipRight()
        if input.is_key_down('up'):
            self.shipShoot=True
        if(self.shipShoot):
            if(self.shipBolt==0):
                if self.getBarrierStrength()>=10:
                    self.setBarrierStrength(self.getBarrierStrength()-10)
                self.pew1.play()
                self.shipBolt=Bolt(velocity=BOLT_SPEED,x=self.getShipX(),y=92)

    def moveAlienBolt(self,bolt):
        """
        Moves the alien bolts down the screen
        Precondition: bolt is a Bolt object fired by an alien
        """
        if self.getBarrierStrength()>=10 and bolt.y<DEFENSE_LINE:
            self._bolts.remove(bolt)
            self.setBarrierStrength(self.getBarrierStrength()-10)
        elif bolt.y > BOLT_HEIGHT:
            bolt.y -= BOLT_SPEED
        else:
            self._bolts.remove(bolt)
            self.alienShoot = False

    def drawAliens(self):
        """
        Draws the aliens
        """
        x_alien = ALIEN_H_SEP + 0.5 * ALIEN_WIDTH
        y_alien = GAME_HEIGHT - ALIEN_CEILING - ALIEN_ROWS*ALIEN_HEIGHT - (ALIEN_ROWS - 1)*ALIEN_V_SEP
        for row in range(ALIEN_ROWS):
            self._aliens.append([])
            for col in range(ALIENS_IN_ROW):
                if row % 6 == 4 or row % 6 == 5:
                    self._aliens[row].append(GImage(x = x_alien, y = y_alien, source = ALIEN_IMAGES[2], width = ALIEN_WIDTH, height = ALIEN_HEIGHT))
                if row % 6 == 2 or row % 6 == 3:
                    self._aliens[row].append(GImage(x = x_alien, y = y_alien, source = ALIEN_IMAGES[1], width = ALIEN_WIDTH, height = ALIEN_HEIGHT))
                if row % 6 == 0 or row % 6 == 1:
                    self._aliens[row].append(GImage(x = x_alien, y = y_alien, source = ALIEN_IMAGES[0], width = ALIEN_WIDTH, height = ALIEN_HEIGHT))
                x_alien += ALIEN_H_SEP + ALIEN_WIDTH
            y_alien = y_alien + ALIEN_V_SEP + ALIEN_HEIGHT
            x_alien = ALIEN_H_SEP + 0.5 * ALIEN_WIDTH

        del self._aliens[-1]

    def pickRandomAlien(self):
        """
        Picks the alien that will shoot the next bolt
        Returns: an Alien object
        """
        flag = -1
        while flag != 0:
            col = random.randint(0,len(self._aliens[ALIEN_ROWS-1])-1)
            number_none = 0
            for row in range(len(self._aliens)-1):
                if self._aliens[row][col] == None:
                    number_none += 1
            if number_none != len(self._aliens):
                flag += 1

        done = 'no'
        row = 0
        while done == 'no' and row < len(self._aliens):
            bottom = self._aliens[row][col]
            if bottom == None:
                row += 1
            else:
                done = 'yes'

        if bottom is not None:
            return bottom
        else:
            self.pickRandomAlien()

    def moveAliensRight(self):
        """
        Moves the aliens to the right
        """
        for row in self._aliens:
            for alien in row:
                if alien is not None:
                    alien.x += ALIEN_H_WALK
        self.steps +=1

    def createAlienBolt(self,bottom,bolt_x):
        """
        Creates an Bolt object to be shot from an alien and appends it to the list of bolts
        """

        if self.steps == self.givenSteps:
            self.pew2.play()
            self.alienShoot = True
            if bottom is not None:
                self._bolts.append(Bolt(-BOLT_SPEED, x = bolt_x, y = bottom.y - 0.5*ALIEN_HEIGHT))
                self.steps = 0
                self.givenSteps = random.randint(1,BOLT_RATE)

    def moveAliensLeft(self):
        """
        Moves the aliens to the left
        """
        for row in self._aliens:
            for alien in row:
                if alien is not None:
                    alien.x -= ALIEN_H_WALK
        self.steps +=1

    def moveAliensDown(self):
        """
        Moves aliens down
        """
        for row in self._aliens:
            for alien in row:
                if alien is not None:
                    alien.y -= ALIEN_V_WALK
        self.steps +=1

    def checkAlienCollision(self):
        """
        Checks if there is an alien in the position that was shot at and if
        so, changes it to None
        """
        for row in range(ALIEN_ROWS):
            for col in range(ALIENS_IN_ROW):
                if Alien.alienCollision(self,self.shipBolt,self._aliens[row]
                [col]) == True:
                    score=self.getScore()
                    self.setScore(score+(ALIEN_ROWS-row)*10)
                    self.blast1.play()
                    self._aliens[row][col] = None
                    self.shipBolt = 0
                    self.shipShoot = False

    def findNonemptyRight(self):
        """
        Finds and returns the position of the rightmost Alien
        Returns: an Alien object
        """
        col = ALIENS_IN_ROW -1
        while col >=0:
            for row in range(len(self._aliens)):
                if self._aliens[row][col] is not None:
                    return self._aliens[row][col]
            col -= 1

    def findNonemptyLeft(self):
        """
        Finds and returns the position of the leftmost Alien
        Returns: an Alien object
        """
        col = 0
        while col < ALIENS_IN_ROW:
            for row in range(len(self._aliens)):
                if self._aliens[row][col] is not None:
                    return self._aliens[row][col]
            col += 1
