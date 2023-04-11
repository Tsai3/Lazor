import numpy as np
from itertools import permutations

"""
Saturday, April 8, 2023, 11:18:29 PM
@author: Luke
"""

class Block:
    '''
    This class carries creates a Block object.
    
    It has attributes for each loacation of the walls, it's type, and it's position in the board matrix
   
    '''

    def __init__(self, y_position, x_position, type): #has to be reversed as we view the coordinate system differently to how numpy does
        '''
        
        '''
        self.LeftWall = (2*x_position,2*y_position+1)
        self.RightWall = (2*(x_position+1),2*y_position+1)
        self.TopWall = (2*x_position+1,2*y_position)
        self.BottomWall = (2*x_position+1,2*(y_position+1))
        self.type = type
        self.x_position = x_position
        self.y_position = y_position

    def get_Left_Wall(self):
        return self.LeftWall
    def get_Right_Wall(self):
        return self.RightWall
    def get_Top_Wall(self):
        return self.TopWall
    def get_Bottom_Wall(self):
        return self.BottomWall
    def get_Type(self):
        return self.type
    
    def get_x(self):
        return self.x_position
    def get_y(self):
        return self.y_position
    
    def __call__(self):
        return self.LeftWall, self.RightWall, self.TopWall, self.BottomWall, self.type
    


        
  