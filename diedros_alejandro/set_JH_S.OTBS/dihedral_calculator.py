import datetime
import os

import numpy as np

# Change the values below to the index of the 4 atoms desired for calculations.
ATOMS = [8, 10, 60, 76]


class dihedral_angle_calculator():

    def __init__(self):
        pos_list = self.get_positions()
        dihedral_list = self.calculate_dihedral(pos_list)
        self.results_to_file(dihedral_list)

    def get_positions(self):
        temp_file_list = [
            file for file in os.listdir() if file.endswith('.xyz')]
        coord_dict = {}
        for file in temp_file_list:
            with open(file, 'r') as f:
                f.readline()
                f.readline()
                text = f.readlines()
                posc_list = [line.split()
                             for line in text if len(line.split()) == 4]
                for atom_number, atom in enumerate(posc_list):
                    atom[:0] = [atom_number]
                atom_calc_list = [at for at in posc_list if at[0] in ATOMS]
                coord_dict[file] = atom_calc_list
        return coord_dict

    def calculate_dihedral(self, coord_dict):
        dihedral_list = []
        for molecule in coord_dict.items():
            molec_name = (molecule[0]).replace('.xyz', '')
            atom_list = molecule[1:]
            for atom_set in atom_list:
                coord_set = []
                for atom_coords in atom_set:
                    atom_coords = [float(num) for num in atom_coords[2:]]
                    coord_set.append(np.array(atom_coords))
                vec1 = coord_set[1] - coord_set[0]
                vec2 = coord_set[2] - coord_set[1]
                vec3 = coord_set[3] - coord_set[2]
                n1 = np.cross(vec1, vec2)
                n2 = np.cross(vec2, vec3)
                uvec2 = vec2/(np.sqrt(np.sum(np.square(vec2))))
                m1 = np.cross(n1, uvec2)
                x = np.dot(n1, n2)
                y = np.dot(m1, n2)
                dihedral_rads = np.arctan2(y, x)
                dihedral = np.degrees(dihedral_rads)
                dihedral_list.append([molec_name, dihedral])
                print(f'The dihedral angle between the atoms {ATOMS} of '
                      f'{molec_name} is {dihedral:5f}º.')
        return dihedral_list

    def results_to_file(self, dihedral_list):
        time = datetime.datetime.now()
        with open(f'dihedral_results_{time.strftime("%d-%m-%y")}','w+') as f:
            for molecule in dihedral_list:
                line = f'{molecule[0]:30} {round(molecule[1],5):>40}º\n'
                f.write(line)


at = dihedral_angle_calculator()
