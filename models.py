class Ship(GImage):
    """
    A class to represent the game ship.
    """

    # INITIALIZER TO CREATE A NEW SHIP
    def __init__(self,x,width=SHIP_WIDTH,height=SHIP_HEIGHT,bottom=SHIP_BOTTOM
    ,movement=SHIP_MOVEMENT):
        super().__init__(x = x,width = SHIP_WIDTH, height = SHIP_HEIGHT,
        bottom=SHIP_BOTTOM,movement=SHIP_MOVEMENT,source='ship.png')
    
    # METHODS TO MOVE THE SHIP AND CHECK FOR COLLISIONS
    def moveShipRight(self):
        """
        Moves the x attribute of the ship to the right but doesn't let it
        cross the boundaries of the game
        """

        xpos=self.x
        if(xpos>GAME_WIDTH-(SHIP_WIDTH)/2):
            return 778
        else:
            self.x=xpos+SHIP_MOVEMENT

    def moveShipLeft(self):
        """
        Moves the x attribute of the ship to the left but doesn't let it
        cross the boundaries of the game
        """

        xpos=self.x
        if(xpos<(SHIP_WIDTH)/2):
            return 22
        else:
            self.x=xpos-SHIP_MOVEMENT

    def shipCollision(bolt_x,bolt_y,ship_x):
        """
        Returns True if the alien bolt collides with ship

        This method returns False if bolt was not fired by the alien.

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        bolt_x=bolt_x+BOLT_WIDTH
        if bolt_x>ship_x-(SHIP_WIDTH/2) and bolt_x<(ship_x+(SHIP_WIDTH/2)):
            if bolt_y>SHIP_BOTTOM and bolt_y<(SHIP_BOTTOM+SHIP_HEIGHT):
                return True
        return False

class Alien(GImage):
    """
    A class to represent a single alien.
    """
    
    # INITIALIZER TO CREATE AN ALIEN
    def __init__(self, x, y, source, width = ALIEN_WIDTH, height = ALIEN_HEIGHT):
        super().__init__(x = x, y = y, source = source, width = ALIEN_WIDTH, height = ALIEN_HEIGHT)
    
    # METHOD TO CHECK FOR COLLISION
    def alienCollision(self,bolt,alien):
        """
        Returns True if the player bolt collides with this alien

        This method returns False if bolt was not fired by the player.

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        if bolt != 0  and bolt is not None and alien is not None and bolt.x>(alien.x - ALIEN_WIDTH/2) and bolt.x<(alien.x+ALIEN_WIDTH/2):
            if bolt.y>alien.y and bolt.y<alien.y+ALIEN_HEIGHT:
                return True
        return False

class Bolt(GRectangle):
    """
    A class representing a laser bolt.
    """

    # INITIALIZER TO SET THE VELOCITY
    def __init__(self,velocity,x,y,width=BOLT_WIDTH,height=BOLT_HEIGHT):
        super().__init__(x=x,y=y,height=height,width=width,fillcolor='gray')
        self._velocity=velocity
