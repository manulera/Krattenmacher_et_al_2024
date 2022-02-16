#!/usr/bin/env bash

python ./scan.py 'python ../../../../analyse_results.py' jobs=12 $1/scan/run*
python ./scan.py '/usr/bin/head -n1 parameters_table.txt >../../parameters_table.txt' $1/scan/run0000
python ./scan.py '/usr/bin/tail -n1 parameters_table.txt >>../../parameters_table.txt' $1/scan/run*

python ./scan.py '/usr/bin/head -n1 other_values.txt >../../other_values.txt' $1/scan/run0000
python ./scan.py '/usr/bin/tail -n1 other_values.txt >>../../other_values.txt' $1/scan/run*