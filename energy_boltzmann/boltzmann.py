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
        log.i('Minimum energy {} was found on file(s) {}.'.format(min_value, min_names))
        return min_value, min_names

    def boltzmann_distr(self, data_list, min_value):
        energy_list = [np.float128(molecule['energy']) for molecule in data_list]
        boltz_list = [np.exp((0-en)/(KB*TEMP)) for en in energy_list]

        # Only leaves one energy minimum in boltz_list
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

        # Only leaves one energy minimum in energy_list
        no1_count = 0
        for count, number in enumerate(energy_list):
            if number == 0 and no1_count > 0:
                del boltz_list[count]
                no1_count += 1
                deleted_index = count
            elif number == 0:
                no1_count += 1 

        result_dict_list = []
        for name in name_list:
            molecule_dict = {}
            molecule_dict['name'] = name
            result_dict_list.append(molecule_dict)

        count_min = 0
        for molecule in result_dict_list:
            for energy in energy_list:
                molecule['energy'] = energy
                energy_list.remove(energy)
                count_min += 1
                break

        boltz_final.insert(deleted_index, 0.0)
        for molecule in result_dict_list:
            for percent in boltz_final:
                molecule['percent'] = percent
                boltz_final.remove(percent)
                break

        for molecule in result_dict_list:
            x.add_row([molecule['name'], molecule['energy'], molecule['percent']])
                       
        table_title = ('Relative energies in kcal/mol')
        print(x.get_string(title=table_title))
        with open(file_name, 'w+') as f:
            f.write('Minimum energy: {}\n'.format(min_value))
            f.write(str(x.get_string(title=table_title)))
        log.info('Data correctly saved as \'{}\' in \'{}\''.format(file_name, os.getcwd()))
        return str(x)

aa = find_molecule_percentage()
