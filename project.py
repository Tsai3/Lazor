import numpy as np
import copy
from sympy.utilities.iterables import multiset_permutations

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
    

class Board:
    '''
    This class carries creates a Board object.
    
    This class contains attributes of the 2D board matrix, a list of A, B, and C Blocks, a list of lasers, their directions, and points.
   
    '''
    
    
    def __init__(self, board_matrix, A, B, C, lasers, lasers_dir, points):
        '''
        Initializes the Board object that takes in a matrix of board symbols, strings of A blocks, B blocks and C blocks, strings of lasers and srrings of points
        '''
        self.board_matrix = board_matrix
        self.A = A
        self.B = B
        self.C = C
        self.lasers = lasers
        self.lasers_dir = lasers_dir
        self.points = points
        
    def __call__(self):
        return self.board_matrix, self.A , self.B, self.C, self.lasers, self.points

    def get_Board_Matrix(self):
        return self.board_matrix
    
    def get_A_Blocks(self):
        number_of_A = 0
        if self.A:
            number_of_A = int(self.A[0][2])
            
        return number_of_A
    
    def get_B_Blocks(self):
        number_of_B = 0
        if self.B:
            number_of_B = int(self.B[0][2])
            
        return number_of_B
    
    def get_C_Blocks(self):
        number_of_C = 0
        if self.C:
            number_of_C = int(self.C[0][2])
            
        return number_of_C
    
    def get_Lasers(self):
        return self.lasers
    
    def get_Lasers_dir(self):
        return self.lasers_dir
    
    def get_points(self):
        return self.points
    
    def add_Lazor(self,x_coordinate, y_coordinate,vx_coordinate, vy_coordinate):
        self.lasers.add((x_coordinate, y_coordinate,vx_coordinate, vy_coordinate))
       
            
class Matrix:
    '''
    This is just a quick class that I used to generate the matrix for laser behavior
    when Luke genere a function that read the board and translate that into matrix, 
    I will just adope that matrix format Luke has
    Matrix code:
      x = no block allowed
      o = blocks allowed
      A = fixed reflect block
      B = fixed opaque block
      C = fixed refract block
      L = laser
      color on_red ('41') = laser path
      T = target needs laser intersect
    '''
    def __init__(self, x, y):
        self.matrix = [['o' for i in range(x)] for j in range(y)]
        self.colors = [['37' for i in range(x)] for j in range(y)]
        self.x = x
        self.y = y
        
    def get_element(self, a, b):
        return self.matrix[b][a]

    def set_target(self, a, b):
        self.matrix[b][a] = 'T'
    
    def set_laser(self, a, b):
        self.matrix[b][a] = 'L'
    
    def set_reflect(self, a, b):
        self.matrix[b][a] = 'A'
    
    def set_opaque(self, a, b):
        self.matrix[b][a] = 'B'
        
    def set_refract(self, a, b):
        self.matrix[b][a] = 'C'
    
    def set_color(self, x, y, color):
        self.colors[y][x] = color
    
    def max_column(self):
        return (self.x)

    def max_row(self):
        return (self.y)
    
    def get_colored_array(self):
        
        colored_arr = []
        color_grid = self.colors
        row_index = 0
        for row in (color_grid):
            col_index = 0
            for col in (row):
                if col == '41':
                    colored_arr.append((col_index,row_index))
                col_index+=1
            row_index+=1
        
        return colored_arr
    
    def __str__(self):
        result = ""
        for row in self.matrix:
            result += " ".join(str(elem) for elem in row) + "\n"
        return result
    
    def print_matrix_with_indices(self):
        print("\x1b[45m  ", end="")
        for i in range(self.x):
            print(i, end=" ")
        print("\033[0m")
        for i in range(self.y):
            print("\033[0;45m{}\033[0m".format(i), end=" ")
            for j in range(self.x):
                print("\033[{}m{}\033[0m".format(self.colors[i][j], self.matrix[i][j]), end=" ")
            print()
    

def set_targets(matrix, target_list):
    '''  
    Parameters
    ----------
    matrix : self-defined class Matrix
            this is the class Matrix that record the board info
    target : list
            this is a list contains positions (targets) that needs laser intersect 
    Returns
    -------
    None.
    '''
    for position in target_list:
        x,y = position
        matrix.set_target(x,y)
        
def set_laser(matrix, laser_list):
    '''  
    Parameters
    ----------
    matrix : self-defined class Matrix
            this is the class Matrix that record the board info
    target : list
            this is a list contains the positions where laser starts 
    Returns
    -------
    None.
    '''
    for position in laser_list:
        x,y = position
        matrix.set_laser(x,y)

def set_reflect(matrix, reflect_list):
    '''  
    Parameters
    ----------
    matrix : self-defined class Matrix
            this is the class Matrix that record the board info
    reflect : list
            this is a list contains positions covered by reflect block(s)
    Returns
    -------
    None.
    '''
    for position in reflect_list:
        x,y = position
        matrix.set_reflect(x,y)

def set_opaque(matrix, opaque_list):
    '''  
    Parameters
    ----------
    matrix : self-defined class Matrix
            this is the class Matrix that record the board info
    opaque_list : list
            this is a list contains positions covered by opaque block(s)
    Returns
    -------
    None.
    '''
    for position in opaque_list:
        x,y = position
        matrix.set_opaque(x,y)

def set_refract(matrix, refract_list):
    '''  
    Parameters
    ----------
    matrix : self-defined class Matrix
            this is the class Matrix that record the board info
    refract_list : list
            this is a list contains positions covered by refract block(s)
    Returns
    -------
    None.
    '''
    for position in refract_list:
        x,y = position
        matrix.set_refract(x,y)

def laser_contact_side(matrix, laser_pos, laser_dir):
    '''
    This function determines which side of the block does the laser hit
    (this info is needed to determined the laser direction when it hit the block)
    
    Parameters
    ----------
    matrix : TYPE
        DESCRIPTION.
    Returns
    -------
    which side of the block does the laser hit (top, down, left, left)
    '''
    m = matrix
    x, y = laser_pos     
    dx, dy = laser_dir
    next_pos = (x+dx, y+dy)
    nx, ny = next_pos
    side = str()
    
    
    look_at_Far_Walls = True
    look_at_Near_Walls = True
    if nx-2 < 0  or nx + 2 >= (m.max_column())  or ny-2 < 0 or  ny + 2 >= (m.max_row()):
        look_at_Far_Walls = False
    if nx-1 < 0  or nx + 1 >= (m.max_column())  or ny-1 < 0 or  ny + 1 >= (m.max_row()):
        look_at_Near_Walls = False
    

    if look_at_Far_Walls == False and look_at_Near_Walls == False:
        side = 'top'
        
    elif look_at_Far_Walls == False and look_at_Near_Walls == True:
        if m.get_element(nx+1,ny) != 'o' and m.get_element(nx-1,ny) != 'o' and m.get_element(nx,ny-1) != 'o':
            side = 'down'
        elif m.get_element(nx+1,ny) != 'o' and m.get_element(nx-1,ny) != 'o' and m.get_element(nx,ny+1) != 'o':
            side = 'top'
        elif m.get_element(nx+1,ny) != 'o'  and m.get_element(nx,ny+1) != 'o' and m.get_element(nx,ny-1) != 'o':
            side = 'left'
        elif m.get_element(nx-1,ny) != 'o'  and m.get_element(nx,ny+1) != 'o' and m.get_element(nx,ny-1) != 'o':
            side = 'right'
    else:
        if m.get_element(nx+1,ny) != 'o' and m.get_element(nx-1,ny) != 'o' and m.get_element(nx,ny-1) != 'o' and m.get_element(nx,ny-2) != 'o':
            side = 'down'
        elif m.get_element(nx+1,ny) != 'o' and m.get_element(nx-1,ny) != 'o' and m.get_element(nx,ny+1) != 'o' and m.get_element(nx,ny+2) != 'o':
            side = 'top'
        elif m.get_element(nx+1,ny) != 'o' and m.get_element(nx+2,ny) != 'o' and m.get_element(nx,ny+1) != 'o' and m.get_element(nx,ny-1) != 'o':
            side = 'left'
        elif m.get_element(nx-1,ny) != 'o' and m.get_element(nx-2,ny) != 'o' and m.get_element(nx,ny+1) != 'o' and m.get_element(nx,ny-1) != 'o':
            side = 'right'
        else:
            side = 'No Contact'
    
    return side    
    
