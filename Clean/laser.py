# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 20:58:28 2023
@author: Tsai
"""
import copy

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

# create a matrix class (MAD1 as example)
m = Matrix(9,9)

# mark the points the lazer need to intersect
target_list = [(3,0),(2,5),(4,3),(4,7)]
set_targets(m,target_list)

# market the laser source
laser_list = [(2,7)]
set_laser(m, laser_list)

# mark the points covered by reflect block
reflect_list = [(0, 1), (4, 0), (1, 2), (2, 1), (0, 0), (3, 1), (1, 1), (2, 0), (4, 2), (3, 0), (0, 2), (2, 2), (1, 0), (3, 2), (4, 1)]
set_reflect(m,reflect_list)

# mark the points covered by opaque block
opaque_list = []
set_opaque(m,opaque_list)

# mark the points covered by refract block
refract_list = [(2,4), (2,5), (2,6), (3,4), (3,5), (3,6), (4,4), (4,5), (4,6)]
                # (3,4), (4,4), (5,4), (3,5), (4,5), (5,5), (3,6), (4,6), (5,6)
                
set_refract(m,refract_list)
 
laser_direction_list = [(1,-1)]


# Get the Original Length of Laser List
length_of_laser_list = len(laser_list)
index = 0

m.print_matrix_with_indices()

while index != length_of_laser_list:
    #Initial Step
    current_pos = laser_list[index]
    laser_direction = laser_direction_list[index]
    interaction = laser_1_step(m,current_pos, laser_direction)
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
        
    elif interaction_len == 5:
            
            validate = interaction[0]
            behavior = interaction[1]
            new_pos = interaction [2]
            next_dir = interaction[3]
            new_dir = interaction [4]
            
            #Create a new laser and add it to the list
            laser_list.append(new_pos)
            laser_direction_list.append(new_dir)
            length_of_laser_list +=1
            
    while validate:
        interaction = laser_1_step(m,new_pos, next_dir)
        
        interaction_len = 0
        if type(interaction) != bool:
            interaction_len = len(interaction)
            
        print(interaction_len)

        if interaction_len == 4:
            
            validate = interaction[0]
            behavior = interaction[1]
            new_pos = interaction [2]
            next_dir = interaction[3]
            
            if behavior == 'stop':
                validate = False
        
        elif interaction_len == 5:
            
            validate = interaction[0]
            behavior = interaction[1]
            new_pos = interaction [2]
            next_dir = interaction[3]
            new_dir = interaction [4]
            
            #Create a new laser and add it to the list
            laser_list.append(new_pos)
            laser_direction_list.append(new_dir)
            length_of_laser_list +=1
         
           
        else:
            validate = False
    
    index += 1
        
        
m.print_matrix_with_indices()

