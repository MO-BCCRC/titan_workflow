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
                    help= '''the sample id ''')

parser.add_argument("--infile", 
                    required = True, 
                    help="input file with list of all sites")

parser.add_argument("--cnfile", 
                    required = True,  
                    help="Wig file for tumour sample ")

parser.add_argument("--map", 
                    required = True, 
                    help="specify the path to map wig file")

parser.add_argument("--num_clusters", 
                    default='1', 
                    help="number of clonal clusters")

parser.add_argument("--num_cores", 
                    default='4', 
                    help="Specify the Number of cores to be used")

parser.add_argument("--ploidy", 
                    default = '2',
                    help="specify the ploidy value")

parser.add_argument("--outfile", 
                    required = True,
                    help="the path to the output file")

parser.add_argument("--obj_outfile", 
                    required = True,
                    help="the path to the output file")

parser.add_argument("--outparam", 
                    required = True,  
                    help="path to file with all the required parameters ")

parser.add_argument("--myskew", 
                    default = '0',  
                    help=" skew parameter for titan")

parser.add_argument("--bool_est_ploidy", 
                    default = 'TRUE',  
                    help="logical indicating whether to estimate and account for tumour ploidy ")

parser.add_argument("--n_zero", 
                    required = True,  
                    help=" n_zero ")

parser.add_argument("--norm_est_meth", 
                    default = 'map',  
                    help='''specifies how to handle normal proportion estimation. To estimate,
                         use map which is maximum a posteriori. If you wish to not estimate
                         this parameter, then use fixed ''')

parser.add_argument("--max_i", 
                    default = '5', 
                    help="maximum number of EM iterations allowed ")

parser.add_argument("--pseudo_counts", 
                    default = '1e-300', 
                    help=" the pseudo counts used for EM")

parser.add_argument("--txn_exp_len", 
                    default = '1e9', 
                    help=''' influences prior probability of genotype transitions in
                     the HMM. The smaller, the lower tendency to change state;
                      however, too small and it produces underflow problems ''')

parser.add_argument("--txn_z_strength", 
                    default = '1e9', 
                    help='''influences prior probability of clonal cluster transitions
                         in the HMM. Smaller values means lower tendency to change
                         clonal cluster state''')

parser.add_argument("--alpha_k", 
                    default='2500', 
                    help="alpha_k")

parser.add_argument("--alpha_high", 
                    default='20000',  
                    help="alpha_high")

parser.add_argument("--maxcn",
                    default = '8',
                    help = "maxcn")

parser.add_argument("--sym",
                    default = 'TRUE',
                    help = 'sym')

args, unknown = parser.parse_known_args()
