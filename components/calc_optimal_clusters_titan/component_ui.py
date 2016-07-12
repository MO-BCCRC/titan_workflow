'''
Created on Apr 1 2015

@author: dgrewal
'''

import argparse

__version__ = '1.0.0'


#==============================================================================
# make a UI
#==============================================================================
parser = argparse.ArgumentParser()

parser.add_argument('--input_dir',
		'-i',
		 required = True,
		 help = ''' The output directory
		 ''')

parser.add_argument('--output',
		'-o',
		 required = True,
		 help = ''' The output directory
		 ''')
parser.add_argument('--sample_id',
		help = '''if the sample is provided, the script will
		       pick files that correspond to the sample''')

args = parser.parse_args()
