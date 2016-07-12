# -*- coding: utf-8 -*-
"""
Created on Tue Dec  9 11:06:41 2014
@author: abashash
This script reads a bunch of titan results files and create a file containg 
case-gene-mutation type. The resulting file will be used to create 
case-gene plot
"""

#!/usr/bin/env python
import glob
import argparse
import warnings
from collections import defaultdict

class CaseGeneTitanParser(object):
    def __init__(self, args):
        self.args = args
        
        if self.args.paramsfile and not self.args.infile:
            argparse.ArgumentTypeError('Paramsfile is only required when infile is provided.')
        
        if self.args.infile:
            self.infiles = self.args.infile
            self.paramfiles = self.args.paramsfile
        else:
            self.infiles = glob.glob(self.args.input_dir+'/*.pygenes') #find the vcf files in inDir
            self.infiles.extend(glob.glob(self.args.input_dir+'/*segs.txt'))
            self.paramfiles = glob.glob(self.args.input_dir+'/*params.txt')

        self.outfile = open(self.args.result, 'wb')

        self.label_map = self.__get_label_mapping()

        #adding label_ prefix to labels -> will help downstream to identify if a field is label
        self.labels = list(set([label for case in self.label_map.keys() for label in self.label_map[case].keys()]))
        #header for the new output format
        out_string = ['case_id', 'ref_sample', 'tum_sample', 'chromosome', 'start',
                      'stop', 'gene', 'gene_id', 'type', 'caller', 'median_logR', 'total_copy_number',
                      'minor_cn', 'major_cn', 'clonal_cluster', 'titan_state', 'clonal_frequency',
                      'ploidy', 'project'] + self.labels
        out_string = '\t'.join(out_string) + '\n'
                
        self.outfile.write(out_string)
        
        self.optimal_clusters = None
        if self.args.optimal_clusters:
            self.optimal_clusters = self.get_clusters()
            
    def get_clusters(self):
        cluster_map = defaultdict(str)
        for lval in self.args.optimal_clusters.split(','):
            lval=lval.split(':')
            case = lval[0]
            cluster = lval[1]
            cluster_map[case] = cluster
        return cluster_map

    def __get_label_mapping(self, prefix='label_'):
        if not self.args.label_mapping:
            return {}
        data = defaultdict(lambda: defaultdict(str))
        label_map = open(self.args.label_mapping)
        for line in label_map:
            line = line.strip().split()
            if line[0] == 'case_id':
                labels = [prefix+val for val in line[1:]]
                continue
            case = line[0]
            for i,label in enumerate(labels):
                data[case][label] = line[i+1]
        return data

    def __cleanup(self):
        self.outfile.close()

    def __find_gene_pygene(self, pygene_line): 
        '''
        extracts gene symbols from pygenes annotated column
        'ENSG00000223315,RN7SKP279;ENSG00000222774,RN7SKP121;ENSG00000221516,AP002806.1;'
        '''
        genes = []
        pygene_line = pygene_line.split(';')
        
        pygene_line = [val for val in pygene_line if not val == '']

        for gene in pygene_line:
            gene_id = gene.split(',')[0]
            gene_name = gene.split(',')[1]
            genes.append((gene_id,gene_name))
        return genes
    
    def __check_header(self, line):
        error_string = 'The input file doesn\'t match the expected input.'
        line = line.strip().split()
        assert line[0] == 'Sample', error_string
        assert line[1] == 'Chromosome', error_string
        assert line[2] == 'Start_Position(bp)', error_string
        assert line[3] == 'End_Position(bp)', error_string
        assert line[4] == 'Length(bp)', error_string
        assert line[5] == 'Median_Ratio', error_string
        assert line[6] == 'Median_logR', error_string
        assert line[7] == 'TITAN_state', error_string
        assert line[8] == 'TITAN_call', error_string
        assert line[9] == 'Copy_Number', error_string
        assert line[10] == 'MinorCN', error_string
        assert line[11] == 'MajorCN', error_string
        assert line[12] == 'Clonal_Cluster', error_string
        assert line[13] == 'Clonal_Frequency', error_string
        assert line[14] == 'Pygenes(gene_id,gene_name;)', error_string
        
    def __get_norm_sample(self, case, fname):
        #remove alphabets from end and add N
        for i,val in enumerate(case[::-1]):
            try:
                int(val)
                break
            except:
                pass
        
        if i==0:
            ref_samp = case+'N'
        else:       
            ref_samp = case[:-i]+'N'
        
        #the demix oufiles are named: {normal}_stats.tsv
        assert ref_samp in fname

        return ref_samp
            
    def __parse_line(self,line):
        line = line.strip().split('\t')

        case = line[0]

        chrom = line[1]
        start = line[2]
        stop = line[3]
        median_ratio = line[5]
        median_logr = line[6]
        titan_state = line[7]
        titan_call = line[8]
        copy_number = line[9]
        minor_cn = line[10]
        major_cn = line[11]
        clonal_cluster = line[12]
        clonal_freq = line[13]
        
        try:
            genes = self.__find_gene_pygene(line[14])
        except IndexError:
            #use N/A when no annotation
            genes = [('N/A', 'N/A')]
            
        caller = 'titan'

        info = [case, chrom, start, stop, median_ratio, median_logr, titan_state,
                titan_call, copy_number, minor_cn, major_cn, clonal_cluster, clonal_freq,
                genes, caller]


        
        return info
    
    def __write(self, info, tum_samp, ref_samp, ploidy):
        if not self.args.project:
            proj = 'N/A'
        else:
            proj=self.args.project

        for gene in info[13]:
            if self.__filter(info, gene[1]):
                continue

            out_string = [tum_samp, tum_samp, ref_samp, info[1], info[2],
                          info[3], gene[1], gene[0], info[7], info[14],
                          info[5], info[8], info[9], info[10], info[11],
                          info[6], info[12], ploidy, proj]
            labels = [self.label_map[tum_samp][label] for label in self.labels]
            out_string = out_string + labels
            
            out_string = '\t'.join(out_string) + '\n'
            
            self.outfile.write(out_string)
            if self.args.remove_duplicates:
                break

    def __filter(self, info, gene):
        if self.args.genes and gene not in self.args.genes:
            return True

        state = info[6]
        if self.args.states and state not in self.args.states:
            return True

        size = int(info[3]) - int(info[2])
        if size < self.args.segment_size_threshold:
            return True
        return False
    
    def __get_ploidy(self, tum_samp, ref_samp, case, cluster):
        for filename in self.paramfiles:
            if case in filename:
                filename = open(filename)
                for line in filename:
                    line = line.strip().split(':')
                    if line[0] == 'Average tumour ploidy estimate':
                        ploidy = line[1]
                    elif 'Clonal cluster cellular prevalence' in line[0]:
                        cluster = len(line[1].split())

                if not self.optimal_clusters:
                    return ploidy

                if self.optimal_clusters[case] and self.optimal_clusters[case] == str(cluster):
                    return ploidy
                    
        raise Exception('Could not find a matching params file for the sample %s' %tum_samp)

    def __read_infile(self, fname):
        fname_reader = open(fname)
        
        num_clusters = set()
        
        data = []
        
        for line in fname_reader:
            if line[0] == '#':
                continue
            else:
                if line.split()[0] == 'Sample':
                    self.__check_header(line)
                    continue
        
                info = self.__parse_line(line)
                
                num_clusters.add(info[11])
                data.append(info)
        
        return data, len(num_clusters)
                
        
                    
    def main(self):
        for fname in self.infiles:  #loop though different files
            data, num_clusters = self.__read_file(fname)
            case = data[0][0]

            if num_clusters != self.optimal_clusters[case]:
                continue
            
            ploidy = self.__get_ploidy(case, num_clusters)
            
            for info in data:
                self.__write(info, case, ploidy)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''This script reads a bunch of titan results files and create a file containg 
                                                    case-gene-mutation type. The resulting file will be used to create 
                                                    case-gene plot''')

    parser.add_argument("-v", "--verbose", action="store_true")
    exgroup = parser.add_mutually_exclusive_group(required = True)
    exgroup.add_argument("--input_dir",
                         default = None,
                         help="Input directory")

    exgroup.add_argument("--infile",
                         nargs = '*',
                         default = None,
                         help="Input files")
    
    
    parser.add_argument("--paramsfile",
                         nargs = '*',
                         default = None,
                         help="params files for the infiles (only required when params file is specified)")    

    parser.add_argument("--label_mapping",
                         default = None,
                         help="File with labels for each case")    

    parser.add_argument("--genes",
                        nargs = '*',
                        help = ''' filters out all the genes except
                        the ones specified here (default : no filtering) 
                        ''')

    parser.add_argument("--segment_size_threshold",
                        default = 5000,
                        type = int,
                        help = ''' filters out all the segments that are smaller
                        than the threshold(default : 5000 bases)
                        ''')

    parser.add_argument("--states",
                       help = ''' filters out all the stats except 
                       the ones specified here (default : no filtering)
                       ''')

    parser.add_argument("--result", help="Resulting file name")

    parser.add_argument("--project",
                        help="The project name for the input files")
    
    parser.add_argument("--remove_duplicates",
                        default = False,
                        action='store_true',
                        help=''' Each call will result in multiple lines in output, one for each gene
                                default: only the first gene will be printed ''')
    
    parser.add_argument("--optimal_clusters",
                        default = None,
                        help = '''optimal clusters for each case. Format: case1:label,case2:label ...,
                                if provided, only optimal clusters will be parsed.''')

    args = parser.parse_args()
    
    titanparser = CaseGeneTitanParser(args)
    titanparser.main()

