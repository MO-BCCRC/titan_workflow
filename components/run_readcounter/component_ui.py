'''
the user interface for the titan_runner component 
Created on May 12, 2014

@author: dgrewal
'''

import argparse

__version__ = 'read_counter_v0.1'

##Make a UI

parser = argparse.ArgumentParser(prog='''ReadCounter''',
                                 description = '''Generate counts for the reads  and then 
                                 filter to generate the wig file ''')

parser.add_argument("--bam", 
                    required = True, 
                    help= '''specify the path to the input bam file ''')

parser.add_argument("-w", 
                    default = '1000', 
                    type = str,
                    help="")


parser.add_argument("-q", 
                    default = '0',  
                    type = str,
                    help="")

parser.add_argument("--out", 
                    type = str,
                    required = True,  
                    help="specify the path where the output wig file will be saved")

args = parser.parse_args()
