'''
Created on Jul 2, 2014

@author: dgrewal
'''

import argparse

chrom_list = map(str, range(1, 23)) + ['X', 'Y']

parser = argparse.ArgumentParser()

parser.add_argument('-i', '--infile',
                    required=True, 
                    help='path to input file ... the output of Titan')

parser.add_argument('-o', '--outfile',
                    required=True,
                    help='output file name')

exgroup = parser.add_mutually_exclusive_group(required=True)

exgroup.add_argument('-b', '--gene_sets_gtf_bin', 
                    help='Gene sets in GTF binary format')

exgroup.add_argument('-r', '--gene_sets_gtf',
                    help='Gene sets in GTF format')


parser.add_argument('-s','--save_gtf_as_bin',
                    action = 'store_true',
                    help = "save '-r' file to pygenes friendly binary format")

parser.add_argument('-c','--is_contained',
                    dest='is_contained',
                    action = 'store_true',
                    help = 'add flag to return output that is contained 100 percent within region \
                    (else will include genes overlapping segment ends)')

args,unknown = parser.parse_known_args()
