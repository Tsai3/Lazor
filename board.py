import numpy as np
from sympy.utilities.iterables import multiset_permutations

class Board:
    '''
    This class carries creates a Board objecct.
   
    '''
    
    
    def __init__(self, board_matrix, A, B, C, lasers, points):
        '''
        Initializes the Board object that takes in a matrix of board symbols, strings of A blocks, B blocks and C blocks, strings of lasers and srrings of points
        '''
        self.board_matrix = board_matrix
        self.A = A
        self.B = B
        self.C = C
        self.lasers = lasers
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
    
    def get_points(self):
        return self.points
    
    def add_Lazor(self,x_coordinate, y_coordinate,vx_coordinate, vy_coordinate):
        self.lasers.add((x_coordinate, y_coordinate,vx_coordinate, vy_coordinate))
       
            
    


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



if __name__ == "__main__":
    #Create a board object
    board, A, B, C, lasers, points = read_board('mad_1.bff')
    Board1 = Board(board,A,B,C,lasers,points)

    
    print(Board1.get_Board_Matrix())
    print(Board1.get_A_Blocks())
    print(Board1.get_B_Blocks())
    print(Board1.get_C_Blocks())
    print(Board1.get_Lasers())
    print(Board1.get_points())
    
    
    Board1.add_Lazor(0,0,1,1)
    print(Board1.get_Lasers())
    

    
    

        
  