def laser_1_step(matrix, laser_pos, laser_dir):
    '''
    Parameters
    ----------
    matrix : self-defined Class Matrix
             this is the class Matrix that record the board info
    laser_start : tuple(x,y)
             this is the position of the laser source
    laser_direction : TYPE
             this is the direction of the laser (as the 1-step movement)
    
    x = no block allowed
    o = blocks allowed
    A = fixed reflect block
    B = fixed opaque block
    C = fixed refract block
    L = laser
    color on_red ('41') = laser path
    T = target needs laser intersect
    
    Returns
    (1_step valid, laser_behavior (pass, reflect, refract, inside refract, stop), next_pos, next_dir, new_direction) 
    
    -------
    None.
    '''
    m = matrix
    x, y = laser_pos
    m.set_color(x, y, '41')
    dx, dy = laser_dir
    next_pos = (x + dx, y + dy)
    n_dx = int()
    n_dy = int()
    next_dir =(n_dx, n_dy)
    
    # if meet reflect box, a new direction will be generated
    nls_dx = int()
    nls_dy = int()
    new_dir=(nls_dx, nls_dy)

    
    #check if next_position is in matrix
    if next_pos[0] <0 or next_pos[0] > (m.max_column()-1) or next_pos[1] <0 or next_pos[1] > (m.max_row()-1):
        return False
    
    #check if next_position is o
    elif m.get_element(x+dx, y+dy) == 'o' or m.get_element(x+dx, y+dy) == 'L'or m.get_element(x+dx, y+dy) == 'T' or m.get_element(x+dx, y+dy) == 'x':
        m.set_color(x+dx, y+dy, '41')
        next_dir = laser_dir
        return True, 'pass', next_pos, laser_dir
    
    #Check the walls I'm next to and the next position I'm going to in order to figure out If laser starts in block
    
    ### All Walls Checkable ###
    
    elif x-1 >= 0 and x+1 < (m.max_column()) and y -1 >=0 and y+1 < (m.max_row()) and x-dx >= 0 and x+dx < (m.max_column()) and y -dy >=0 and y+dy < (m.max_row()):
        # Is literally everywhere around me a relect block or opaque block
        if  (m.get_element(x+dx,y+dy) == 'A') and (m.get_element(x,(y+1)) == 'A' or m.get_element(x,(y+1)) == 'B') and (m.get_element(x,(y-1)) == 'A' or m.get_element(x,(y-1)) == 'B') and (m.get_element((x+1),(y)) =="A" or m.get_element((x+1),(y)) =="B") and (m.get_element((x-1),(y)) == 'A' or m.get_element((x-1),(y)) == 'B'): 
            next_dir = (0, 0)
            next_pos = (x + 0, y + 0)
            return True, 'stop', next_pos, next_dir
        
        # Is the Laser on the left or right edge of a block and is it trying to go to a reflect wall through itself.
        elif m.get_element(x+dx,y+dy) == 'A' and (m.get_element(x,(y+1)) == 'A' or m.get_element(x,(y+1)) == 'B') and (m.get_element(x,(y-1)) == 'A' or m.get_element(x,(y-1)) == 'B') and  m.get_element((x+dx),(y))=='A': 
            next_dir = (-dx, dy)
            next_pos = (x - dx, y + dy)
            return True, 'reflect', next_pos, next_dir 
    
        # Is the Laser on the top or bottom edge of a block and is it trying to go to a reflect wall through itself.
        elif m.get_element(x+dx,y+dy) == 'A' and (m.get_element((x+1),(y)) =="A" or m.get_element((x+1),(y)) =="B") and (m.get_element((x-1),(y)) == 'A' or m.get_element((x-1),(y)) == 'B') and m.get_element((x),(y+dy)) == 'A': 

            next_dir = (dx, -dy)
            next_pos = (x + dx, y - dy)
            return True, 'reflect', next_pos, next_dir
        
        # Is the Laser on the left or right edge of a block and is it trying to go to a reflect wall NOT through itself.
        elif m.get_element(x+dx,y+dy) == 'A' and (m.get_element(x,(y+1)) == 'A' or m.get_element(x,(y+1)) == 'B') and (m.get_element(x,(y-1)) == 'A' or m.get_element(x,(y-1)) == 'B') and  m.get_element((x+dx),(y)!='A'): 

            m.set_color(x+dx, y+dy, '41')
            side = laser_contact_side(matrix, laser_pos, laser_dir)
            if side == 'top' or side == 'down':
                next_dir = (dx, -dy)
            if side == 'left' or side == 'right':
                next_dir = (-dx, dy)
            return True, 'reflect', next_pos, next_dir

        # Is the Laser on the top or bottom edge of a block and is it trying to go to a reflect wall NOT through itself.
        elif m.get_element(x+dx,y+dy) == 'A' and (m.get_element((x+1),(y)) =="A" or m.get_element((x+1),(y)) =="B") and (m.get_element((x-1),(y)) == 'A' or m.get_element((x-1),(y)) == 'B') and m.get_element((x),(y+dy)) != 'A': 
            
            
            m.set_color(x+dx, y+dy, '41')
            side = laser_contact_side(matrix, laser_pos, laser_dir)
            if side == 'top' or side == 'down':
                next_dir = (dx, -dy)
            if side == 'left' or side == 'right':
                next_dir = (-dx, dy)
            return True, 'reflect', next_pos, next_dir
            

        
        
    
        # Is the Laser on the left or right edge of a block and is it trying to go to an opaque block through itself
        elif m.get_element(x+dx,y+dy) == 'B' and (m.get_element(x,(y+1)) == 'A' or m.get_element(x,(y+1)) == 'B') and (m.get_element(x,(y-1)) == 'A' or m.get_element(x,(y-1)) == 'B') and  m.get_element((x+dx),(y))=='B': 
            next_dir = (0, 0)
            next_pos = (x - 0, y + 0)
            return True, 'stop', next_pos, next_dir
         
        # Is the Laser on the top or bottom edge of a block and is it trying to go to an opaque block through itself
        
        elif m.get_element(x+dx,y+dy) == 'B' and (m.get_element((x+1),(y)) =="A" or m.get_element((x+1),(y)) =="B") and (m.get_element((x-1),(y)) == 'A' or m.get_element((x-1),(y)) == 'B') and m.get_element((x),(y+dy)) == 'B':         
            next_dir = (0, 0)
            next_pos = (x + 0, y - 0)
            return True, 'stop', next_pos, next_dir
        
        
        
        # Is the Laser on the left or right edge of a block and is it trying to go to a opaque wall NOT through itself.
        elif m.get_element(x+dx,y+dy) == 'B' and (m.get_element(x,(y+1)) == 'A' or m.get_element(x,(y+1)) == 'B') and (m.get_element(x,(y-1)) == 'A' or m.get_element(x,(y-1)) == 'B') and  m.get_element((x+dx),(y)!='B'): 
            m.set_color(x+dx, y+dy, '41')
            next_dir =(0, 0)
            return True, 'stop', next_pos, next_dir, new_dir
    
        # Is the Laser on the top or bottom edge of a block and is it trying to go to a opaque wall NOT through itself.
        elif m.get_element(x+dx,y+dy) == 'B' and (m.get_element((x+1),(y)) =="A" or m.get_element((x+1),(y)) =="B") and (m.get_element((x-1),(y)) == 'A' or m.get_element((x-1),(y)) == 'B') and m.get_element((x),(y+dy)) != 'B': 
            
            m.set_color(x+dx, y+dy, '41')
            next_dir =(0, 0)
            return True, 'stop', next_pos, next_dir, new_dir
        

    
        # Is the Laser on the left or right edge of a block and is it trying to go through a refract block
        elif (m.get_element(x,(y+1)) != 'o' and m.get_element(x,(y-1)) != 'o' and m.get_element(x+dx,y+dy)) == 'C' and m.get_element((x),(y+1)) ==m.get_element((x),(y-1)): 
            # print('help-7')
    
            side = 'left'
            if side == 'top' or side == 'down':
                next_dir = (dx, -dy)
            if side == 'left' or side == 'right':
                next_dir = (-dx, dy)
            m.set_color(x-dx, y+dy, '41')
            next_pos = (x - dx, y + dy)
            new_dir = copy.copy(laser_dir)
            og_pos = (x+dx,y+dy)
            return True, 'retract', next_pos, next_dir, new_dir, og_pos  
            
        # Is the Laser on the top or bottom edge of a block and is it trying to go through a refract block
        elif (m.get_element((x+1),(y)) != 'o' and m.get_element((x-1),(y)) != 'o' and m.get_element(x+dx,y+dy)) == 'C' and m.get_element((x+1),(y)) ==m.get_element((x-1),(y)): 
            # print('help-8')
            if m.get_element(x+dx, y+dy) == 'C':
                side = 'top'
                if side == 'top' or side == 'down':
                    next_dir = (dx, -dy)
                if side == 'left' or side == 'right':
                    next_dir = (-dx, dy)    
                
                m.set_color(x+dx, y-dy, '41')
                next_pos = (x + dx, y - dy)
                new_dir = laser_dir
                og_pos = (x+dx,y+dy)
                return True, 'retract', next_pos, next_dir, new_dir, og_pos
        # when laser meets reflect block, A
        elif m.get_element(x+dx,y+dy) == 'A':
            # print('help-9')
            m.set_color(x+dx, y+dy, '41')
            side = laser_contact_side(matrix, laser_pos, laser_dir)
        
            if side == 'top' or side == 'down':
                next_dir = (dx, -dy)
            if side == 'left' or side == 'right':
                next_dir = (-dx, dy)
            # print(next_pos, next_dir)
            return True, 'reflect', next_pos, next_dir
            
        # when laser meets opaque, B
        elif m.get_element(x+dx, y+dy) == 'B':
            # print('help-10')
            m.set_color(x+dx, y+dy, '41')
            next_dir =(0, 0)
            return True, 'stop', next_pos, next_dir, new_dir
        
        # when laser meets refract block, C
        elif m.get_element(x+dx, y+dy) == 'C':
            # print('help-11')
            # print('re')
            m.set_color(x+dx, y+dy, '41')
            if m.get_element(x, y) == 'C':
                next_dir = laser_dir
                return True, 'inside refract', next_pos, next_dir
            else:
                side = laser_contact_side(matrix, laser_pos, laser_dir)
                if side == 'top' or side == 'down':
                    next_dir = (dx, -dy)
                if side == 'left' or side == 'right':
                    next_dir = (-dx, dy)    
                new_dir = laser_dir
                og_pos = (x+dx,y+dy)
                return True, 'retract', next_pos, next_dir, new_dir, og_pos 
    
    ### Bottom Row ###
    
    elif y+1 == (m.max_row()):
        
        # (print('bottom'))
        # Is the Laser on the top or bottom edge of a block and is it trying to go to a reflect wall through itself.
        if m.get_element(x,y+dy) != 'o' and m.get_element((x+1),(y)) != 'o' and m.get_element((x-1),(y)) != 'o' and m.get_element((x),(y+dy)) == 'A': 
            # print('help-2')
            # print(m.get_element((x-1),(y)) != m.get_element((x+1),(y)))
            next_dir = (0, 0)
            next_pos = (x + 0, y + 0)
            return True, 'stop', next_pos, next_dir
        
        
      
         
        # Is the Laser on the top or bottom edge of a block and is it trying to go to an opaque block through itself
        elif m.get_element(x+dx,y+dy) == 'B' and (m.get_element((x+1),(y)) =="A" or m.get_element((x+1),(y)) =="B") and (m.get_element((x-1),(y)) == 'A' or m.get_element((x-1),(y)) == 'B') and m.get_element((x),(y+dy)) == 'B': 
            # print('help-6')
        
            next_dir = (0, 0)
            next_pos = (x + 0, y - 0)
            return True, 'stop', next_pos, next_dir
        
        
        
    
        # Is the Laser on the top or bottom edge of a block and is it trying to go to a opaque wall NOT through itself.
        elif m.get_element(x+dx,y+dy) == 'B' and (m.get_element((x+1),(y)) =="A" or m.get_element((x+1),(y)) =="B") and (m.get_element((x-1),(y)) == 'A' or m.get_element((x-1),(y)) == 'B') and m.get_element((x),(y+dy)) != 'B': 
            
            m.set_color(x+dx, y+dy, '41')
            next_dir =(0, 0)
            return True, 'stop', next_pos, next_dir, new_dir
    
            
            
        # Is the Laser on the top or bottom edge of a block and is it trying to go through a refract block
        elif (m.get_element((x+1),(y)) != 'o' and m.get_element((x-1),(y)) != 'o' and m.get_element(x+dx,y+dy)) == 'C' and m.get_element((x+1),(y)) ==m.get_element((x-1),(y)): 
            # print('help-8')
            if m.get_element(x+dx, y+dy) == 'C':
                side = 'top'
                if side == 'top' or side == 'down':
                    next_dir = (dx, -dy)
                if side == 'left' or side == 'right':
                    next_dir = (-dx, dy)    
                
                m.set_color(x+dx, y-dy, '41')
                next_pos = (x + dx, y - dy)
                new_dir = laser_dir
                og_pos = (x+dx,y+dy)
                return True, 'retract', next_pos, next_dir, new_dir, og_pos
            
        # Is the Laser on the top or bottom edge of a block and is it trying to go to a reflect wall NOT through itself.
        elif m.get_element(x+dx,y+dy) == 'A' and m.get_element((x+1),(y)) != 'o' and m.get_element((x-1),(y)) != 'o' and m.get_element((x),(y+dy)) != 'A': 
            # print('help-4')
            
            m.set_color(x+dx, y+dy, '41')
            side = laser_contact_side(matrix, laser_pos, laser_dir)
            # print(side)
            if side == 'top' or side == 'down':
                next_dir = (dx, -dy)
            if side == 'left' or side == 'right':
                next_dir = (-dx, dy)
            # print(next_pos, next_dir)
            return True, 'reflect', next_pos, next_dir
            
            # # print(m.get_element((x-1),(y)) != m.get_element((x+1),(y)))
            # # next_dir = (dx, -dy)
            # # next_pos = (x + dx, y + dy)
            # return True, 'reflect', next_pos, next_dir
            
        # when laser meets reflect block, A
        elif m.get_element(x+dx,y+dy) == 'A':
                m.set_color(x+dx, y+dy, '41')
                side = laser_contact_side(matrix, laser_pos, laser_dir)
            
                if side == 'top' or side == 'down':
                    next_dir = (dx, -dy)
                if side == 'left' or side == 'right':
                    next_dir = (-dx, dy)
                return True, 'reflect', next_pos, next_dir
            
        # when laser meets opaque, B
        elif m.get_element(x+dx, y+dy) == 'B':
            m.set_color(x+dx, y+dy, '41')
            next_dir =(0, 0)
            return True, 'stop', next_pos, next_dir, new_dir
        
        # when laser meets refract block, C
        elif m.get_element(x+dx, y+dy) == 'C':
            # print('re')
            m.set_color(x+dx, y+dy, '41')
            if m.get_element(x, y) == 'C':
                next_dir = laser_dir
                return True, 'inside refract', next_pos, next_dir
            else:
                side = laser_contact_side(matrix, laser_pos, laser_dir)
                if side == 'top' or side == 'down':
                    next_dir = (dx, -dy)
                if side == 'left' or side == 'right':
                    next_dir = (-dx, dy)    
                new_dir = laser_dir
                og_pos = (x+dx,y+dy)
                return True, 'retract', next_pos, next_dir, new_dir, og_pos 
    
    ### Top Row ###
    
    elif y - 1 < 0:
    
        # Is the Laser on the top or bottom edge of a block and is it trying to go to a reflect wall through itself.
        if m.get_element(x,y+dy) != 'o' and m.get_element((x+1),(y)) != 'o' and m.get_element((x-1),(y)) != 'o' and m.get_element((x),(y+dy)) == 'A': 
            # print('help-2')
            # print(m.get_element((x-1),(y)) != m.get_element((x+1),(y)))
            next_dir = (0, 0)
            next_pos = (x + 0, y + 0)
            return True, 'stop', next_pos, next_dir
    
    
        # Is the Laser on the top or bottom edge of a block and is it trying to go to a reflect wall NOT through itself.
        elif m.get_element(x+dx,y+dy) == 'A' and m.get_element((x+1),(y)) != 'o' and m.get_element((x-1),(y)) != 'o' and m.get_element((x),(y+dy)) != 'A': 
            m.set_color(x+dx, y+dy, '41')
            side = laser_contact_side(matrix, laser_pos, laser_dir)
            if side == 'top' or side == 'down':
                next_dir = (dx, -dy)
            if side == 'left' or side == 'right':
                next_dir = (-dx, dy)
            return True, 'reflect', next_pos, next_dir
    

         
        # Is the Laser on the top or bottom edge of a block and is it trying to go to an opaque block through itself
        elif m.get_element(x+dx,y+dy) == 'B' and (m.get_element((x+1),(y)) =="A" or m.get_element((x+1),(y)) =="B") and (m.get_element((x-1),(y)) == 'A' or m.get_element((x-1),(y)) == 'B') and m.get_element((x),(y+dy)) == 'B': 
            # print('help-6')
        
            next_dir = (0, 0)
            next_pos = (x + 0, y - 0)
            return True, 'stop', next_pos, next_dir
        
        
        
    
        # Is the Laser on the top or bottom edge of a block and is it trying to go to a opaque wall NOT through itself.
        elif m.get_element(x+dx,y+dy) == 'B' and (m.get_element((x+1),(y)) =="A" or m.get_element((x+1),(y)) =="B") and (m.get_element((x-1),(y)) == 'A' or m.get_element((x-1),(y)) == 'B') and m.get_element((x),(y+dy)) != 'B': 
            
            m.set_color(x+dx, y+dy, '41')
            next_dir =(0, 0)
            return True, 'stop', next_pos, next_dir, new_dir

    
     
            
        # Is the Laser on the top or bottom edge of a block and is it trying to go through a refract block
        elif (m.get_element((x+1),(y)) != 'o' and m.get_element((x-1),(y)) != 'o' and m.get_element(x+dx,y+dy)) == 'C' and m.get_element((x+1),(y)) ==m.get_element((x-1),(y)): 
            # print('help-8')
            if m.get_element(x+dx, y+dy) == 'C':
                side = 'top'
                if side == 'top' or side == 'down':
                    next_dir = (dx, -dy)
                if side == 'left' or side == 'right':
                    next_dir = (-dx, dy)    
                
                m.set_color(x+dx, y-dy, '41')
                next_pos = (x + dx, y - dy)
                new_dir = laser_dir
                og_pos = (x+dx,y+dy)
                return True, 'retract', next_pos, next_dir, new_dir, og_pos
            

        
        # when laser meets reflect block, A
        elif m.get_element(x+dx,y+dy) == 'A':
                m.set_color(x+dx, y+dy, '41')
                side = laser_contact_side(matrix, laser_pos, laser_dir)
            
                if side == 'top' or side == 'down':
                    next_dir = (dx, -dy)
                if side == 'left' or side == 'right':
                    next_dir = (-dx, dy)
                return True, 'reflect', next_pos, next_dir
            
        # when laser meets opaque, B
        elif m.get_element(x+dx, y+dy) == 'B':
            m.set_color(x+dx, y+dy, '41')
            next_dir =(0, 0)
            return True, 'stop', next_pos, next_dir, new_dir
        
        # when laser meets refract block, C
        elif m.get_element(x+dx, y+dy) == 'C':
            # print('re')
            m.set_color(x+dx, y+dy, '41')
            if m.get_element(x, y) == 'C':
                next_dir = laser_dir
                return True, 'inside refract', next_pos, next_dir
            else:
                side = laser_contact_side(matrix, laser_pos, laser_dir)
                if side == 'top' or side == 'down':
                    next_dir = (dx, -dy)
                if side == 'left' or side == 'right':
                    next_dir = (-dx, dy)    
                new_dir = laser_dir
                og_pos = (x+dx,y+dy)
                return True, 'retract', next_pos, next_dir, new_dir, og_pos 
            
    ### Left Wall ###
    
    elif x-1 < 0 :
        
        # Is the Laser on the left or right edge of a block and is it trying to go to a reflect wall through itself.
        if m.get_element(x+dx,y+dy) == 'A' and m.get_element(x,(y+1)) != 'o' and m.get_element(x,(y-1)) != 'o' and  m.get_element((x+dx),(y))=='A': 
            next_dir = (0, 0)
            next_pos = (x - 0, y + 0)
            return True, 'stop', next_pos, next_dir
    
        
        # Is the Laser on the left or right edge of a block and is it trying to go to a reflect wall NOT through itself.
        elif m.get_element(x+dx,y+dy) == 'A' and m.get_element(x,(y+1)) != 'o' and m.get_element(x,(y-1)) != 'o' and  m.get_element((x+dx),(y)!='A'): 
            m.set_color(x+dx, y+dy, '41')
            side = laser_contact_side(matrix, laser_pos, laser_dir)
            if side == 'top' or side == 'down':
                next_dir = (dx, -dy)
            if side == 'left' or side == 'right':
                next_dir = (-dx, dy)
            return True, 'reflect', next_pos, next_dir
        
        # Is the Laser on the left or right edge of a block and is it trying to go to an opaque block through itself
        elif m.get_element(x+dx,y+dy) == 'B' and (m.get_element(x,(y+1)) == 'A' or m.get_element(x,(y+1)) == 'B') and (m.get_element(x,(y-1)) == 'A' or m.get_element(x,(y-1)) == 'B') and  m.get_element((x+dx),(y))=='B': 
            # print('help-5')
            next_dir = (0, 0)
            next_pos = (x - 0, y + 0)
            return True, 'stop', next_pos, next_dir
         
        
        
        # Is the Laser on the left or right edge of a block and is it trying to go to a opaque wall NOT through itself.
        elif m.get_element(x+dx,y+dy) == 'B' and (m.get_element(x,(y+1)) == 'A' or m.get_element(x,(y+1)) == 'B') and (m.get_element(x,(y-1)) == 'A' or m.get_element(x,(y-1)) == 'B') and  m.get_element((x+dx),(y)!='B'): 
            
            m.set_color(x+dx, y+dy, '41')
            next_dir =(0, 0)
            return True, 'stop', next_pos, next_dir, new_dir
    

        
        
    
    
        # Is the Laser on the left or right edge of a block and is it trying to go through a refract block
        elif (m.get_element(x,(y+1)) != 'o' and m.get_element(x,(y-1)) != 'o' and m.get_element(x+dx,y+dy)) == 'C' and m.get_element((x),(y+1)) ==m.get_element((x),(y-1)): 
            # print('help-7')
    
            side = 'left'
            if side == 'top' or side == 'down':
                next_dir = (dx, -dy)
            if side == 'left' or side == 'right':
                next_dir = (-dx, dy)
            m.set_color(x-dx, y+dy, '41')
            next_pos = (x - dx, y + dy)
            new_dir = copy.copy(laser_dir)
            og_pos = (x+dx,y+dy)
            return True, 'retract', next_pos, next_dir, new_dir, og_pos  
            
        
        # when laser meets reflect block, A
        elif m.get_element(x+dx,y+dy) == 'A':
                m.set_color(x+dx, y+dy, '41')
                side = laser_contact_side(matrix, laser_pos, laser_dir)
            
                if side == 'top' or side == 'down':
                    next_dir = (dx, -dy)
                if side == 'left' or side == 'right':
                    next_dir = (-dx, dy)
                return True, 'reflect', next_pos, next_dir
            
        # when laser meets opaque, B
        elif m.get_element(x+dx, y+dy) == 'B':
            m.set_color(x+dx, y+dy, '41')
            next_dir =(0, 0)
            return True, 'stop', next_pos, next_dir, new_dir
        
        # when laser meets refract block, C
        elif m.get_element(x+dx, y+dy) == 'C':
            # print('re')
            m.set_color(x+dx, y+dy, '41')
            if m.get_element(x, y) == 'C':
                next_dir = laser_dir
                return True, 'inside refract', next_pos, next_dir
            else:
                side = laser_contact_side(matrix, laser_pos, laser_dir)
                if side == 'top' or side == 'down':
                    next_dir = (dx, -dy)
                if side == 'left' or side == 'right':
                    next_dir = (-dx, dy)    
                new_dir = laser_dir
                og_pos = (x+dx,y+dy)
                return True, 'retract', next_pos, next_dir, new_dir, og_pos
    
    ### Right Wall ###
    
    elif x+1 == m.max_column() :
        
        # Is the Laser on the left or right edge of a block and is it trying to go to a reflect wall through itself.
        if m.get_element(x+dx,y+dy) == 'A' and m.get_element(x,(y+1)) != 'o' and m.get_element(x,(y-1)) != 'o' and  m.get_element((x+dx),(y))=='A': 
            # print('help-1')
            next_dir = (0, 0)
            next_pos = (x - 0, y + 0)
            return True, 'stop', next_pos, next_dir
    
        
        
        # Is the Laser on the left or right edge of a block and is it trying to go to a reflect wall NOT through itself.
        elif m.get_element(x+dx,y+dy) == 'A' and m.get_element(x,(y+1)) != 'o' and m.get_element(x,(y-1)) != 'o' and  m.get_element((x+dx),(y)!='A'): 
            # print('help-3')
            m.set_color(x+dx, y+dy, '41')
            side = laser_contact_side(matrix, laser_pos, laser_dir)
            # print(side)
            if side == 'top' or side == 'down':
                next_dir = (dx, -dy)
            if side == 'left' or side == 'right':
                next_dir = (-dx, dy)
            # print(next_pos, next_dir)
            return True, 'reflect', next_pos, next_dir
            # next_dir = (-dx, dy)
            # next_pos = (x + dx, y + dy)
        
        
    
        # Is the Laser on the left or right edge of a block and is it trying to go to an opaque block through itself
        elif m.get_element(x+dx,y+dy) == 'B' and (m.get_element(x,(y+1)) == 'A' or m.get_element(x,(y+1)) == 'B') and (m.get_element(x,(y-1)) == 'A' or m.get_element(x,(y-1)) == 'B') and  m.get_element((x+dx),(y))=='B': 
            # print('help-5')
            next_dir = (0, 0)
            next_pos = (x - 0, y + 0)
            return True, 'stop', next_pos, next_dir
        
        
        
        
        # Is the Laser on the left or right edge of a block and is it trying to go to a opaque wall NOT through itself.
        elif m.get_element(x+dx,y+dy) == 'B' and (m.get_element(x,(y+1)) == 'A' or m.get_element(x,(y+1)) == 'B') and (m.get_element(x,(y-1)) == 'A' or m.get_element(x,(y-1)) == 'B') and  m.get_element((x+dx),(y)!='B'): 
            
            m.set_color(x+dx, y+dy, '41')
            next_dir =(0, 0)
            return True, 'stop', next_pos, next_dir, new_dir
    
         

    
        # Is the Laser on the left or right edge of a block and is it trying to go through a refract block
        elif (m.get_element(x,(y+1)) != 'o' and m.get_element(x,(y-1)) != 'o' and m.get_element(x+dx,y+dy)) == 'C' and m.get_element((x),(y+1)) ==m.get_element((x),(y-1)): 
            # print('help-7')
    
            side = 'left'
            if side == 'top' or side == 'down':
                next_dir = (dx, -dy)
            if side == 'left' or side == 'right':
                next_dir = (-dx, dy)
            m.set_color(x-dx, y+dy, '41')
            next_pos = (x - dx, y + dy)
            new_dir = copy.copy(laser_dir)
            og_pos = (x+dx,y+dy)
            return True, 'retract', next_pos, next_dir, new_dir, og_pos  
            
            # return True, 'reflect', next_pos, next_dir
        
        # when laser meets reflect block, A
        elif m.get_element(x+dx,y+dy) == 'A':
                m.set_color(x+dx, y+dy, '41')
                side = laser_contact_side(matrix, laser_pos, laser_dir)
            
                if side == 'top' or side == 'down':
                    next_dir = (dx, -dy)
                if side == 'left' or side == 'right':
                    next_dir = (-dx, dy)
                return True, 'reflect', next_pos, next_dir
            
        # when laser meets opaque, B
        elif m.get_element(x+dx, y+dy) == 'B':
            m.set_color(x+dx, y+dy, '41')
            next_dir =(0, 0)
            return True, 'stop', next_pos, next_dir, new_dir
        
        # when laser meets refract block, C
        elif m.get_element(x+dx, y+dy) == 'C':
            # print('re')
            m.set_color(x+dx, y+dy, '41')
            if m.get_element(x, y) == 'C':
                next_dir = laser_dir
                return True, 'inside refract', next_pos, next_dir
            else:
                side = laser_contact_side(matrix, laser_pos, laser_dir)
                if side == 'top' or side == 'down':
                    next_dir = (dx, -dy)
                if side == 'left' or side == 'right':
                    next_dir = (-dx, dy)    
                new_dir = laser_dir
                og_pos = (x+dx,y+dy)
                return True, 'retract', next_pos, next_dir, new_dir, og_pos                   
    
    ### Everything else if anything was missed ###
    
    
    # when laser meets reflect block, A
    elif m.get_element(x+dx,y+dy) == 'A':
            # print("hehehe")
            m.set_color(x+dx, y+dy, '41')
            side = laser_contact_side(matrix, laser_pos, laser_dir)
        
            if side == 'top' or side == 'down':
                next_dir = (dx, -dy)
            if side == 'left' or side == 'right':
                next_dir = (-dx, dy)
            return True, 'reflect', next_pos, next_dir
        
    # when laser meets opaque, B
    elif m.get_element(x+dx, y+dy) == 'B':
        m.set_color(x+dx, y+dy, '41')
        next_dir =(0, 0)
        return True, 'stop', next_pos, next_dir, new_dir
    
    # when laser meets refract block, C
    elif m.get_element(x+dx, y+dy) == 'C':
        m.set_color(x+dx, y+dy, '41')
        if m.get_element(x, y) == 'C':
            next_dir = laser_dir
            return True, 'inside refract', next_pos, next_dir
        else:
            side = laser_contact_side(matrix, laser_pos, laser_dir)
            if side == 'top' or side == 'down':
                next_dir = (dx, -dy)
            if side == 'left' or side == 'right':
                next_dir = (-dx, dy)    
            new_dir = laser_dir
            og_pos = (x+dx,y+dy)
            return True, 'retract', next_pos, next_dir, new_dir, og_pos    


