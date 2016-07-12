'''
the user interface for the titan_runner component 
Created on May 12, 2014

@author: dgrewal
'''

import argparse
#============================
##Make a UI
#============================
parser = argparse.ArgumentParser(prog='''Correct Reads''',
                                 description = '''Plot TITAN results''')

parser.add_argument("--id", 
                    required = True, 
                    help= '''the sample id ''')

parser.add_argument("--tumwig", 
                    required = True, 
                    help="The path to Wig file for the tumour")

parser.add_argument("--normwig", 
                    required = True,  
                    help="The path to Wig file for the normal")

parser.add_argument("--gc", 
                    required = True,  
                    help=" path to the gc content wig file ")

parser.add_argument("--map", 
                    required = True,  
                    help=" path to the map wig files")

parser.add_argument("--outfile",
                    required = True,
                    help='''specify the path where the output file will be saved.''')

args,unknown = parser.parse_known_args()
