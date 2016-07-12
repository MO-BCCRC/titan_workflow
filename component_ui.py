'''
the user interface for the titan_runner component 
Created on May 12, 2014

@author: dgrewal
'''

import argparse

__version__ = 'titan_runner_v0.1'

##Make a UI

parser = argparse.ArgumentParser(prog='''TITAN''',
                                 description = '''Run TITAN ''')

parser.add_argument("--id", 
                    required = True, 
                    help= '''sample id ''')

parser.add_argument("--infile", 
                    required = True, 
                    help="input file with list of all sites")

parser.add_argument("--outfile", 
                    required = True,  
                    help="specify the path where the segment file will be saved")

parser.add_argument("--outigv", 
                    required = True,  
                    help="specify the path where the IGV compatible segment file will be saved")

args,unknown = parser.parse_known_args()