def read_board(string):
    """ Takes in the filename of a bff file and translates it into a tuple

    Args:
        string (str): name of file. Format must be "name.bff"

    Returns:
        tuple: board_matrix array, a list of each type of useable block, a list of the lasers, their respective directions, and the target points
    """
    
    file = open(string, 'r')
    lines = file.readlines()
    
    board_positions = []
    board_matrix = []
    collect_Grid = False
    
    A_blocks = []
    B_blocks = []
    C_blocks = []
    
    lasers = []
    
    points = []
    
    for i in range(len(lines)):
        single_line = lines[i].strip() #gets rid of the \n at the end of each line
        
        if single_line == "GRID STOP":
            collect_Grid = False
            
        if collect_Grid:
            board_positions.append(single_line)
        
        if single_line == "GRID START":
            collect_Grid = True
            
            
        if 'A' in single_line and not collect_Grid and '#' not in single_line:
            A_blocks.append(single_line)
            
        if 'B' in single_line and not collect_Grid and '#' not in single_line:
            B_blocks.append(single_line)
            
        if 'C' in single_line and not collect_Grid and '#' not in single_line:
            C_blocks.append(single_line)
        
        if 'L' in single_line and not collect_Grid and '#' not in single_line:
            lasers.append(single_line)
        
        if 'P' in single_line and not collect_Grid and 'GRID' not in single_line and '#' not in single_line:
            points.append(single_line)
        
    for i in range(len(board_positions)):
        board_row = []
        for j in range(len(board_positions[i])):
            if board_positions[i][j] != ' ':
                board_row.append(board_positions[i][j])
                
        board_matrix.append(board_row)
            
    points_arr = []


    for i in range(len(points)):
        x_coordinate = int(points[i][2])
        y_coordinate = int(points[i][4])
        points_arr.append((x_coordinate, y_coordinate))
        
    lasers_arr = []
    lasers_dir_arr = []

    for i in range(len(lasers)):
        laser_string_arr = lasers[i].split(' ')
        x_coordinate = int(laser_string_arr[1])
        y_coordinate = int(laser_string_arr[2])
        vx_coordinate = int(laser_string_arr[3])
        vy_coordinate = int(laser_string_arr[4])
        
        lasers_arr.append((x_coordinate, y_coordinate))
        lasers_dir_arr.append((vx_coordinate, vy_coordinate))
      
    board_matrix_array = np.array(board_matrix)  
      
    return board_matrix_array, A_blocks, B_blocks, C_blocks, lasers_arr, lasers_dir_arr, points_arr

