'''
Created on Jun 26, 2014

@author: jtaghiyar
'''

import argparse

#==============================================================================
# make a UI 
#==============================================================================
parser = argparse.ArgumentParser(description='''Merge component, remove header and merge vcf files''')
parser.add_argument("infiles", 
                    metavar='FILE', nargs='*', 
                    default=None, 
                    #type=argparse.FileType('r'), 
                    help= '''A list vcf file names''')

parser.add_argument("-o", "--out", 
                    default=None, required=True, 
                    help='''name of the output file''')

parser.add_argument("-e", "--extension",
                    default='.vcf',
                    help='''specify the extension of files to be merged''')

parser.add_argument("--samtools",
                    default=None, 
                    help='''specify the path to samtools''')

args, unknown = parser.parse_known_args()