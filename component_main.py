'''

Created on May 12, 2014

@author: dgrewal

component for titan pipeline
create the segment files (including the IGV compatible seg file)
'''

from kronos.utils import ComponentAbstract
import os

class Component(ComponentAbstract):

    def __init__(self, component_name='calc_cnsegments_titan',
                 component_parent_dir=None, seed_dir=None):
        self.version = '1.1.2'
        ## initialize ComponentAbstract
        super(Component, self).__init__(component_name,
                                        component_parent_dir, seed_dir)


    def make_cmd(self, chunk=None):
        path = os.path.join(self.seed_dir, 'createTITANsegmentfiles.pl')
        cmd = self.requirements['perl'] + ' ' + path

        cmd_args = ['-id='+str(self.args.id),
                    '-infile='+self.args.infile,
                    '-outfile='+self.args.outfile,
                    '-outIGV='+self.args.outigv,
                    '-symmetric='+self.args.symmetric]
        return cmd,cmd_args

    def test(self):
        import component_test
        component_test.run()

def _main():
    comp = Component()
    comp.args = component_ui.args
    comp.run()
    comp.test()

if __name__ == '__main__':
    import component_ui
    _main()