def get_board_permutations(board, num_of_A, num_of_B, num_of_C, lasers, lasers_direction_list, targets):
    '''
    Takes in a 2D-Matrix of the board, the number of A blocks, the number of B blocks, and the number of C blocks and lists of lasers and targets
    
    Returns an array with each element containing set of tuples in the form of (blockType, x-coordinate, y-coordinate) for each added block and the number of fixed blocks
    '''
    
    
    board_array = np.array(board)
    board_rows, board_col = board_array.shape
    
    ## Get Fixed Block Locations and x Locations
    
    fixed_blocks = set()
   
    for i in range((board_rows)):
        for j in range((board_col)):
            if board_array[i][j] != "o":
                fixed_blocks.add((j,i))

    fixed_count = len(fixed_blocks)
    flattened_board_array = board_array.flatten()
    fixed_flattened_arr = []
    for i in range(len(flattened_board_array)):
        if flattened_board_array[i] != 'o':
            fixed_flattened_arr.append((flattened_board_array[i],i))
        

    ## Delete fixed elements from flattened array
    new_flat = np.delete(flattened_board_array, np.where((flattened_board_array !='o')))

    ## Count number of useable Blocks

    total_number_of_blocks = num_of_A + num_of_B + num_of_C
    
    
    A_blocks = []
    B_blocks = []
    C_blocks = []

    ## Create instances of A, B, and C to be added to board
    for i in range(num_of_A):
        A_blocks.append('A')
    for i in range(num_of_B):
        B_blocks.append('B')
    for i in range(num_of_C):
        C_blocks.append('C')
    
   
    
    ## Delete o's from flattened array and replace them with the instances of A, B, and C
    for i in range(total_number_of_blocks):
        new_flat = np.delete(new_flat,0)
        
    
    all_arrs = (A_blocks,B_blocks,C_blocks, new_flat)
    flattened_with_blocks = np.concatenate(all_arrs)
    
    # Create Array of all Possible Board Permutations    
    added_blocks_permutations = []
    flattened_permutations = multiset_permutations(flattened_with_blocks)
    
 # ------------------------------------------------------------------------------------------------------------------#
                            # Filtering Starts #
 # ------------------------------------------------------------------------------------------------------------------#  

