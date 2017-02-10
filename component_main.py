'''

Created on May 12, 2014

@author: dgrewal

component for titan pipeline
generate the wig file
'''

from kronos.utils import ComponentAbstract
import os
import sys

class Component(ComponentAbstract):

    def __init__(self,component_name='run_readcounter', component_parent_dir=None, seed_dir=None):
        self.version = '1.1.6'
        ## initialize ComponentAbstract
        super(Component, self).__init__(component_name, component_parent_dir, seed_dir)

    def make_cmd(self,chunk):
        #switch to enable/disable the component
        if not self.args.run_component:
            cmd= 'exit 0'
            cmd_args = []
            return cmd, cmd_args

        command = os.path.join(self.seed_dir, 'readCounter')


        #couldn't iterate as the order isn't preserved in args object
        command_args = [self.args.bam, '-w'+str(self.args.w),
                       '-q'+str(self.args.q)]


        if self.args.chromosomes:
            if isinstance(self.args.chromosomes, list):
                chrs = ','.join(self.args.chromosomes)
                command_args.extend(['-c', chrs])
            else:
                command_args.extend(['-c', self.args.chromosomes])


        command_args.extend(['>', self.args.out])

        return command,command_args

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
