import argparse
import os
import pprint as pp
import subprocess


from tqdm import tqdm
from zenlog import log


class gaussian_file_calculator():

    def __init__(self):
        args = self.command_parser()
        config_dict = self.gjf_settings()
        # self.prepare_files(config_dict)       

    def command_parser(self):
        parser = argparse.ArgumentParser(description='Prepare and send .pdb files to gaussian06 for calculations.')
        parser.add_argument('-mail', type=str, nargs='?', default=' ', metavar='m', dest='mail', help='Input mail adress to recieve text results.')
        args = parser.parse_args()
        return args

    def gjf_settings(self):
        config_dict = {}
        file_list = [file for file in os.listdir() if file.endswith('.pdb')]
        
        if len(file_list) == 0:
            log.e(f'\'.pdb\' files not found in directory \'{os.path.basename(os.getcwd())}\'. Aborting...')
            quit()
        

        log.i(f'{len(file_list)} files found. Gathering settings...')
        
        while True:
            try:
                log.d('How many calculations do you wish to perform?')
                ncalc = int(input())
                log.d('Do you want to set number of processors used and memory size available? Default is 8 processors and 1gb memory. (Y/N) ')
                query = input()
                nproc, mem = 8, 1
                if query.lower() == 'y':
                    log.d('How many procesors do you wish to use? ')
                    nproc = int(input())
                    log.d('How much memory do you want to use? ')
                    mem = float(input())
                break
            except:
                log.w('You have not provided a valid input, please try again.')

        config_dict['ncalc'] = ncalc
        config_dict['nproc'] = nproc
        config_dict['mem'] = mem
        config_dict['chk'] = 'chkfile.chk'

        for calc_number in range(ncalc):
            log.d(f'For calculation number {calc_number}, select calculation type:'
            '\n1) DFTmin_opt\n2) MP2min_sp\n3) M062Xmin_opt\n4) M062max_sp')    
            

        pp.pprint(config_dict)
        return config_dict



    def prepare_files(self, config_dict):
        file_list = [file for file in os.listdir() if file.endswith('.pdb')]
        
        for file in file_list:
            file_name = file[:-4]
            subprocess.call([f'obabel {file} -O {file_name}.xyz'], shell=True, stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)

        xyz_list = [file for file in os.listdir() if file.endswith('.xyz')]
        for xyz_file in xyz_list:
            with open(xyz_file, 'w') as f:
                f.write(config_dict['nproc'])

init_prog = gaussian_file_calculator() 