## Create set of impossible block combinations -- Combinations where the laser or targets are trapped by walls horizontally ##
    

    
    impossible_set = set()

    # Find Trapped Lasers
    for element in lasers:
        
        laser_x, laser_y = element
        
        # If I'm trapped between two horizontal walls
        if (laser_x % 2 == 0):
            left_block_x = int((laser_x/2)-1) 
            right_block_x = int((laser_x/2))
            both_blocks_y = int((laser_y-1)/2)
            impossible_set.add(('A',left_block_x,both_blocks_y))
            impossible_set.add(('A',right_block_x,both_blocks_y))
            impossible_set.add(('B',right_block_x,both_blocks_y))
            impossible_set.add(('B',left_block_x,both_blocks_y))
            
        #If I'm Trapped between two vertical wall
        if (laser_y % 2 == 0):    
            top_block_y = int((laser_y/2)-1)  
            bottom_block_y = int((laser_y/2))
            both_block_x = int((laser_x - 1)/2)
            impossible_set.add(('A',both_block_x,top_block_y))
            impossible_set.add(('A',both_block_x,bottom_block_y))
            impossible_set.add(('B',both_block_x,bottom_block_y))
            impossible_set.add(('B',both_block_x,top_block_y))
        
        
    #Do the Same for Targets
            
    for element in targets:

        laser_x, laser_y = element
        
        # If I'm trapped between two horizontal walls
        if (laser_x % 2 == 0):
            left_block_x = int((laser_x/2)-1) 
            right_block_x = int(laser_x/2)
            both_blocks_y = int((laser_y-1)/2)
            impossible_set.add(('A',left_block_x,both_blocks_y))
            impossible_set.add(('A',right_block_x,both_blocks_y))
            impossible_set.add(('B',right_block_x,both_blocks_y))
            impossible_set.add(('B',left_block_x,both_blocks_y))
            
        #If I'm Trapped between two vertical wall
        if (laser_y % 2 == 0):    
            top_block_y = int((laser_y/2)-1)  
            bottom_block_y = int(laser_y/2)
            both_block_x = int((laser_x - 1)/2)
            impossible_set.add(('A',both_block_x,top_block_y))
            impossible_set.add(('A',both_block_x,bottom_block_y))
            impossible_set.add(('B',both_block_x,bottom_block_y))
            impossible_set.add(('B',both_block_x,top_block_y))
        
            
    
    forbidden_set = impossible_set
    
    print("This set has blocks that trap our points and lasers. If a block combination has one of these, it will check to see if the adjacent blocks are also in there ", forbidden_set)
    
