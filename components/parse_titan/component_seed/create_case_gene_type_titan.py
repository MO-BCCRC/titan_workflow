# -*- coding: utf-8 -*-
"""
Last Updated: Jun 3 2015

@author dgrewal

reads titan seg files, filters and writes the output in tsv format
"""

#!/usr/bin/env python
import argparse
from parseutils import ParseUtils as pau

class ParseTitan(object):
    '''
    parse, filter and print titan files to tsv format
    '''

    def __init__(self, args):
        self.args = args

        pau.test_args(self.args)

        self.infiles = pau.get_inputs(self.args.tumour_id,
                                      self.args.normal_id,
                                      self.args.infile,
                                      self.args.all_files,
                                      paramsfile=self.args.paramsfile)

        self.lab_map, self.labs = pau.get_label_mapping(
            self.args.label_mapping)

        self.genome_length = pau.get_genome_length()

        self.genes = pau.read_file_to_list(self.args.genes)

    @staticmethod
    def get_colnames():
        '''
        get output header names
        '''
        vals = ['case_id', 'normal_id', 'tumour_id', 'chromosome', 'start',
                'stop', 'gene', 'gene_id', 'type', 'caller', 'median_logR',
                'total_copy_number', 'minor_cn', 'major_cn', 'clonal_cluster',
                'titan_state', 'clonal_frequency', 'ploidy', 'project'
               ]

        return vals

    @staticmethod
    def parse_file(fname):
        '''
        parse the titan segs file
        '''
        colnames = ['Sample', 'Chromosome', 'Start_Position(bp)',
                    'End_Position(bp)', 'Median_Ratio', 'Median_logR',
                    'TITAN_state', 'TITAN_call', 'Copy_Number', 'MinorCN',
                    'MajorCN', 'Clonal_Cluster', 'Clonal_Frequency',
                    'Pygenes(gene_id,gene_name;)'
                   ]

        freader = open(fname)
        header = freader.readline()
        header_idx = pau.build_indices(header, colnames)

        for line in freader:
            line = line.strip('\n').split('\t')

            info = [line[val] for val in header_idx]

            info[13] = pau.parse_pygene(info[13])

            info.append('titan')

            yield info

        freader.close()

    def filter(self, infos):
        '''
        filter unnecessary calls
        '''
        for info in infos:
            genes = info[13]

            if self.genes:
                genes = [val for val in genes if val[1] in self.genes]

            if self.args.types and info[6] not in self.args.types:
                continue

            size = int(info[3]) - int(info[2])
            if size < self.args.segment_size_threshold:
                continue

            if self.args.chromosomes and info[1] not in self.args.chromosomes:
                continue

            # update genes in info and return info
            for gene in genes:
                info[13] = gene
                yield info

    # pylint: disable=too-many-arguments
    def write(self, outfile, infos, ploidy, tum, norm):
        '''
        write to outfile in tsv format
        '''
        for info in infos:
            case = norm if norm not in ['N/A', 'NA'] else tum
            labs = pau.get_labels(self.lab_map, self.labs, case)

            gene = info[13]
            vals = [case, norm, tum, info[1], info[2],
                    info[3], gene[1], gene[0], info[7], info[14],
                    info[5], info[8], info[9], info[10], info[11],
                    info[6], info[12], ploidy, self.args.project]

            pau.write_list(outfile, vals, labs)

    @staticmethod
    def get_ploidy(paramfile):
        '''
        get ploidy value from the params file
        '''
        filename = open(paramfile)
        for line in filename:
            line = line.strip().split(':')
            if line[0] == 'Average tumour ploidy estimate':
                ploidy = line[1]

        ploidy = ploidy.strip()
        return ploidy

    def main(self):
        '''
        loop through all files, load,
        filter and write to tsv outfile
        '''
        cols = self.get_colnames()
        outfile = pau.open_outfile(self.args.result, self.labs, cols)

        for (tid, nid), (fname, paramfile) in self.infiles.iteritems():

            ploidy = self.get_ploidy(paramfile)

            infos = self.parse_file(fname)

            infos = self.filter(infos)

            self.write(outfile, infos, ploidy, tid, nid)

        pau.close_file(outfile)

def parse_args():
    '''
    specify and parse args
    '''
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
                        filtered (default:no filtering)
                        ''')

    args = parser.parse_args()

    return args


if __name__ == '__main__':
    ARGS = parse_args()

    PARSE_TITAN = ParseTitan(ARGS)
    PARSE_TITAN.main()
