# -*- coding: utf-8 -*-
"""
Last Updated: Jun 3 2015

@author dgrewal

reads titan seg files, filters and writes the output in tsv format
"""


import os

from kronos.utils import ComponentAbstract
import warnings

class Component(ComponentAbstract):
    '''
    create_case_gene_type_titan component
    '''

    def __init__(self, component_name='parse_titan', component_parent_dir=None, seed_dir=None):
        self.version = "1.0.0"

        ## initialize ComponentAbstract
        super(Component, self).__init__(component_name, component_parent_dir, seed_dir)

    def __focus(self, cmd, cmd_args, chunk):
        if ':' not in chunk or not len(chunk.split(':')) == 2:
            warnings.warn('skipping focus due to incorrect chunk format')
            return cmd, cmd_args

        proj = chunk.split(':')[0]
        chunk = chunk.split(':')[1]
        cmd_args.extend(['--all_files ',chunk])
        cmd_args.extend(['--project ', proj])
        return cmd, cmd_args

    def make_cmd(self, chunk=None):
        cmd = self.requirements['python'] + ' ' + os.path.join(self.seed_dir, 'create_case_gene_type_titan.py') 

        cmd_args = []
        for k, v in vars(self.args).iteritems():
            if v is None:
                continue

            if isinstance(v, bool):
                if v: 
                    cmd_args.append('--' + k)
                    continue
            else:
                if isinstance(v, list):
                    v = ' '.join(v)
                cmd_args.extend(['--' + k , v])
        if chunk is not None:
            cmd, cmd_args = self.__focus(cmd,cmd_args, chunk)
        
        return cmd, cmd_args


## to run as stand alone
def _main():
    m = Component()
    m.args = component_ui.args
    m.run()

if __name__ == '__main__':
    import component_ui

    _main()

