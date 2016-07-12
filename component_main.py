'''

Created on May 12, 2014

@author: dgrewal

component for titan pipeline
Generate plots
'''

from kronos.utils import ComponentAbstract
import os

class Component(ComponentAbstract):

    def __init__(self,component_name='plot_titan',
                component_parent_dir=None, seed_dir=None):
        self.version = '1.1.4'
        ## initialize ComponentAbstract
        super(Component, self).__init__(component_name,
                                        component_parent_dir, seed_dir)


    def make_cmd(self, chunk=None):
        path = os.path.join(self.seed_dir,'plot_titan.R')

        cmd = ' '.join([self.requirements['R']+'script', path])

        if chunk is not None:
            params = eval(chunk)
            num_clusters = params['num_clusters']
            ploidy = params['ploidy']
        else:
            num_clusters = self.args.num_clusters
            ploidy = self.args.ploidy

        if self.args.chr:
            if type(self.args.chr) is not list:
                raise Exception('Chromosomes should be list')
            chr = ["'"+str(val)+"'" for val in self.args.chr]

            chr = '"c('+ ','.join(chr)+')"'
            cmd_args = [self.args.obj_file, self.args.outdir, num_clusters, self.args.id,
                        self.args.rid,chr, ploidy]
        else:
            chr = '"c(1:22,\'X\')"'
            cmd_args = [self.args.obj_file, self.args.outdir, num_clusters, self.args.id,
                        self.args.rid, chr, ploidy]


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

