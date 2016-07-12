#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on Aug 25, 2015

@author: dgrewal
'''

import argparse
from collections import defaultdict
import warnings

from intervaltree import IntervalTree
import pandas


def build_indices(line):
    '''
    converts the line to dict
    with value as key and index as val
    '''

    if isinstance(line, str):
        line = line.strip().split()

    return dict([(val, i) for (i, val) in enumerate(line)])


class ParseUtils(object):
    '''
    helper functions for the parsers
    in the bigdata pipeline.
    '''

    def __init__(self):

        # default chr_lengths from hg19 chromosome (build: GRCh37 released
        # February 27, 2009) please see
        # www.ncbi.nlm.nih.gov/projects/genome/assembly/grc/human/data/index.shtml

        self.chr_lengths = {
            '1': 249250621,
            '2': 243199373,
            '3': 198022430,
            '4': 191154276,
            '5': 180915260,
            '6': 171115067,
            '7': 159138663,
            '8': 146364022,
            '9': 141213431,
            '10': 135534747,
            '11': 135006516,
            '12': 133851895,
            '13': 115169878,
            '14': 107349540,
            '15': 102531392,
            '16': 90354753,
            '17': 81195210,
            '18': 78077248,
            '19': 59128983,
            '20': 63025520,
            '21': 48129895,
            '22': 51304566,
            'X': 155270560,
            'Y': 59373566,
        }

    @staticmethod
    def get_genome_length(build='grch37_hg19'):
        '''
        return the length of genome (inbp)
        for the build provided
        '''
        if build == 'grch37_hg19':

            # based on chr_lengths from hg19 chromosome (build: GRCh37 released
            # February 27, 2009) please see
            # www.ncbi.nlm.nih.gov/projects/genome/assembly/grc/human/data/index.shtml

            genome_length = 3095677412
        else:

            raise Exception('Genome length for build %s not available'
                            % build)

        return genome_length

    @staticmethod
    def close_file(ofile):
        '''
        close file object
        '''
        ofile.close()

    @staticmethod
    def test_args(args):
        '''
        if using the all_files option, then we dont need params, tid and nid as
        it is included in file
        '''

        if not args.infile:
            if hasattr(args, 'params_file') and args.paramsfile:
                argparse.ArgumentTypeError('Paramsfile is only required'
                                           ' when infile is provided.')

            if args.tumour_id:
                argparse.ArgumentTypeError('tumour_id is only required'
                                           ' when infile is provided.')

            if args.normal_id:
                argparse.ArgumentTypeError('normal_id is only required'
                                           ' when infile is provided.')

        if args.infile:
            if hasattr(args, 'params_file') and not args.paramsfile:
                argparse.ArgumentTypeError('Paramsfile is required'
                                           ' when infile is provided.')
            if args.tumour_id:
                argparse.ArgumentTypeError('tumour_id is required'
                                           ' when infile is provided.')
            if args.normal_id:
                argparse.ArgumentTypeError('normal_id is required'
                                           ' when infile is provided.')

    # pylint: disable=too-many-arguments
    @staticmethod
    def get_inputs(tid, nid, infile, all_files, paramsfile=None,
                   fh_names=None):
        '''
        load the all_files if provided, o.w. use the infile and
        paramsfile params
        '''
        if not fh_names:
            fh_names = ['params', 'segments']

        output = defaultdict()
        if infile:
            val = (infile, paramsfile) if paramsfile else infile
            output[(tid, nid)] = val
        else:
            freader = open(all_files)

            header = freader.readline()
            header = build_indices(header)
            k_idx = [header['tumour_id'],
                     header['normal_id']
                     ]

            if isinstance(fh_names, str):
                v_idx = header[fh_names]
            else:
                v_idx = [header[val] for val in fh_names]

            for line in freader:
                # ignore comments
                if line[0] == '#':
                    continue
                line = line.strip().split()
                key = tuple(line[val] for val in k_idx)

                if isinstance(v_idx, list):
                    val = tuple(line[val] for val in v_idx)
                else:
                    val = line[v_idx]

                output[key] = val
        return output

    @staticmethod
    def get_label_mapping(lmap_file, prefix='label_'):
        '''
        adding label_ prefix to labels -> will help downstream to identify
        if a field is label
        '''

        if not lmap_file:
            return {}, []

        data = defaultdict(lambda: defaultdict(str))
        label_map = open(lmap_file)

        for line in label_map:
            line = line.strip().split()
            if line[0] == 'case_id':
                labels = [prefix + val for val in line[1:]]
                continue

            case = line[0]

            for (i, label) in enumerate(labels):
                if line[i + 1].lower() == 'true':
                    data[case][label] = label.replace('label_', '')
                elif line[i + 1].lower() == 'false':
                    data[case][label] = '-'
                else:
                    raise Exception('Invalid Value: The labels'
                                    ' should only be TRUE/FALSE')

        labels = list(set([label for case in data.keys() for label in
                           data[case].keys()]))

        return (data, labels)

    @staticmethod
    def parse_pygene(pygene_line):
        '''
        extracts gene symbols from pygenes annotated column
        'ENSG00000223315,RN7SKP279;ENSG00000222774,RN7SKP121;ENSG00000221516,AP002806.1;'
        '''

        genes = []
        pygene_line = pygene_line.split(';')

        pygene_line = [val for val in pygene_line if not val == '']

        if not pygene_line:

            # use N/A when no annotation

            return [('N/A', 'N/A')]

        for gene in pygene_line:
            gene_id = gene.split(',')[0]
            gene_name = gene.split(',')[1]
            genes.append((gene_id, gene_name))

        return genes

    @staticmethod
    def build_interval_ref(centrofile):
        '''
        check if position falls in region in the file
        filename is the path to file with all centromeres
        '''

        if not centrofile:
            return

        centrotree = defaultdict(IntervalTree)

        ref_reader = open(centrofile)

        # assuming first line is header

        header = ref_reader.readline()
        idxs = build_indices(header)
        chr_idx = idxs['chromosome']
        beg_idx = idxs['start']
        end_idx = idxs['end']

        for line in ref_reader:
            line = line.strip().split()
            chrom = line[chr_idx]
            start = int(line[beg_idx])
            end = int(line[end_idx])

            if end - start < 1:
                warnings.warn('Encountered empty interval in %s, line: %s'
                              % (centrofile, line))
            end = end + 1

            centrotree[chrom].addi(start, end)

        return centrotree

    @staticmethod
    def is_present_intervaltree(centrotree, info):
        '''
        check if provided position falls in the
        centromere regions. requires an intervaltree
        with all centromeres
        '''
        chrom = info[1]
        start = int(info[2])
        end = int(info[3])

        olp = (centrotree[chrom])[start:end]

        if len(olp) != 0:
            return True

    @staticmethod
    def read_file_to_list(fname):
        '''
        simplistic file parser, reads file into list,
        removes line breaks
        '''

        if not fname:
            return

        data = [val.strip() for val in open(fname).readlines()]
        return data

    @staticmethod
    def build_indices(line, colnames=None):
        '''
        converts the line to dict
        with value as key and index as val
        get the indices for the provided cols
        '''

        if isinstance(line, str):
            line = line.strip().split()

        indices = dict([(val, i) for (i, val) in enumerate(line)])

        if colnames:
            col_indices = [indices[val] for val in colnames]

            return col_indices

        return indices

    @staticmethod
    def get_labels(label_map, labels, case_id):
        '''
        get the labels from the label_dict loaded from labels file
        '''
        labels = [label_map[case_id][label] for label in labels]

        if '' in labels:
            raise Exception('Incorrect labels for %s. labels were: %s'
                            % (case_id, labels))

        return labels

    @staticmethod
    def open_outfile(fpath, labs, cols):
        '''
        open infile for writing,
        writes header
        '''

        outfile = open(fpath, 'w')

        # header for the new output format
        out_string = cols + labs

        out_string = '\t'.join(out_string) + '\n'
        outfile.write(out_string)

        return outfile

    @staticmethod
    def write_list(ofile, vals, labs=None, sep='\t'):
        '''
        write the list to file (join by sep)
        '''
        if labs:
            vals = vals + labs

        vals = [str(val) for val in vals]
        outstr = sep.join(vals) + '\n'
        ofile.write(outstr)

    @staticmethod
    def get_annotations(info):
        '''
        extract dbsnp, 1000gen
        and cosmic anns
        '''
        dbsnp = 'N/A'
        th_gen = 'N/A'
        cosmic = 'N/A'

        for val in info:
            if 'DBSNP' in val:
                dbsnp = val.split('=')[1]
            elif '1000Gen' in val:
                th_gen = val.split('=')[1]
            elif 'Cosmic' in val:
                cosmic = val.split('=')[1]

        return dbsnp, th_gen, cosmic

    @staticmethod
    def parse_snpeff(info):
        '''
        extract snpeff annotations from info section
        '''
        output = []

        if isinstance(info, str):
            info = info.split(';')

        snpeff_ann = [val for val in info if val.split('=')[0] == 'EFF'][0]
        snpeff_ann = snpeff_ann.split('=')[1].split(',')
        for eff in snpeff_ann:
            keyword = eff.split('(')[0]
            eff = eff.split('(')[1].split(')')[0].split('|')
            gene_name = eff[5]
            gene_id = eff[8]
            imp = eff[0]
            amino = eff[3]
            func_change = eff[1]
            gene_coding = eff[7]

            outval = (keyword, gene_name, gene_id, imp,
                      amino, func_change, gene_coding)

            outval = tuple(val if val else 'N/A' for val in outval)

            output.append(outval)
        return output

    @staticmethod
    def sort_snpeff(snpeff_ann):
        '''
        sort snpeff annotations by their modifier
        '''
        high = []
        mod = []
        low = []
        oth = []

        for val in snpeff_ann:
            if val[3] == 'HIGH':
                high.append(val)
            elif val[3] == 'MODERATE':
                mod.append(val)
            elif val[3] == 'LOW':
                low.append(val)
            else:
                oth.append(val)

        return high + mod + low + oth

    @staticmethod
    def find_overlaps(indata_df, chrom, start, end):
        """
        query df for the segment chr:start-end.
        """
        expr = 'start >= {0} and end <={1} and chromosome == "{2}"'
        expr = expr.format(start, end, chrom)
        return indata_df.query(expr)

    @staticmethod
    def load_tsv_to_df(fname, dtypes=None):
        '''
        load a tsv into a pandas dataframe
        '''
        data = pandas.read_csv(fname,
                               sep='\t',
                               dtype=dtypes,
                               )

        return data

    @staticmethod
    def has_overlaps_bkp(indata_df, pos):
        """
        query df for the segment chr:start-end.
        """

        chrom_1, start_1, end_1, chrom_2, start_2, end_2 = pos

        expr_1 = 'start >= {0} and end <={1} and chromosome == "{2}"'
        expr_1 = expr_1.format(start_1, end_1, chrom_1)

        expr_2 = 'start >= {0} and end <={1} and chromosome == "{2}"'
        expr_2 = expr_2.format(start_2, end_2, chrom_2)

        #if results of both queries are empty -> no overlap
        if indata_df.query(expr_1).empty and indata_df.query(expr_2).empty:
            return False

        return True

