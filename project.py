import numpy as np
from sympy.utilities.iterables import multiset_permutations


class Lazor:
    '''
    This class carries creates a Lazor objecct.
   
    '''
    
    direction = None
    board_rows = None
    board_col = None
    
    def __init__(self, start_x, start_y, trajectory_x, trajectory_y, end_x = 0, end_y = 0):
        '''
        Initializes the Lazor object
        '''
        self.start_x = start_x
        self.start_y = start_y
        self.trajectory_x = trajectory_x
        self.trajectory_y = trajectory_y
        
        if trajectory_x > 0 and trajectory_y > 0:
            self.direction = 'bottom_Right'
            self.end_x = self.board_rows
            self.end_y = self.board_col
        if trajectory_x < 0 and trajectory_y > 0:
            self.direction = 'bottom_Left'
            self.end_x = 0
            self.end_y = self.board_col
        if trajectory_x > 0 and trajectory_y < 0:
            self.direction = 'top_Right'
            self.end_x = self.board_rows
            self.end_y = 0
        if trajectory_x < 0 and trajectory_y < 0:
            self.direction = 'top_Left'
            self.end_x = 0
            self.end_y = 0
            
    
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
            
    points_set = set()


    for i in range(len(points)):
        x_coordinate = int(points[i][2])
        y_coordinate = int(points[i][4])
        points_set.add((x_coordinate, y_coordinate))
        
    lasers_set = set()


    for i in range(len(lasers)):
        laser_string_arr = lasers[i].split(' ')
        x_coordinate = int(laser_string_arr[1])
        y_coordinate = int(laser_string_arr[2])
        vx_coordinate = int(laser_string_arr[3])
        vy_coordinate = int(laser_string_arr[4])
        
        lasers_set.add((x_coordinate, y_coordinate,vx_coordinate, vy_coordinate))
        
      
    board_matrix_array = np.array(board_matrix)  
      
    return board_matrix_array, A_blocks, B_blocks, C_blocks, lasers_set, points_set

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
                left_walls_arr.append(selected_block.get_Left_Wall())
    
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
                right_walls_arr.append(selected_block.get_Right_Wall())
    
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
                top_walls_arr.append(selected_block.get_Top_Wall())
    
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
                bottom_walls_arr.append(selected_block.get_Bottom_Wall())
    
    return bottom_walls_arr

if __name__ == "__main__":
    #Create a fixed set of all the intersection point
    board, A, B, C, lasers, points = read_board('mad_7.bff')
    Board1 = Board(board, A, B, C, lasers, points)
    num_A_blocks = Board1.get_A_Blocks()
    num_B_blocks = Board1.get_B_Blocks()
    num_C_blocks = Board1.get_C_Blocks()
    
    board_permutations = get_board_permutations(board,num_A_blocks,num_B_blocks,num_C_blocks)
    
    print(board_permutations[1])
    print(rebuild_matrix(board,board_permutations[1]))
    
    new_board = rebuild_matrix(board,board_permutations[1])
    
    print(get_All_Left_Walls(new_board))




    
    
  