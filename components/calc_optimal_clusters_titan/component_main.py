'''
Created on Apr 1,2015
@author: dgrewal
'''

import os

from kronos.utils import ComponentAbstract


class Component(ComponentAbstract):

    def __init__(self, component_name='calc_optimal_clusters_titan', component_parent_dir=None, seed_dir=None):
       self.version = "1.0.0"

        ## initialize ComponentAbstract
       super(Component, self).__init__(component_name, component_parent_dir, seed_dir)

    def make_cmd(self, chunk=None):

        path = os.path.join(self.seed_dir, 'optimal_clusters.py')
        cmd = self.requirements['python'] + ' ' +  path
        cmd_args = ['-i '+self.args.input_dir,
                     '-o '+self.args.output]

        if self.args.sample_id:
            cmd_args.append('--sample_id '+self.args.sample_id)


        return cmd, cmd_args

# to run as stand alone
def _main():
    '''main function'''
    optclus = Component()
    optclus.args = component_ui.args
    optclus.run()

if __name__ == '__main__':

    import component_ui

    _main()
