import numpy as np
from sympy.utilities.iterables import multiset_permutations

class Block:
    '''
    This class carries creates a Block objecct.
   
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
    This class carries creates a Board objecct.
   
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
    
    
    
        
    if m.get_element(nx+1,ny) != 'o' and m.get_element(nx-1,ny) != 'o' and m.get_element(nx,ny-1) != 'o' and m.get_element(nx,ny-2) != 'o':
        side = 'down'
    elif m.get_element(nx+1,ny) != 'o' and m.get_element(nx-1,ny) != 'o' and m.get_element(nx,ny+1) != 'o' and m.get_element(nx,ny+2) != 'o':
        side = 'top'
    elif m.get_element(nx+1,ny) != 'o' and m.get_element(nx+2,ny) != 'o' and m.get_element(nx,ny+1) != 'o' and m.get_element(nx,ny-1) != 'o':
        side = 'left'
    elif m.get_element(nx-1,ny) != 'o' and m.get_element(nx-2,ny) != 'o' and m.get_element(nx,ny+1) != 'o' and m.get_element(nx,ny-1) != 'o':
        side = 'top'
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
        return 'False'
        
    #check if next_position is o
    elif m.get_element(x+dx, y+dy) == 'o' or m.get_element(x+dx, y+dy) == 'L'or m.get_element(x+dx, y+dy) == 'T':
        m.set_color(x+dx, y+dy, '41')
        next_dir = laser_dir
        return 'True', 'pass', next_pos, laser_dir
    
    # when laser meets reflect block, A
    elif m.get_element(x+dx,y+dy) == 'A':
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


def read_board(string):
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

def get_board_permutations(board, num_of_A, num_of_B, num_of_C):
    '''
    Takes in a 2D-Matrix of the board, the number of A blocks, the number of B blocks, and the number of C blocks
    
    Returns an array with each element containing set of tuples in the form of (blockType, x-coordinate, y-coordinate) for each added block
    '''
    
    board_array = np.array(board)
    board_rows, board_col = board_array.shape

    ##Get Fixed Block Locations and x Locations
    fixed_blocks = set()
   
    for i in range((board_rows)):
        for j in range((board_col)):
            if board_array[i][j] != "o":
                fixed_blocks.add((i,j))

    
                
    flattened_board_array = board_array.flatten()

    ##Delete fixed elements from flattened array
    new_flat = np.delete(flattened_board_array, np.where((flattened_board_array !='o')))

    ##Count number of useable Blocks

    total_number_of_blocks = num_of_A + num_of_B + num_of_C
    
    A_blocks = []
    B_blocks = []
    C_blocks = []

    ##Create instances of A, B, and C to be added to board
    for i in range(num_of_A):
        A_blocks.append('A')
    for i in range(num_of_B):
        B_blocks.append('B')
    for i in range(num_of_C):
        C_blocks.append('C')
    
   
    
    ##Delete o's from flattened array and replace them with the instances of A, B, and C
    for i in range(total_number_of_blocks):
        new_flat = np.delete(new_flat,0)
        
    
    all_arrs = (A_blocks,B_blocks,C_blocks, new_flat)
    flattened_with_blocks = np.concatenate(all_arrs)
    
    
    #Create Array of all Possible Board Permutations    
    added_blocks_permutations = []
    flattened_permutations = multiset_permutations(flattened_with_blocks)
    
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
            row_num = i // board_rows
            col_num = i % board_rows
            if block_type != 'o' and (row_num,col_num) not in fixed_blocks:
                added_blocks_set.append((block_type, row_num, col_num))
        added_blocks_permutations.append(added_blocks_set)
    
    return added_blocks_permutations

def rebuild_matrix(original_board, added_block_set):
    
    board_array = np.array(original_board)
    board_rows, board_col = board_array.shape
    
    new_board_matrix = original_board
    
    for i in (added_block_set):
        added_type = i[0]
        added_x = i[1]
        added_y = i[2]
        new_board_matrix[added_x][added_y] = added_type
            
    
    return new_board_matrix

def get_All_Left_Walls(board):
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
    reflect_walls = []
    all_walls = get_All_Walls(board)
    for i in range(len(all_walls)):
        block_type = all_walls[i][0]
        if block_type == 'A':
            reflect_walls.append(all_walls[i][1])
    
    return list(set(reflect_walls))

def get_All_Opaque_Walls(board):
    opaque_walls = []
    all_walls = get_All_Walls(board)
    for i in range(len(all_walls)):
        block_type = all_walls[i][0]
        if block_type == 'B':
            opaque_walls.append(all_walls[i][1])
    
    return list(set(opaque_walls))

def get_All_Refract_Walls(board):
    refract_walls = []
    all_walls = get_All_Walls(board)
    for i in range(len(all_walls)):
        block_type = all_walls[i][0]
        if block_type == 'C':
            refract_walls.append(all_walls[i][1])
    
    return list(set(refract_walls))

if __name__ == "__main__":
    #Create a fixed set of all the intersection point
    board, A, B, C, lasers, laser_dir, points = read_board('mad_1.bff')
    Board1 = Board(board, A, B, C, lasers, laser_dir, points)
    
    board_height, board_width = board.shape
    matrix_height = board_height*2 + 1
    matrix_width = board_width*2+1

    num_A_blocks = Board1.get_A_Blocks()
    num_B_blocks = Board1.get_B_Blocks()
    num_C_blocks = Board1.get_C_Blocks()
    
    board_permutations = get_board_permutations(board,num_A_blocks,num_B_blocks,num_C_blocks)
    
    print(board_permutations[1])
    print(rebuild_matrix(board,board_permutations[1]))
    
    new_board = rebuild_matrix(board,board_permutations[1])
    
    m = Matrix(board_width,board_height)
    target_list = Board1.get_points()
    laser_list = Board1.get_Lasers()
    laser_dir_list = Board1.get_Lasers_dir()
    reflect_list = get_All_Reflect_Walls(new_board)
    refract_list = get_All_Refract_Walls(new_board)
    opaque_list = get_All_Opaque_Walls(new_board)
    
    print(target_list)
    print(laser_list)
    print(laser_dir_list)
    print(reflect_list)
    print(refract_list)



    
    
  