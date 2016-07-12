'''
Created on Jul 2, 2014

@author: dgrewal
'''
from kronos.utils import ComponentAbstract
import os


class Component(ComponentAbstract):

    def __init__(self, component_name='annot_pygenes',
                 component_parent_dir=None, seed_dir=None):
        self.version = '1.1.5'
        ## initialize ComponentAbstract
        super(Component, self).__init__(component_name,
                                        component_parent_dir, seed_dir)

    def make_cmd(self, chunk=None):
        path = os.path.join(self.seed_dir, 'pygene_annotation.py')
        
        cmd = self.requirements['python'] + ' ' + path
        cmd_args = []

        gene_sets_gtf = self.args.gene_sets_gtf if hasattr(self.args, 'gene_sets_gtf') else None
        gene_sets_gtf_bin = self.args.gene_sets_gtf_bin if hasattr(self.args, 'gene_sets_gtf_bin') else None

        if gene_sets_gtf and gene_sets_gtf_bin:
            raise Exception('Please specify the gtf or the binary (not both)')
        elif gene_sets_gtf is None and gene_sets_gtf_bin is None:
            raise Exception('Please specify either gene_sets_gtf or gene_sets_gtf_bin')

        for k, v in vars(self.args).iteritems():
            if v is None or v is False:
                continue
            cmd_args.append('--'+k)
            if isinstance(v, bool):
                continue
            else:
                cmd_args.extend([v])
        

        return cmd, cmd_args

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
    _main(n)
