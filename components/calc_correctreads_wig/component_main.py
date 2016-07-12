'''
Created on May 12, 2014

@author: dgrewal

component for titan pipeline
correct the reads from tumour and normal wig files based on the gc and map wig files
'''

from kronos.utils import ComponentAbstract
import os

class Component(ComponentAbstract):

    def __init__(self, component_name='calc_correctreads_wig',
                 component_parent_dir=None, seed_dir=None):
        self.version = '1.1.3'
        ## initialize ComponentAbstract
        super(Component, self).__init__(component_name, 
                                        component_parent_dir, seed_dir)


    def make_cmd(self, chunk=None):
        if not self.args.run_component:
            cmd = 'exit 0'
            cmd_args = []
            return  cmd, cmd_args

        if self.args.hmmcopy:
            path = os.path.join(self.seed_dir, 'correctReadCount.R')
            cmd = ' '.join([self.requirements['R'], '--no-save', '--args'])
            
            if self.args.tumwig and self.args.normwig:
                raise Exception('please provide either tumour or normal wig but not both')
            elif self.args.tumwig:
                infile = self.args.tumwig
            elif self.args.normwig:
                infile = self.args.normwig
            else:
                raise Exception('both tumour and normal wig files are absent')
                            
            cmd_args = [infile, self.args.gc, self.args.map,
                        self.args.mapcutoff,self.args.outfile,
                        self.args.outobj, '<', path]

        else:
            path = os.path.join(self.seed_dir, 'correctReads.R')

            cmd = ' '.join([self.requirements['R'], '--no-save', '--args'])

            cmd_args = [self.args.tumwig, self.args.normwig,
                        self.args.gc, self.args.map,
                        self.args.target_list, self.args.outfile,'<', path]

        return cmd, cmd_args

    def test(self):
        import component_test
        component_test.run()

def _main():
    comp = Component()
    comp.test()
    comp.args = component_ui.args
    #comp.run()

if __name__ == '__main__':
    import component_ui
    _main()

