import math as m
import numpy as np
import os
import subprocess



class amine_distance():
    def __init__(self):
        at_coord, n_coord = self.atom_index_finder()
        dist = self.pyramid_calculator(at_coord, n_coord)


    def atom_index_finder(self):
        temp_file_list = [file for file in os.listdir() if file.endswith('.xyz')]
        for file in temp_file_list:
            filename = file[:-4]
            subprocess.call([f'obabel -i xyz {file} -O {filename}.pdb'], shell=True, stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
            with open(f'{filename}.pdb', 'r') as f:
                nitrog_temp_list = [line.strip() for line in f if ' N ' in line]
                nitrog_temp_list = nitrog_temp_list[0].split()
                nitrogen_coords = [float(coordinate) for coordinate in nitrog_temp_list[5:8]]
                nitrog_posc = nitrog_temp_list[1]
                f.seek(0)
                
                # Following section could be improved
                bonded_atoms = [line.strip() for line in f if f' {nitrog_posc} ' in line and 'CONECT    ' in line]   
                bonded_atoms = [element.split()[2:] for element in bonded_atoms if element.split()[1] == '1']
                bonded_atoms = [element for element in bonded_atoms[0]]
                f.seek(0)
                atom_coords = []
                for line in f:
                    if line.split()[0] not in ['END', 'CONECT'] and line.split()[1] in bonded_atoms:
                        temp_coords = [float(num) for num in line.split()[5:8]]
                        atom_coords.append(temp_coords)
                        
        print('nitrogen_coords: ', nitrogen_coords)
        print('atom_coords: ', atom_coords)
        return atom_coords, nitrogen_coords                

    def pyramid_calculator(self, at_coord, n_coord):
        n_coord = np.array(n_coord)
        v1 = np.array(at_coord[1]) - np.array(at_coord[0])
        v2 = np.array(at_coord[2]) - np.array(at_coord[1])
        v3 = np.array(at_coord[0]) - np.array(at_coord[2])
        
        # Gives a vector with 3 coord. which correspond to ...
        # ... (a,b,c) in plane equation ax+by+cz+d=0
        abc = np.cross(v1,v2)
        d = -(abc[0]*np.array(at_coord[0][0])+abc[1]*np.array(at_coord[0][1])+abc[2]*np.array(at_coord[0][2]))
        print(f'Plane equation: {abc[0]}x + {abc[1]}y + {abc[2]}z + {d}')

        # Equation was too long to fit in one line

        distance_num = (abs((abc[0]*n_coord[0])+((abc[1]*n_coord[1])+((abc[2]*n_coord[2])+d))))
        
        distance_deno = (m.sqrt((abc[0]**2)+(abc[1]**2)+(abc[2]**2)))
        dist = distance_num/distance_deno
        print('dist: ', dist)
        return dist



at = amine_distance()
