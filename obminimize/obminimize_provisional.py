import os
import time


class obmini_molecules():
    def __init__(self):
        self.obmini_files()

    def obmini_files(self):    
        file_list =  [file for file in os.listdir() if file.endswith('.pdb')]
        time_start = time.time()
        for count, file in enumerate(file_list):
            minimized_file_name = 'obmini_'+file
            print("Optimizing file {} of {}.".format(count, len(file_list)))
            os.system('obabel {} -O {} --gen3d --conformer --log --nconf 200 --weighted'.format(file, minimized_file_name))
        time_end = time.time()
        print("{} files done in {}s".format(len(file_list),round(time_end-time_start,3)))

at = obmini_molecules()