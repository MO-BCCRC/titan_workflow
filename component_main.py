'''

Created on May 12, 2014

@author: dgrewal

component for titan pipeline

generate counts using the tumour/normal bam files for the positions provided
'''

from kronos.utils import ComponentAbstract
import os

class Component(ComponentAbstract):

    def __init__(self, component_name='convert_museq_vcf2counts',
                 component_parent_dir=None, seed_dir=None):
        self.version = '1.1.3'
        ## initialize ComponentAbstract
        super(Component, self).__init__(component_name,
                                        component_parent_dir, seed_dir)

    def make_cmd(self, chunk=None):
        path = os.path.join(self.seed_dir, 'transform_vcf_to_counts.py')

        cmd = self.requirements['python'] + ' ' + path
        cmd_args = ['--infile',self.args.infile,'--outfile',
                    self.args.outfile]

        if self.args.positions_file:
            cmd_args.extend(['--positions_file',self.args.positions_file])

        return cmd, cmd_args

    def test(self):
        import component_test
        component_test.run()

def _main():
    comp = Component()
    comp.test()
    comp.args = component_ui.args
    comp.run()

if __name__ == '__main__':
    import component_ui
    _main()
