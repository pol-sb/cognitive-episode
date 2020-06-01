import math as m
import numpy as np
import os
import pprint as pp
import subprocess


from zenlog import log



class amine_distance():
    def __init__(self):
        result_dict = self.atom_index_finder()
        dist = self.pyramid_calculator(result_dict)

    def atom_index_finder(self):
        temp_file_list = [file for file in os.listdir() if file.endswith('.xyz')]
        result_dict = {}
        for file in temp_file_list:
            filename = file[:-4]
            result_dict[filename] = {}
            subprocess.call([f'obabel -i xyz {file} -O {filename}.pdb'], shell=True, stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
            with open(f'{filename}.pdb', 'r') as f:
                for line in f:
                    if ' N ' in line and ' O ' not in next(f):
                        nitrog_temp_list = line.strip()
                        nitrog_temp_list = nitrog_temp_list.split()
                        nitrogen_coords = [float(coordinate) for coordinate in nitrog_temp_list[5:8]]
                        nitrog_posc = nitrog_temp_list[1]
                    
                f.seek(0)
                
                # Following section could be improved
                bonded_atoms = [line.split()[1:] for line in f if 'CONECT' in line]   
                bonded_atoms = [elements for elements in bonded_atoms if elements[0] == nitrog_posc]

                for element in bonded_atoms:
                    element.remove(nitrog_posc)
                bonded_atoms = bonded_atoms[0]
                f.seek(0)
                atom_coords = []
                for line in f:
                    if line.split()[0] not in ['END', 'CONECT'] and line.split()[1] in bonded_atoms:
                        temp_coords = [float(num) for num in line.split()[5:8]]
                        atom_coords.append(temp_coords)

                result_dict[filename]['atom_coords'] = atom_coords
                result_dict[filename]['nitrogen_coords'] = nitrogen_coords

        return result_dict                

    def pyramid_calculator(self, result_dict):
        for file in result_dict.items():
        
            n_coord = np.array(file[1]['nitrogen_coords'])
            at_coord = file[1]['atom_coords']
            
            v1 = np.array(at_coord[1]) - np.array(at_coord[0])
            v2 = np.array(at_coord[2]) - np.array(at_coord[1])
            v3 = np.array(at_coord[0]) - np.array(at_coord[2])
            
            # Gives a vector with 3 coord. which correspond to ...
            # ... (a,b,c) in plane equation ax+by+cz+d=0
            abc = np.cross(v1,v2)
            d = -(abc[0]*np.array(at_coord[0][0])+abc[1]*np.array(at_coord[0][1])+abc[2]*np.array(at_coord[0][2]))

            # Equation was too long to fit in one line
            distance_num = (abs((abc[0]*n_coord[0])+((abc[1]*n_coord[1])+((abc[2]*n_coord[2])+d))))     
            distance_deno = (m.sqrt((abc[0]**2)+(abc[1]**2)+(abc[2]**2)))
            dist = distance_num/distance_deno

            print()
            log.i(f'Results from file \'{file[0]}\': ')
            log.d(f'Plane equation: {abc[0]}x + {abc[1]}y + {abc[2]}z + {d}')
            log.d(f'Coordinates from surrounding atoms: {at_coord}')
            log.d(f'Nitrogen coordinates: {n_coord}')
            log.i(f'Nitrogen planar distance: {dist} (A)\n')
            log.w(f'File \'{file[0]}\' done, proceeding with next file if possible...')
            subprocess.call([f'rm {file[0]}.pdb'], shell=True, stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
        return dist

at = amine_distance()
print()