##      Create a set of Blocks that we need to be in the lasers path         ##


    # Per each laser, create a sets of block combinations that lead to straight laser paths. Put these sets in an array.
    
    
    needed_blocks_per_laser = []
    
    ## Get Straight Laser Path Set per each laser ##
    for i in range(len(laser_positions)):
        
        need_at_least_one_block_from_here = set() ## This is a set of the block combinations (e.g {(A, 0, 0), (A,1,0), (A,2,0)}
        straight_laser_path = set() #This is a set of the laser Path (e.g {(2,1), (3,2), (4,3), etc})
        
        x, y = laser_positions[i]
        dx, dy = lasers_direction_list[i]
        print('Laser', i+1 , 'Path: ')
        while (((x <= matrix_width) and (x >= 0)) and ((y <= matrix_height) and (y >= 0))):
            print((x,y))
            straight_laser_path.add((x,y))
            x = x + dx
            y = y + dy
        print()
        print('Laser Path as Set: ', straight_laser_path)
        print()
    
    ## Get blocks that would cause walls there
        
        for element in straight_laser_path:
            laser_x, laser_y = element
            if (laser_x % 2 == 0 and laser_x!= matrix_width and laser_x !=0):
                left_block_x = int((laser_x/2)-1) 
                right_block_x = int(laser_x/2)
                both_blocks_y = int((laser_y-1)/2)
                need_at_least_one_block_from_here.add(('A',left_block_x,both_blocks_y))
                need_at_least_one_block_from_here.add(('A',right_block_x,both_blocks_y))
                need_at_least_one_block_from_here.add(('C',right_block_x,both_blocks_y))
                need_at_least_one_block_from_here.add(('C',left_block_x,both_blocks_y))
                
            if (laser_y % 2 == 0 and laser_y != matrix_height and laser_y !=0):    
                top_block_y = int((laser_y/2)-1)  
                bottom_block_y = int(laser_y/2)
                both_block_x = int((laser_x - 1)/2)
                need_at_least_one_block_from_here.add(('A',both_block_x,top_block_y))
                need_at_least_one_block_from_here.add(('A',both_block_x,bottom_block_y))
                need_at_least_one_block_from_here.add(('C',both_block_x,bottom_block_y))
                need_at_least_one_block_from_here.add(('C',both_block_x,top_block_y))
        
        # print()
        # print(need_at_least_one_block_from_here)
        # print(need_at_least_one_block_from_here)
        needed_blocks_per_laser.append(need_at_least_one_block_from_here)
    
    for j in range(len(needed_blocks_per_laser)):
        print('This is the set of blocks that Laser', j+1, 'need in its path. The laser must hit AT LEAST one of these')
        print(needed_blocks_per_laser[j])
        print()
    
    
    ## Now we have our  our necessary blocks set and our impossible set. Go through the permutations and add them/subtract them to the end array as needed ##
    
    for board_perm in flattened_permutations:
    
    #replace fixed blocks back into flattened array with the added blocks
        restored_board_permutation = []
        fixed_index_count = 0
        for i in range(len(flattened_board_array)):
            if flattened_board_array[i] == 'o':
                restored_board_permutation.append(board_perm[i - fixed_index_count])
            else:
                restored_board_permutation.append(flattened_board_array[i])
                fixed_index_count+=1
            
        
    #Find the board matrix coordinates of the added blocks and add it to a set containing the type   
        added_blocks_set = []

     
        
        
        for i in range(len(restored_board_permutation)):
    
            block_type = restored_board_permutation[i]
            row_num = i // board_col
            col_num = i % board_col
            
                
         
            
            
            if block_type != 'o' and (row_num, col_num) not in fixed_blocks:
                added_blocks_set.append((block_type, col_num, row_num)) 
                

        clean_list = []             
        clean_boolean = True
         
        
        # print(added_blocks_set) ## array
        for value in needed_blocks_per_laser:
            if any(elem in value for elem in added_blocks_set) == False:
                    clean_boolean = False
        
        
        
        # Iterate through forbidden set and do the Impossible Tests
        for i in forbidden_set:    
        
    
            filtered_block_type, filter_x, filter_y = i 
            left_block_of_current = ((filter_x)-1)
            right_block_of_current = ((filter_x)+1)
            top_block_of_current = (filter_y)-1
            bottom_block_of_current = (filter_y)+1
        
        
        
        
                
                
        ## Horizontal Wall Trap Filter ##
        if(filtered_block_type,filter_x,filter_y) in added_blocks_set and ('A',left_block_of_current,filter_y) in  added_blocks_set:
            clean_boolean = False
        if(filtered_block_type,filter_x,filter_y) in added_blocks_set and ('B',left_block_of_current,filter_y) in  added_blocks_set:
            clean_boolean = False
        
        if(filtered_block_type,filter_x,filter_y) in added_blocks_set and ('A',right_block_of_current,filter_y) in added_blocks_set:
            clean_boolean = False
        if(filtered_block_type,filter_x,filter_y) in added_blocks_set and ('B',right_block_of_current,filter_y) in added_blocks_set:
            clean_boolean = False
       
            
        ## Vertical Wall Trap Filter ##
        if(filtered_block_type,filter_x,filter_y) in added_blocks_set and ('A',filter_x, top_block_of_current) in  added_blocks_set:
            clean_boolean = False
        if(filtered_block_type,filter_x,filter_y) in added_blocks_set and ('B',filter_x, top_block_of_current) in  added_blocks_set:
            clean_boolean = False
       
        
        if(filtered_block_type,filter_x,filter_y) in added_blocks_set and ('A',filter_x,bottom_block_of_current) in  added_blocks_set:
            clean_boolean = False
        if(filtered_block_type,filter_x,filter_y) in added_blocks_set and ('B',filter_x,bottom_block_of_current) in  added_blocks_set:
            clean_boolean = False
        
        
  
        
        
                
        
        if clean_boolean:
            clean_list.append(added_blocks_set)            
            added_blocks_permutations.append(clean_list[0])     
                
    # print(added_blocks_permutations[1])
    return added_blocks_permutations, fixed_count

