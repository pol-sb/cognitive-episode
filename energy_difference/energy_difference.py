import os
from zenlog import log

file_names = [filename for filename in os.listdir() if filename.endswith('.txt')]

for file in file_names:
    filename = file[:-4]
    string_table = []
    with open(file, 'r') as f:
        log.d(f'Reading file: \'{file}\'')
        lines = f.readlines()
        for line in lines:
            line = line.strip().split()
            try:
                difference = abs(float(line[1])-float(line[2]))*627.51
                for index1, value in enumerate(line):
                    if (value.lstrip('+-').replace('.','')).isdigit():
                        line[index1] = str(round(float(value), 5))
                line.append(str(round(difference, 2))+'\n')
                log.i(f'Energy difference in {line[0]} is {difference:.5}')
                line = '\t'.join(line)
                string_table.append(line)
            except IndexError:
                log.e(f'File \'{file}\' has incorrect format. Please make sure you are in the correct directory, or change the file format.')
                quit()

    with open(f'diff_{filename}', 'w') as diff_text:
        for item in string_table:
            diff_text.write(item)
    
    log.d(f'File \'{file}\' done.')
