# -*- coding: utf-8 -*-
"""
Last Updated: Jun 3 2015

@author dgrewal

reads titan seg files, filters and writes the output in tsv format
"""


import argparse

parser = argparse.ArgumentParser(description='''reads titan seg files,\
                                                filters and writes the \
                                                output in tsv format''')

exgroup = parser.add_mutually_exclusive_group(required=True)
exgroup.add_argument("--all_files",
                     default=None,
                     help="Input directory")

exgroup.add_argument("--infile",
                     default=None,
                     help="Input files")

parser.add_argument("--paramsfile",
                    nargs='*',
                    default=None,
                    help="params files for the infiles\
                    (only required when params file is specified)")

parser.add_argument("--tumour_id",
                    help='''tumour id for the infile
                        (only required when infile is specified)''')

parser.add_argument("--normal_id",
                    help='''normal id for the infile
                        (only required when infile is specified)''')

parser.add_argument("--label_mapping",
                    default=None,
                    help="File with labels for each case")

parser.add_argument("--genes",
                    help=''' filters out all the genes except
                    the ones specified here (default : no filtering)
                    ''')

parser.add_argument("--segment_size_threshold",
                    default=5000,
                    type=int,
                    help=''' filters out all the segments that are smaller
                    than the threshold(default : 5000 bases)
                    ''')

parser.add_argument("--types",
                    nargs='*',
                    help=''' filters out all the states except
                       the ones specified here (default : no filtering)
                       ''')

parser.add_argument("--result", help="Resulting file name")

parser.add_argument("--project",
                    default='project',
                    help="The project name for the input files")

parser.add_argument("--chromosomes",
                    default=None,
                    nargs='*',
                    help=''' all chromosomes except the ones provided will be
                    filtered (default: no filtering)
                    ''')

args = parser.parse_args()
