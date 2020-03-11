
    
class Player():
    '''a player object that represents the player'''
    
    def __init__(self):
        '''warming up the class'''
        self.seeds = ['mushroom', 'tomato']
        self.playersName = "player1"
    
    def setPlayersName(self, name):
        '''set the player's name'''
        
        self.playersName = name
    
    def getPlayersName(self):
        '''return the current player's name'''
        
        return self.playersName
    
    def setSeedToPlant(self, seed):
        '''retrieve the player's seed'''
        
        self.seedToPlant = seed
    
    def plant(self):
        '''a player can plant a seed'''
        
        print("planting {0}...".format(self.seedToPlant))

    def planting(self):
        '''planting something'''
        
        print("{0} planted!".format(self.seedToPlant))    