def rebuild_matrix(original_board, added_block_set):
    """This function creates a new 2D board array with blocks from an added block set array

    Args:
        original_board (2D array): the original empty 2D matrix array
        added_block_set (tuple): (block_type, block x-position, block y-position)

    Returns:
        new board matrix (2D array)
    """
    board_array = np.array(original_board)
    board_rows, board_col = board_array.shape
    
    new_board_matrix = copy.copy(original_board)
    # print(added_block_set)
    for i in (added_block_set):
        # print(i)
        added_type = i[0]
        added_x = i[2]
        added_y = i[1]
        new_board_matrix[int(added_x)][added_y] = added_type
            
    
    return new_board_matrix

def get_All_Left_Walls(board):
    """
    This function takes our 2D Board Matrix and extracts all the left wall Points in Matrix Co-Ordinates
    Args:
        board (2D-Array)
    Returns:
        list: array of left wall points
    """
    left_walls_arr = []
    board_array = np.array(board)
    board_rows, board_col = board_array.shape
    
    for i in range(board_rows):
        for j in range(board_col):
            block_type = board_array[i][j]
            if block_type != 'x' and block_type != 'o':
                selected_block = Block(i,j,block_type)
                x,y = selected_block.get_Left_Wall()
                left_walls_arr.append((block_type, (x,y)))
                left_walls_arr.append((block_type,(x,y+1)))
                left_walls_arr.append((block_type,(x,y-1)))
    return left_walls_arr

def get_All_Right_Walls(board):
    """
    This function takes our 2D Board Matrix and extracts all the right wall Points in Matrix Co-Ordinates
    Args:
        board (2D-Array)
    Returns:
        list: array of right wall points
    """
    right_walls_arr = []
    board_array = np.array(board)
    board_rows, board_col = board_array.shape
    
    for i in range(board_rows):
        for j in range(board_col):
            block_type = board_array[i][j]
            if block_type != 'x' and block_type != 'o':
                selected_block = Block(i,j,block_type)
                x,y = selected_block.get_Right_Wall()
                right_walls_arr.append((block_type, (x,y)))
                right_walls_arr.append((block_type,(x,y+1)))
                right_walls_arr.append((block_type,(x,y-1)))
    
    return right_walls_arr

def get_All_Top_Walls(board):
    """
    This function takes our 2D Board Matrix and extracts all the top wall Points in Matrix Co-Ordinates
    Args:
        board (2D-Array)
    Returns:
        list: array of top wall points
    """
    top_walls_arr = []
    board_array = np.array(board)
    board_rows, board_col = board_array.shape
    
    for i in range(board_rows):
        for j in range(board_col):
            block_type = board_array[i][j]
            if block_type != 'x' and block_type != 'o':
                selected_block = Block(i,j,block_type)
                x,y = selected_block.get_Top_Wall()
                top_walls_arr.append((block_type, (x,y)))
                top_walls_arr.append((block_type,(x+1,y)))
                top_walls_arr.append((block_type,(x-1,y)))
    
    return top_walls_arr

def get_All_Bottom_Walls(board):
    """
    This function takes our 2D Board Matrix and extracts all the bottom wall Points in Matrix Co-Ordinates
    Args:
        board (2D-Array)
    Returns:
        list: array of bottom wall points
    """
    bottom_walls_arr = []
    board_array = np.array(board)
    board_rows, board_col = board_array.shape
    
    for i in range(board_rows):
        for j in range(board_col):
            block_type = board_array[i][j]
            if block_type != 'x' and block_type != 'o':
                selected_block = Block(i,j,block_type)
                x,y = selected_block.get_Bottom_Wall()
                bottom_walls_arr.append((block_type, (x,y)))
                bottom_walls_arr.append((block_type,(x+1,y)))
                bottom_walls_arr.append((block_type,(x-1,y)))                

    return bottom_walls_arr

def get_All_Centers(board):
    """
    This function takes our 2D Board Matrix and extracts all the Center Points in Matrix Co-Ordinates
    Args:
        board (2D-Array)
    Returns:
        list: array of center points
    """
    centers_arr = []
    board_array = np.array(board)
    board_rows, board_col = board_array.shape
    
    for i in range(board_rows):
        for j in range(board_col):
            block_type = board_array[i][j]
            if block_type != 'x' and block_type != 'o':
                selected_block = Block(i,j,block_type)
                x,y = 2*selected_block.get_x()+1, 2*selected_block.get_y()+1
                
                centers_arr.append((block_type, (x,y)))
                

    return centers_arr

def get_All_Walls(board):
    """
    This function takes our 2D Board Matrix and extracts all the  Walls in Matrix Co-Ordinates
    Args:
        board (2D-Array)
    Returns:
        array: array of Walls
    """
    np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)
    Top_walls = get_All_Top_Walls(board)
    Bottom_walls = get_All_Bottom_Walls(board)
    Left_walls = get_All_Left_Walls(board)
    Right_walls = get_All_Right_Walls(board)
    Centers = get_All_Centers(board)
    
    args = (Top_walls,Bottom_walls,Left_walls,Right_walls, Centers)
    walls_arr = np.concatenate(args)
    return walls_arr

def get_All_Reflect_Walls(board):
    """
    This function takes our 2D Board Matrix and extracts all the Reflecting Walls in Matrix Co-Ordinates
    Args:
        board (2D-Array)
    Returns:
        set: set of Reflect Walls
    """
    reflect_walls = []
    all_walls = get_All_Walls(board)
    for i in range(len(all_walls)):
        block_type = all_walls[i][0]
        if block_type == 'A':
            reflect_walls.append(all_walls[i][1])
    
    return list(set(reflect_walls))

def get_All_Opaque_Walls(board):
    """
    This function takes our 2D Board Matrix and extracts all the Opaque Walls in Matrix Co-Ordinates
    Args:
        board (2D-Array)
    Returns:
        set: set of Opaque Walls
    """
    opaque_walls = []
    all_walls = get_All_Walls(board)
    for i in range(len(all_walls)):
        block_type = all_walls[i][0]
        if block_type == 'B':
            opaque_walls.append(all_walls[i][1])
    
    return list(set(opaque_walls))

