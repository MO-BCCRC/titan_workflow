'''
Created on Mar 11, 2014

@author: jtaghiyar
'''
from kronos.utils import ComponentAbstract
import os
import subprocess

class Component(ComponentAbstract):
    '''
    mutationSeq component
    '''

    def __init__(self, component_name='run_mutationseq', component_parent_dir=None, seed_dir=None):
        self.version = "1.0.10"

        ## initialize ComponentAbstract
        super(Component, self).__init__(component_name, component_parent_dir, seed_dir)


    def focus(self, cmd, cmd_args, chunk):
        cmd_args.append('--interval ' + str(chunk))
        return cmd, cmd_args

    def make_cmd(self, chunk=None):
        if self.args.titan_mode:
            classifier_path = os.path.join(self.requirements['mutationseq'], 'preprocess.py')
        else:
            classifier_path = os.path.join(self.requirements['mutationseq'], 'classify.py')   

        cmd = self.requirements['python'] + ' ' + classifier_path


        ## 'samples' parameter is parsed into four different parameters in the component_params.py,
        ## i.e. 'tumour', 'normal', 'reference', 'model'. This makes it easier for the user to
        ## specify different sets of input samples in the '__SAMPLES__' section of the config file
        ## when they want to run it in multi-sample mode.
        ## Note that this only requires to change the component_params.py and does NOT have
        ## anything to do with component_ui.py.
        if not 'samples' in self.args:
            ## made it so that one can specify only the model basename in the config.yaml to
            ## access the model in component seed
            if not os.path.isfile(self.args.model):
                model = os.path.join(self.requirements['mutationseq'], os.path.basename(self.args.model))
            else:
                model = self.args.model

            samples = [
                       'reference:' + self.args.reference,
                       'model:' + model
                       ]

            ## check if single sample or paired
            if self.args.tumour is not None:
                samples.append('tumour:' + self.args.tumour)

            if self.args.normal is not None:
                samples.append('normal:' + self.args.normal)

            ## delete the excessive options from the self.args namespace
            del vars(self.args)['tumour']
            del vars(self.args)['normal']
            del vars(self.args)['reference']
            del vars(self.args)['model']

        ## If the component is run as a stand alone and since the component_ui still has the
        ## 'samples' parameter and NOT the mentioned four different parameters, then user would
        ## specify the inputs to the 'samples' parameter.
        else:
            samples = self.args.samples
        
        
        cmd_args = [" ".join(samples)]
        for k, v in vars(self.args).iteritems():
            if k == 'titan_mode':
                continue
            if v is None:
                continue
            if k == 'config':
                if v is not None and not os.path.isfile(v):
                    config_file = os.path.join(self.requirements['mutationseq'], os.path.basename(v))
                else:
                    config_file = v

                cmd_args.extend(['--'+k, config_file])
                continue

            if v and k != 'samples' and k != 'component_dir':
                cmd_args.append('--'+k)
                if isinstance(v, bool):
                    continue

                else:
                    cmd_args.extend([v])
           
            # if v is 0 then it doesn't enter any of the previous loops as 0 evaluates as False/None
            if not isinstance(v, bool) and v == 0:
                cmd_args.extend(['--'+k, v])       

        if chunk is not None:
            cmd, cmd_args = self.focus(cmd, cmd_args, chunk)

        checker = '\n if ! grep -q "successfully completed" '+self.args.log_file+'; then exit -1; fi'
        cmd_args.append(checker)

        return cmd, cmd_args


## to run as stand alone
def _main():
    m = Component()
    m.args = component_ui.args
    m.run()


if __name__ == '__main__':
    import component_ui

    _main()

