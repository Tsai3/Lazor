import numpy as np
from block import *
from sympy.utilities.iterables import multiset_permutations
import copy
"""
Created on Saturday, April 8,2023, 10:23:38 PM
@author: Luke
"""
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

def get_board_permutations(board, num_of_A, num_of_B, num_of_C):
    '''
    Takes in a 2D-Matrix of the board, the number of A blocks, the number of B blocks, and the number of C blocks
    
    Returns an array with each element containing set of tuples in the form of (blockType, x-coordinate, y-coordinate) for each added block and the number of fixed blocks
    '''
    
    board_array = np.array(board)
    board_rows, board_col = board_array.shape
    
    ##Get Fixed Block Locations and x Locations
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
    
    test_me = True
    
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

        A_block_count = 0
        B_block_count = 0
        C_block_count = 0
        
        
        for i in range(len(restored_board_permutation)):
            
            block_type = restored_board_permutation[i]
            row_num = i // board_col
            col_num = i % board_col
            
                
            
            if block_type != 'o' and (row_num, col_num) not in fixed_blocks:
                    
                added_blocks_set.append((block_type, col_num, row_num))

        for item in added_blocks_set:
            if 'A' in item:
                A_block_count += 1
            if 'B' in item:
                B_block_count += 1   
            if 'C' in item:
                C_block_count += 1
                
        ## Only adds permutations that use all the blocks we have, as sometimes the permutations leave out blocks        
        if (A_block_count >= num_of_A) and (B_block_count >= num_of_B) and (C_block_count >= num_of_C):      
            added_blocks_permutations.append(added_blocks_set)     
                
    
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
        new_board_matrix[added_x][added_y] = added_type
            
    
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




        
  