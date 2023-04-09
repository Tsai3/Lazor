# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 20:58:28 2023
@author: Tsai
"""

class Matrix:
    '''
    This is just a quick class that I used to generate the matrix for laser behavior
    when Luje genere a function that read the board and translate that into matrix, 
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
        m.set_target(x,y)
        
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
        m.set_laser(x,y)

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
        m.set_reflect(x,y)

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
        m.set_opaque(x,y)

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
        m.set_refract(x,y)

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
    
    
    
        
    if m.get_element(nx+1,ny) != 'o' and m.get_element(nx-1,ny) != 'o' and m.get_element(nx,ny-1) != 'o' and m.get_element(nx,ny-2) != 'o':
        side = 'down'
    elif m.get_element(nx+1,ny) != 'o' and m.get_element(nx-1,ny) != 'o' and m.get_element(nx,ny+1) != 'o' and m.get_element(nx,ny+2) != 'o':
        side = 'top'
    elif m.get_element(nx+1,ny) != 'o' and m.get_element(nx+2,ny) != 'o' and m.get_element(nx,ny+1) != 'o' and m.get_element(nx,ny-1) != 'o':
        side = 'left'
    elif m.get_element(nx-1,ny) != 'o' and m.get_element(nx-2,ny) != 'o' and m.get_element(nx,ny+1) != 'o' and m.get_element(nx,ny-1) != 'o':
        side = 'top'
    
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
    
    # print('next_pos[0]__nx: ', next_pos[0])
    # print('next_pos[0]__nx: ', next_pos[0])
    # print('m.max_column()__max_x: ', m.max_column())
    # print('next_pos[1]__ny: ', next_pos[1])
    # print('next_pos[1]__ny: ', next_pos[1])
    # print('m.max_row()__max_y: ', m.max_row())
    
    
    #check if next_position is in matrix
    if next_pos[0] <0 or next_pos[0] > (m.max_column()-1) or next_pos[1] <0 or next_pos[1] > (m.max_row()-1):
        return 'False'
        
    #check if next_position is o
    elif m.get_element(x+dx, y+dy) == 'o' or m.get_element(x+dx, y+dy) == 'L'or m.get_element(x+dx, y+dy) == 'T':
        m.set_color(x+dx, y+dy, '41')
        next_dir = laser_dir
        return 'True', 'pass', next_pos, laser_dir
    
    # when laser meets reflect block, A
    elif m.get_element(x,y) == 'A':
        m.set_color(x+dx, y+dy, '41')
        side = laser_contact_side(matrix, laser_pos, laser_dir)
        if side == 'top' or side == 'down':
            next_dir = (dx, -dy)
        if side == 'left' or side == 'right':
            next_dir = (-dx, dy)
        return 'True', 'reflect', next_pos, next_dir
    
    # when laser meets opaque, B
    elif m.get_element(x+dx, y+dy) == 'B':
        m.set_color(x+dx, y+dy, '41')
        next_dir =(0, 0)
        return 'True', 'stop', next_pos, next_dir
    # when laser meets refract block, C
    elif m.get_element(x+dx, y+dy) == 'C':
        m.set_color(x+dx, y+dy, '41')
        if m.get_element(x, y) == 'C':
            next_dir = laser_dir
            return 'True', 'inside refract', next_pos, next_dir
        else:
            side = laser_contact_side(matrix, laser_pos, laser_dir)
            if side == 'top' or side == 'down':
                next_dir = (dx, -dy)
            if side == 'left' or side == 'right':
                next_dir = (-dx, dy)    
            new_dir = laser_dir
            return 'True', 'retract', next_pos, next_dir, new_dir

# create a matrix class (MAD1 as example)
m = Matrix(9,9)

# mark the points the lazer need to intersect
target_list = [(3,0),(2,5),(4,3),(4,7)]
set_targets(m,target_list)

# market the laser source
laser_list = [(2,7)]
set_laser(m, laser_list)

# mark the points covered by reflect block
reflect_list = []
set_reflect(m,reflect_list)

# mark the points covered by opaque block
opaque_list = []
set_opaque(m,opaque_list)

# mark the points covered by refract block
refract_list = [(6,0), (7,0), (8,0), (6,1), (7,1), (8,1), (6,2), (7,2), (8,2)]
                # (3,4), (4,4), (5,4), (3,5), (4,5), (5,5), (3,6), (4,6), (5,6)
                
set_refract(m,refract_list)


# will use a loop to keep doing laser_1_step and use the new position and dir returned to run another laser_1_step etc. 
laser_direction = (1,-1)
print(laser_1_step(m, (2,7), (1,-1)))
laser_1_step(m, (3,6), (1,-1))




# run_laser(m)
m.print_matrix_with_indices()

