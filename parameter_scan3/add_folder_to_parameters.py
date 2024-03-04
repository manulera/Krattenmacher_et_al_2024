import pandas
import sys
import glob
import os


if __name__ == '__main__':
    if len(sys.argv) == 2:
        folder = sys.argv[1]
        # Find names of run folders
        run_folders = sorted(glob.glob(f'{folder}/scan/run*'))
        # Add them as extra column
        data = pandas.read_csv(f'{folder}/parameters_table.txt')
        data['run_folder'] = run_folders
        # Save the new table
        data.to_csv(f'{folder}/parameters_table.txt', index=False)

    else:
        print('No folder name given')

