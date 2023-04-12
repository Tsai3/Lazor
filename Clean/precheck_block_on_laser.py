# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 00:03:04 2023

"""

'newly added-------------------------------------------------------------------------------------------'
def precheck_block_on_laser (matrix, A_position, B_position, C_position, laser_list, laser_direction):
    '''
    this is the function to check if there is any block already on the laser path 
    when no step is taken. 
    
    Return
        True: if there is at lease one block on the laser path
        False: if there is no block on the laser path
    '''
    laser_path_before_test = []
    for index in len(laser_list):
        current_pos = laser_list[index]
        laser_direction = laser_dir_list[index]
        next_pos = current_pos + laser_direction
        if next_pos in matrix:
            laser_path_before_test.append(next_pos)
    
    validation = bool('True')
    for position in laser_path_before_test:
        if position not in A_position and B_position and C_position:
            validation = ('False')
    
    return validation

'---------------------------------------------------------------------'

if __name__ == "__main__":
    
    print("Enter Name of the Board (include '.bff').")
    filename = input()
    #Create a fixed set of all the intersection point
    board, A, B, C, lasers, laser_dir, points = read_board(filename)
    Original_Board = Board(board, A, B, C, lasers, laser_dir, points)
    print("Original Board: ")
    print(board)
    board_height, board_width = board.shape
    matrix_height = board_height*2 + 1
    matrix_width = board_width*2 + 1

    num_A_blocks = Original_Board.get_A_Blocks()
    num_B_blocks = Original_Board.get_B_Blocks()
    num_C_blocks = Original_Board.get_C_Blocks()
    
    board_permutations, fixed_count= get_board_permutations(board,num_A_blocks,num_B_blocks,num_C_blocks)
    
    total_permutations = len(board_permutations)
    print("There are ",total_permutations, "permutations of solutions")
    board_permutations_index = 0
    true_path_index = 0
    Does_Laser_Hit_Targets = False
    
    m = Matrix(matrix_width,matrix_height)
    
    target_list_len = len(copy.copy(Original_Board.get_points()))
    
    current_match = 0
    laser_path_points_to_remember = list()
    untouched_blocks = []   
    
    # The below while loop will run laser on the board with variouds block location generated 
    # from the permutation
    while Does_Laser_Hit_Targets != True:
        
        Board1 = Board(board, A, B, C, lasers, laser_dir, points)
        placed_count = 0
        total_allowed_to_be_placed = num_A_blocks+num_B_blocks+num_C_blocks       

        new_board = rebuild_matrix(board,board_permutations[board_permutations_index])
        
        target_list = copy.copy(Board1.get_points())
        laser_list = copy.copy(Board1.get_Lasers())
        laser_dir_list = copy.copy(Board1.get_Lasers_dir())
        reflect_list = get_All_Reflect_Walls(new_board)
        refract_list = get_All_Refract_Walls(new_board)
        opaque_list = get_All_Opaque_Walls(new_board)
        
        m = Matrix(matrix_width,matrix_height)
        
        set_targets(m,target_list)
        set_laser(m, laser_list)  
        set_reflect(m,reflect_list)
        set_opaque(m,opaque_list)
        set_refract(m,refract_list)
'newly added-------------------------------------------------------------------------------------------'
        # check if no any block is on laser path. If not then skip the following code and 
        # go back to the while
        if precheck_block_on_laser (m, reflect_list, refract_list, opaque_list, laser_list, laser_dir_list):
            continue
        
        length_of_laser_list = len(laser_list)
        index = 0
        
        #Initial Step
        
        while index != length_of_laser_list:
            current_pos = laser_list[index]
            laser_direction = laser_dir_list[index]
'newly added-------------------------------------------------------------------------------------------'
