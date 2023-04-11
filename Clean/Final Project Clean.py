import numpy as np
import copy
from sympy.utilities.iterables import multiset_permutations
from laser import *
from block import *
from board import *


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
        
        length_of_laser_list = len(laser_list)
        index = 0
        
        #Initial Step
        
        while index != length_of_laser_list:
            current_pos = laser_list[index]
            laser_direction = laser_dir_list[index]
            interaction = laser_1_step(m,current_pos, laser_direction)
            interaction_len = 0
            validate = bool()
         
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
                    
                    # This is a Refract interaction. Create a new laser and add it to the list
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
                    # This is a Refract interaction. Create a new laser and add it to the list
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
        
        if target_list_set.issubset(laser_path_set) :
            Does_Laser_Hit_Targets = True
            true_path_index = board_permutations_index
        
        if (board_permutations_index == total_permutations):
            Does_Laser_Hit_Targets = True
            
            
        board_permutations_index+=1

        
    if(Does_Laser_Hit_Targets):
        print("Here is the path the laser takes")
        m.print_matrix_with_indices()
    
        print("Targets: ", target_list_set)
        print("Laser Path: ", laser_path_set)
        print("")
        print("You want to place the blocks in the following position: ", board_permutations[true_path_index])
        print("This placement should yield the correct solution")
        print(rebuild_matrix(board,board_permutations[true_path_index]))
        



    
    
  