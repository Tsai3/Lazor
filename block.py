import numpy as np
from itertools import permutations

class Block:
    '''
    This class carries creates a Block objecct.
   
    '''

    def __init__(self, x_position, y_position, type):
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
    
if __name__ == "__main__":

    Block1 = Block(3,5,"A")
    
    print(Block1())
    print(Block1.get_x())
    
    
    

        
  