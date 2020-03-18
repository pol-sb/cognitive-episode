import datetime
import os
import pprint as pp

from zenlog import log


class find_molecule_percentage():

    def __init__(self):
        data_list = self.get_data()
        self.lowest_energy_molecule(data_list)

    def get_data(self):

        # Gets energies stored in *.txt files
        file_list = [file for file in os.listdir() if file.endswith('.txt')]
        for current_file in file_list:
            with open(current_file, 'r') as f:
                text = f.readlines()
                data_list = []
                for line in text:
                    line_dict = {}
                    line = line.split()
                    line_dict['name'] = line[0][:-1]
                    line_dict['energy'] = float(line[-1])
                    data_list.append(line_dict)
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

        time = datetime.datetime.now()
        with open('min_energy_results_{}'.format(time.strftime("%d-%m-%y")),'w+') as f:
            for molecule in data_list:
                if molecule['energy'] != 0:
                    log.d('{} relative energy:\t{}  kcal/mol.'.format(molecule['name'], molecule['energy']))
                    f.write('{} \t {}\n'.format(molecule['name'], molecule['energy']))
        log.i('Results saved in \'min_energy_results_{}\'.'.format((time.strftime("%d-%m-%y"))))


            

                




aa = find_molecule_percentage()
