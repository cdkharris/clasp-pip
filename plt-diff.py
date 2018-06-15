"""This is for diffing alllllll the vars in two plt files.
Call it like:
    plt-diff.py path/to/plt/1 path/to/plt/2

Camilla Harris, June 2018
"""

import numpy as np
import tecplot
import sys

## load the zone we're starting with and the zone we're comparing
batsrus = tecplot.data.load_tecplot([sys.argv[1],sys.argv[2]])

print(sys.argv[0].split('/')[-1],': loaded!')

print(sys.argv[0].split('/')[-1],': Dataset has the following variables')

print([v.name for v in batsrus.variables()])

print(sys.argv[0].split('/')[-1],': Diffing variables!')

## make a dict where each key is a variable and each value is a bool about whether there's any difference
vars = {v.name: max(abs(np.array(v.values(0)[:]) - np.array(v.values(1)[:]))) != 0 for v in batsrus.variables()}

for k in vars:
    print('{}\t : {}'.format(k, vars[k]))
