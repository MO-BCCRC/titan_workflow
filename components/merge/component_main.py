'''
Created on Jun 26, 2014

@author: jtaghiyar
'''
from kronos.utils import ComponentAbstract
import os


class Component(ComponentAbstract):
    '''
    merge component
    '''
    
    def __init__(self, component_name='merge', component_parent_dir=None, seed_dir=None):
        self.version = "1.0.0"
        
        ## initialize ComponentAbstract 
        super(Component, self).__init__(component_name, component_parent_dir, seed_dir)
        
    
    def make_cmd(self, chunk=None):
        merger_path = os.path.join(self.seed_dir, 'merge.py')

        cmd = self.requirements['python'] + ' ' + merger_path
        cmd_args = [" ".join(self.args.infiles)]

        for k, v in vars(self.args).iteritems():
            if v and k != 'infiles' and k != 'component_dir':
                cmd_args.append('--'+k)
                if isinstance(v, bool):
                    continue

                else:
                    cmd_args.extend([v])

        cmd_args.append('--samtools ' + self.requirements['samtools'])
        
        return cmd, cmd_args
    
       
## to run as stand alone 
def _main():
    c = Component()
    c.args = component_ui.args
    c.run()


if __name__ == '__main__':
    import component_ui
    
    _main()
    
