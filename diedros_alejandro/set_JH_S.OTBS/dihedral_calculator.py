import os

import numpy as np

# Change the values below to the index of the 4 atoms desired for calculations. 
ATOMS = [8, 10, 60, 76]

class dihedral_angle_calculator():

    def __init__(self):
        pos_list = self.get_positions()
        self.calculate_dihedral(pos_list)

    def get_positions(self):
        temp_file_list = [file for file in os.listdir() if file.endswith('.xyz')]
        coord_dict = {}
        for file in temp_file_list:
            with open(file, 'r') as f:
                f.readline()
                f.readline()
                text = f.readlines()
                posc_list = [line.split() for line in text if len(line.split()) == 4]
                for atom_number, atom in enumerate(posc_list):
                    atom[:0] = [atom_number]
                atom_calc_list = [at for at in posc_list if at[0] in ATOMS]
                coord_dict[file]= atom_calc_list
        return coord_dict

    def calculate_dihedral(self, coord_dict):
        for molecule in coord_dict.items():
            atom_list = molecule[1:]
            # for coords in atom_list:
# 
at = dihedral_angle_calculator()