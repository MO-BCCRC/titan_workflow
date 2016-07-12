'''
Created on May 21, 2015

@author: dgrewal
'''

import argparse
import glob
from collections import defaultdict
import warnings

version='1.0.1'

class OptimalClustersTitan(object):
    def __init__(self, args):
        self.args = args

        self.infiles = glob.glob(self.args.input_dir+'/*params.txt')

    def __enter__(self):
        return self

    def __exit__(self,typ, value, traceback):
        pass

    def __split_infiles_by_case(self):
        '''
        assuming there is a normal sample with N in name
        '''
        out = defaultdict(list)

        def get_case(filename):
            filename = filename.split('_')
            for val in filename:
                if 'N' in val:
                    return val.replace('N','')
            raise Exception('couldn\'t get the case for %s' %fname)

        for fname in self.infiles:
            if not self.args.sample_id:
                case = get_case(fname)
            else:
                if self.args.sample_id not in fname:
                    warnings.warn('The file %s doesn\'t match the sample, skipping file' %fname )
                    continue
                case = self.args.sample_id

            out[case].append(fname)

        return out

    def __get_clusters(self, case_dict):

        cluster_out = defaultdict(lambda: defaultdict(float))
        for case, files in case_dict.iteritems():
            for fname in files:
                fname_reader = open(fname)
                for line in fname_reader:
                    line = line.strip().split(':')
                    if 'Clonal cluster cellular prevalence' in line[0].strip():
                        num_clus = len(line[1].split())
                    if 'Average tumour ploidy estimate' in line[0].strip():
                        ploidy = line[1].strip()

                    elif line[0].strip() == 'S_Dbw validity index (Both)':
                        if line[1].strip() == 'NaN':
                            warnings.warn('the validity index for %s is Nan.' %fname)
                            idx  = line[1].strip()
                        else:
                            idx = eval(line[1])
                if not all((num_clus, idx)):
                    raise Exception('couldn\'t retrieve the num_clusters and validity_index from the params file' )
                cluster_out[case][(num_clus,ploidy)] = idx
                fname_reader.close()

        return cluster_out

    def __write(self, opt_clus):
        outfile = open(self.args.output, 'w')
        for case, clus_dict in opt_clus.iteritems():
            for key, idx in clus_dict.iteritems():
                num_clus, ploidy = key
                outfile.write(' '.join(map(str,['case:', case, 'num_clusters:', num_clus, 'Ploidy:', ploidy, 'DBW validity index:', idx]))+'\n')
            
            optimal = min([val for val in clus_dict.itervalues() if val != 'NaN'])
            optclus = [val[0] for val in clus_dict.iteritems() if val[1]==optimal]
            
            outfile.write('\n')
            outfile.write('optimal Clusters: '+ ' '.join(map(str,optclus))+'\n' )
            outfile.write('optimal DBW index: %s \n' %optimal )
            
            outfile.write('*'*80+'\n\n')
            
        outfile.close()
    def main(self):
        files_by_case = self.__split_infiles_by_case()

        optclus = self.__get_clusters(files_by_case)

        self.__write(optclus)



if __name__ == '__main__':
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

    with OptimalClustersTitan(args) as optclustitan:
        optclustitan.main()
