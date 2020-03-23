import copy
import datetime
import math as m
import os
import pprint as pp
from re import sub

import numpy as np
from prettytable import PrettyTable
from zenlog import log

KB = 0.0019872041 # kcal/mol
TEMP = 293.15 # K

class find_molecule_percentage():

    def __init__(self):
        data_list  = self.get_data()
        min_value, min_names = self.lowest_energy_molecule(data_list)
        boltz_list, boltz_final = self.boltzmann_distr(data_list, min_value)
        self.save_values_in_file(data_list, min_value, min_names, boltz_list, boltz_final)

    def get_data(self):

        # Gets energies stored in *.txt files
        file_list = [file for file in os.listdir() if file.endswith('.txt')]
        for current_file in file_list:
            log.i('Reading \'{}\'.'.format(current_file))
            with open(current_file, 'r') as f:
                text = f.readlines()
                data_list = []
                for line in text:
                    line_dict = {}
                    line = line.split()
                    line_dict['name'] = line[0][:-1]
                    line_dict['energy'] = float(line[-1])
                    data_list.append(line_dict)

        # Orders data list
        ordered_data_list = [None] * (len(data_list)+1)
        for molecule in data_list:
            numer = int(sub("[^0-9]", "", molecule['name']))
            ordered_data_list[numer] = molecule 
        data_list = ordered_data_list
        for item in data_list:
            if item is None:
                data_list.remove(item)
        return data_list

    def lowest_energy_molecule(self, data_list):

        # Converts each energy value from Hartree (Ha) to kcal/mol
        for molecule in data_list:
            molecule['energy'] = molecule['energy'] * 627.51
        min_value = min([molecule['energy'] for molecule in data_list])
        min_names = []
        for molecule in data_list:
            molecule_data = list(molecule.values())
            if min_value in molecule_data:
                min_names.append(molecule_data[0])
            molecule['energy'] -= min_value
        log.i('Minimum energy {} was found on file(s) {}'.format(min_value, min_names))
        return min_value, min_names

    def boltzmann_distr(self, data_list, min_value):
        energy_list = [np.float128(molecule['energy']) for molecule in data_list]
        boltz_list = [np.exp((0-en)/(KB*TEMP)) for en in energy_list]

        # Only leaves one energy minimum in energy_list
        no1_count = 0
        for count, number in enumerate(boltz_list):
            if number == 1 and no1_count > 0:
                del boltz_list[count]
                no1_count += 1
            elif number == 1:
                no1_count += 1   

        boltz_total = sum(boltz_list)
        boltz_final = [round((bol/boltz_total)*100, 4) for bol in boltz_list]
        return boltz_list, boltz_final

    def save_values_in_file(self, data_list, min_value, min_names, boltz_list, boltz_final):

        time = datetime.datetime.now()
        file_name = ('min_energy_table-{}.out'.format(time.strftime("%d-%m-%y_%H:%M")))
        x = PrettyTable()
        x.field_names = ['Molecule Name', 'Energy', '% in equilibrium']
        energy_list = [molecule['energy'] for molecule in data_list]
        name_list = [molecule['name'] for molecule in data_list]
        for j in energy_list:     
            for i in name_list:
                name_list.remove(i)
                for k in boltz_final:
                    x.add_row([i, j, k])
                    boltz_final.remove(k)
                    break  
        table_title = ('Relative energies in kcal/mol')
        print(x.get_string(title=table_title))
        with open(file_name, 'w+') as f:
            f.write('Minimum energy: {}\n'.format(min_value))
            f.write(str(x.get_string(title=table_title)))
        log.info('Data correctly saved as \'{}\' in \'{}\''.format(file_name, os.getcwd()))
        return str(x)



# Después necesito saber qué porcentaje de cada molécula tengo en equilibrio, asumiendo una distribución de Boltzmann (son conformaciones de una misma molécula que están en equilibrio). 
# La fórmula es Pi/Pj = e((Gi-Gj)/KbT)  (e elevado a (Gi-Gj/KbT, puedes ver la fórmula en el artículo de la Wikipedia de la distribución de Boltzmann).
# Donde Kb es la constante de Boltzmann i T la temperatura (supondriamos T ambiente, 20 grados, en K, supongo...)

aa = find_molecule_percentage()