def get_All_Refract_Walls(board):
    """
    This function takes our 2D Board Matrix and extracts all the Refracting Walls in Matrix Co-Ordinates
    Args:
        board (2D-Array)
    Returns:
        set: set of Refract Walls
    """
    refract_walls = []
    all_walls = get_All_Walls(board)
    for i in range(len(all_walls)):
        block_type = all_walls[i][0]
        if block_type == 'C':
            refract_walls.append(all_walls[i][1])
    
    return list(set(refract_walls))

if __name__ == "__main__":
    
    #Create a fixed set of all the intersection point
    board, A, B, C, lasers, laser_dir, points = read_board('mad_7.bff')
    Original_Board = Board(board, A, B, C, lasers, laser_dir, points)
    print("Original Board: ")
    print(board)
    board_height, board_width = board.shape
    matrix_height = board_height*2 + 1
    matrix_width = board_width*2 + 1

    num_A_blocks = Original_Board.get_A_Blocks()
    num_B_blocks = Original_Board.get_B_Blocks()
    num_C_blocks = Original_Board.get_C_Blocks()
    
    laser_positions = Original_Board.get_Lasers()
    laser_directions = Original_Board.get_Lasers_dir()
    targets = Original_Board.get_points()
    
    board_permutations, fixed_count= get_board_permutations(board,num_A_blocks,num_B_blocks,num_C_blocks, laser_positions, laser_directions, targets) 
    total_permutations = len(board_permutations)
    
    print("There are ",total_permutations, "permutations of solutions")
    
    board_permutations_index = 0
    true_path_index = 0
    Does_Laser_Hit_Targets = False
    
    m = Matrix(matrix_width,matrix_height)
    
    while board_permutations_index != len(board_permutations):
    # for i in range(0,4,1):
        
        # print(board_permutations_index)
   
                
                
        Board1 = Board(board, A, B, C, lasers, laser_dir, points)
        
        
        placed_count = 0
        total_allowed_to_be_placed = num_A_blocks+num_B_blocks+num_C_blocks       

        new_board = rebuild_matrix(board,board_permutations[board_permutations_index])
        # print(rebuild_matrix(board,board_permutations[board_permutations_index]))
 
        
        target_list = copy.copy(Board1.get_points())
        laser_list = copy.copy(Board1.get_Lasers())
        laser_dir_list = copy.copy(Board1.get_Lasers_dir())
        reflect_list = get_All_Reflect_Walls(new_board)
        refract_list = get_All_Refract_Walls(new_board)
        opaque_list = get_All_Opaque_Walls(new_board)
        
        # print(laser_list)
        
        m = Matrix(matrix_width,matrix_height)
        
        
        
        set_targets(m,target_list)
        set_laser(m, laser_list)  
        set_reflect(m,reflect_list)
        set_opaque(m,opaque_list)
        set_refract(m,refract_list)
        # print('here')
        length_of_laser_list = len(laser_list)
        index = 0
        
        while index != length_of_laser_list:
            #Initial Step
            current_pos = laser_list[index]
            laser_direction = laser_dir_list[index]
            interaction = laser_1_step(m,current_pos, laser_direction)
            interaction_len = 0
            validate = bool()
            # print("outer")
            # print(interaction)
            if type(interaction) != bool:
                    interaction_len = len(interaction)

            if interaction_len == 4:
                    
                    validate = interaction[0]
                    behavior = interaction[1]
                    new_pos = interaction [2]
                    next_dir = interaction[3]
                    
                    if behavior == 'stop':
                        validate = False
                
            elif interaction_len == 6:
                    
                    validate = interaction[0]
                    behavior = interaction[1]
                    new_pos = interaction [2]
                    next_dir = interaction[3]
                    new_dir = interaction [4]
                    og_pos = interaction[5]
                    laser_list.append(og_pos)
                    laser_dir_list.append(new_dir)
                    
                    length_of_laser_list +=1
            else:
                validate == False
                    
            while validate:
                interaction = laser_1_step(m,new_pos, next_dir)

                interaction_len = 0
                if type(interaction) != bool:
                    interaction_len = len(interaction)
                    
                if interaction_len == 4:
                    
                    validate = interaction[0]
                    behavior = interaction[1]
                    new_pos = interaction [2]
                    next_dir = interaction[3]

                    if behavior == 'stop':
                        validate = False
                
                elif interaction_len == 6:
                    
                    validate = interaction[0]
                    behavior = interaction[1]
                    new_pos = interaction [2]
                    next_dir = interaction[3]
                    new_dir = interaction [4]
                    og_pos = interaction[5]
                    laser_list.append(og_pos)
                    laser_dir_list.append(new_dir)
                    length_of_laser_list +=1
                   
                
                
                else:
                    validate = False
            
            index += 1
        target_list_set = set(target_list)    
        laser_path_set = set(m.get_colored_array())
        
        this_iteration_overlap = len(list(laser_path_set.intersection(target_list_set)))
        

        brand_new_board = (rebuild_matrix(board,board_permutations[board_permutations_index]))
        all_lefts = get_All_Left_Walls(brand_new_board)
        all_rights = get_All_Right_Walls(brand_new_board)
        all_tops = get_All_Top_Walls(brand_new_board)
        all_bottoms = get_All_Bottom_Walls(brand_new_board)
        all_centers = get_All_Centers(brand_new_board)
        
        
        center_x, center_y = int(), int()
        laser_wall_intersection_arr = []
        
        for i in range(len(all_centers)):
            for item in laser_path_set:
                if item in all_lefts[3*i]:
                    temp_x, temp_y = all_lefts[3*i][1]
                    center_x, center_y = temp_x-1, temp_y
                    laser_wall_intersection_arr.append((center_x,center_y))
                    
                if item in all_rights[3*i]:
                    temp_x, temp_y = all_rights[3*i][1]
                    center_x, center_y = temp_x+1, temp_y
                    laser_wall_intersection_arr.append((center_x,center_y))
                    
                if item in all_tops[3*i]:
                    temp_x, temp_y = all_tops[3*i][1]
                    center_x, center_y = temp_x, temp_y-1
                    laser_wall_intersection_arr.append((center_x,center_y))
                    
                if item in all_bottoms[3*i]:
                    temp_x, temp_y = all_bottoms[3*i][1]
                    center_x, center_y = temp_x, temp_y+1
                    laser_wall_intersection_arr.append((center_x,center_y))
                    
        
        laser_intersect_block_locations = []
        # print(laser_wall_intersection_arr)
        
        # print(all_centers[0])
        # print(all_centers[3])
        for i in laser_wall_intersection_arr:
            center_x, center_y = i
            
            new_board_x = int((center_x - 1)/2)
            new_board_y = int((center_y - 1)/2)
            laser_intersect_block_locations.append((new_board_x,new_board_y))
        
        # # print('The Block Locations that have Laser touching them are ', laser_intersect_block_locations)
        # untouched_blocks = []
        # for applied_blocks in (board_permutations[board_permutations_index]):
        #     if (applied_blocks[1],applied_blocks[2]) not in laser_intersect_block_locations:
        #         untouched_blocks.append(applied_blocks)
        
        # print(untouched_blocks)
        # # print(get_All_Walls(brand_new_board))
        
        # # if(this_iteration_overlap > current_match):
        # #     print(this_iteration_overlap)
        # #     # print(board_permutations[board_permutations_index])
        # #     current_match = this_iteration_overlap
        # #     laser_path_points_to_remember = board_permutations[board_permutations_index]
            
        
        if target_list_set.issubset(laser_path_set) :
            Does_Laser_Hit_Targets = True
            true_path_index = board_permutations_index
            
            
        #     placed_count = 0
        #     for items in board_permutations[board_permutations_index]:
        #         if items[0] != 'x':
        #             placed_count += 1
                        
        #         total_allowed_to_be_placed = num_A_blocks+num_B_blocks+num_C_blocks
        #         # print(total_allowed_to_be_placed, placed_count)
        #         if placed_count - fixed_count >= total_allowed_to_be_placed:

        if (board_permutations_index == total_permutations):
            Does_Laser_Hit_Targets = True
            
        board_permutations_index+=1
        
    
        # print(board_permutations[true_path_index])
        # m.print_matrix_with_indices()
        # print(laser_list)
        
    if(Does_Laser_Hit_Targets):
        print("Here is the path the laser takes")
        m.print_matrix_with_indices()
    
        print("You want to place the blocks in the following position: ", board_permutations[true_path_index])
        print("This placement should yield the correct solution")
        print(rebuild_matrix(board,board_permutations[true_path_index]))
    
    else:
        print("No Soultion Found")
       
        



    
    
  