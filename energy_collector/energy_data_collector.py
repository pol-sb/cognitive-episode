import argparse
import datetime
import getpass
import os
import pprint as pp
import re
import subprocess

import prettytable
from prettytable import PrettyTable
from zenlog import log


DFT_RE = re.compile(r'SCF Done:.*=\s+([^\n]+\d+\.\d+)')
M06_RE = re.compile(r'RM062X.*=\s+([^\n]+\d+\.\d+)')
FRQ_RE = re.compile(r'Free Energies=\s+([^\n]+\d+\.\d+)')
ENT_RE = re.compile(r'Enthalpies=\s+([^\n]+\d+\.\d+)')
USER = getpass.getuser()


class energy_data_collector():

    def __init__(self):
        args = self.command_parser()        
        energies, folder_names = self.get_energies_from_files()
        self.print_energies_on_file(energies, folder_names, args)

    def command_parser(self):
        parser = argparse.ArgumentParser(description='Calculate energy results.')
        parser.add_argument('-mail', type=str, nargs='?', default=' ', metavar='m', dest='mail',
                        help='Input mail adress to recieve text results.')
        args = parser.parse_args()
        return args

    def get_energies_from_files(self):
        log.d('Getting energies from files.')
        energies_dict = {}
        folder_names = [folder for folder in next(os.walk('.'))[1] if folder[0].isnumeric()]
        folder_names.sort()
        for folder_name in folder_names:
            try:
                temp_file_list = [file for file in os.listdir(folder_name) if file.endswith('.log')]
            except FileNotFoundError:
                continue
            for molecule_name in temp_file_list:
                text = None
                temp_dict = {}
                with open(folder_name+'/'+molecule_name, 'r') as f:
                    text = f.read()
                if 'DFT' in folder_name or 'MP2min' in folder_name:
                    energy_value = round(float(DFT_RE.findall(text)[-1]), 5)
                    temp_dict[folder_name] = energy_value
                elif 'M062X' in folder_name:
                    energy_value = round(float(M06_RE.findall(text)[-1]), 5)
                    temp_dict[folder_name] = energy_value
                elif 'freq' in folder_name:
                    free_energ = round(float(FRQ_RE.findall(text)[-1]), 5)
                    enthalp = round(float(ENT_RE.findall(text)[-1]), 5)
                    energy_value = 'Free Energy: ' + str(free_energ) +'\nEnthalpy: ' + str(enthalp)
                    temp_dict[folder_name] = energy_value
                if molecule_name[:-4] not in energies_dict:
                    energies_dict[molecule_name[:-4]] = [temp_dict]
                else:
                    energies_dict[molecule_name[:-4]].append(temp_dict)
        log.i(f'Energies from {len(energies_dict.keys())} files recovered.')
        return energies_dict, folder_names

    def print_energies_on_file(self, energy_dict, folder_names, args):
        time = datetime.datetime.now()
        file_name = (f'{USER} - {time.strftime("%d-%m-%y")}.txt')
        x = PrettyTable()
        folder_names.insert(0, 'Molecule Name')
        x.field_names = folder_names 
        temp_table = list(energy_dict.values())      
        temp_table2 = list(energy_dict.keys())
        for j in temp_table:     
            for i in temp_table2:
                cont = 0
                lista1 = [i]
                while cont < len(j):
                    try:
                        valor = list(j[cont].values())[0]
                    except IndexError:
                        valor = '    '
                    lista1.append(valor)
                    cont += 1
                try:
                    x.add_row(lista1)
                except Exception:
                    log.e('There is not the same number of files in all the directories. Energy collection halted...')
                temp_table2.remove(i)
                break
        x.sortby = 'Molecule Name'
        table_title = (f'{USER} - {time.strftime("%d-%m-%y")} - Gaussian Energy Calculation Results')
        x.hrules = prettytable.ALL
        print(x.get_string(title=table_title))
        with open(file_name, 'w+') as f:
            f.write(str(x.get_string(title=table_title)))
        subprocess.call([f'obabel -i pdb *.pdb -O {time.strftime("%d-%m-%y")}-molecules.svg -d -xC'], shell=True, stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
        log.info(f'Data correctly saved as \'{file_name}\' in \'{os.getcwd()}\'')
        log.info(f'Molecule structure drawn in \'{time.strftime("%d-%m-%y")}-molecules.svg\' in \'{os.getcwd()}\'')
        if args.mail != ' ':
            email = args.mail
            subprocess.call(['cat "{}" | mail -s "Results - {}"  {}'.format(file_name, time.strftime("%d-%m-%y"), email)], shell=True, stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
            log.info('Results delivery attempted in {}'.format(email))
        return str(x)
 

at = energy_data_collector()
