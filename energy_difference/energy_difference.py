import os
from zenlog import log

file_names = [filename for filename in os.listdir() if filename.endswith('.txt')]

for file in file_names:
    with open(file, 'r') as f:
        log.d(f'Reading file: \'{file}\'')
        lines = f.readlines()
        for line in lines:
            line = line.strip().split()
            difference = abs(float(line[1])-float(line[2]))*627.51
            log.i(f'Energy difference in {line[0]} is {difference:.5}')
        log.d(f'File \'{file}\' done.')
