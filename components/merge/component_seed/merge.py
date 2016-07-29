'''
Created on Jun 26, 2014

@author: jtaghiyar, jrosner
'''
from __future__ import division
import os
import subprocess

def __merge_vcf(infiles, outfile):
    '''
    merges a list of vcf files into a single vcf
    '''
    with open(outfile, 'w') as ofile:
        is_first_run = True

        for ifile in infiles:
            with open(ifile) as f:
                print f.name

                lines = f.readlines()
                for l in lines:
                    if l.startswith('#'):
                        if is_first_run:
                            print >> ofile, l,

                        continue

                    else:
                        is_first_run = False
                        print >> ofile, l,



def __merge_bam(infiles, outfile):
    '''
    merges a list of bam files into a single bam
    '''
    inputs = ' '.join(infiles)

    cmd = ' '.join ([args.samtools, 'merge', '-f', outfile, inputs])

    print cmd

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    cmdout, cmderr = proc.communicate()

    if cmdout != '' or cmderr != '':
        raise Exception(cmdout +' '+ cmderr)


def __merge_sam(infiles, outfile):
    '''
    merges a list of sam files into a single sam
    '''
    raise Exception('merging sam files not implemented yet')


def __merge_any(infiles, outfile):
    '''
    merge any given infiles into a single outfile file
    '''

    with open(outfile, 'w') as ofile:

        for ifile in infiles:

            with open(ifile) as f:
                print f.name

                ## read line by line to avoid reading all lines of large files into memory at once
                l = f.readline()

                while l:
                    print >> ofile, l,
                    l = f.readline()


def merge_files(infiles, outfile, ext=None):
    '''
    given a list of files, merges into a single output file.
    supported types are vcf, bam, and sam.
    '''

    # get the filename extension
    if ext is None:
        ext = os.path.splitext(infiles[0])[1]
        ext = ext.replace('.','')

    ## this prevents merge_any from ever being run
    # assert ext == 'vcf' or ext == 'bam' or ext == 'sam', \
    #     'file extension ' + ext + ' not valid. supported extensions are vcf, bam, and sam'

    if ext == 'vcf':
        __merge_vcf(infiles, outfile)

    elif ext == 'bam':
        __merge_bam(infiles, outfile)

    elif ext == 'sam':
        __merge_sam(infiles, outfile)

    else:
        print 'merging any'
        __merge_any(infiles, outfile)


if __name__ == '__main__':
    import mergeui

    args = mergeui.args
    merge_files(args.infiles, args.out, args.extension)

