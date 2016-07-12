'''
Created on Jun 17, 2014

@author: dgrewal
##tests for the count_component
'''

import unittest
import component_reqs, component_main
import subprocess
import os
from collections import defaultdict

class args():
    def __init__(self):
        self.id = '1'
        self.infile = './component_test/infile'
        self.cnfile = './component_test/cnfile'
        self.map = '/share/lustre/dgrewal/Miscellaneous/component_tests/test_bam/GRCh37-lite.map.ws_1000.wig'
        self.num_clusters = '1'
        self.num_cores = '4'
        self.ploidy = '2'
        self.outfile = './component_test/outfile'
        self.outparam = './component_test/params'
        self.myskew = '0'
        self.bool_est_ploidy = 'TRUE'
        self.n_zero = '1'
        self.norm_est_meth = 'map'
        self.max_i = '5'
        self.pseudo_counts = '1e-300'
        self.txn_exp_len = '1e9'
        self.txn_z_strength = '1e9'
        self.alpha_k = '2500'
        self.maxcn='8'
        self.alpha_high = '20000'
        self.sym='TRUE'
        self.obj_outfile='./component_test/obj' 

class check_requirements(unittest.TestCase):
    def setUp(self):
        self.args = args()
        
    #make sure that the required fields are present in reqs file
    def __get_version_main(self):
        main_stream = open('component_main.py')
        for line in main_stream:
            if 'self.version' in line:
                return eval(line.strip().split('=')[1])
        return None

    def test_version(self):
        main_version = self.__get_version_main() 
        version = component_reqs.version
        
        self.assertNotEqual(main_version, None, 'Could not retrieve the version from component_main')
        self.assertEqual(main_version, version, 'the version in component_main and component_reqs did not match') 

    #make sure that the required fields are present in reqs file
    def test_verify_reqs(self):
        try:
            _ = component_reqs.env_vars
            _ = component_reqs.interval_file
            _ = component_reqs.memory
            _ = component_reqs.parallel
            _ = component_reqs.parallel_params
            _ = component_reqs.requirements
            _ = component_reqs.version
            _ = component_reqs.seed_version
        except:
            self.assertEqual(True, False, 'Please complete the requirements file')
        
        try:
            _ = component_reqs.parallel_run
            self.assertEqual(True, False, 'The parallel_run option must be called parallel in compoenent')
        except:
            pass
        try:
            _ = component_reqs.parallel_mode
            self.assertEqual(True, False, 'The parallel_mode option has been removed')
        except:
            pass

    def test_component(self):
        component = component_main.Component()
        component.args = self.args
        component.run()

        import filecmp
        filecmp.cmp('./component_test/outfile', './component_test/outfile_ref')

        os.remove(self.args.outfile)
        os.remove(self.args.obj_outfile)
        os.remove(self.args.outparam)

        
    def test_verify_R(self):
        cmd = component_reqs.requirements['Rscript'] + ' --version'
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        cmdout, cmderr = proc.communicate()
        
        if cmdout=='' and cmderr == '':
            self.assertEqual(True, False, 'Couldn\'t retreive the version information')
        elif cmdout != '' and cmderr != '':
            err = cmdout + ' ' +cmderr
            self.assertEqual(True, False, 'Couldn\'t retreive the version information: '+err)
        elif cmdout == '':
            val = cmderr.strip().split()[-2].split('.') 
        elif cmderr == '':
            val = cmdout.strip().split()[-2].split('.')
        
        self.assertGreaterEqual(int(val[0]), 3, 'The major version of R must be 3 or greater')
        if int(val[0])>3:
            return
        
        self.assertGreaterEqual(int(val[1]), 1, 'The minor version of R must be 1 or greater')
        
    def test_verify_titan(self):
        cmd = component_reqs.requirements['Rscript'] + ''' -e "packageVersion('TitanCNA')" '''
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        cmdout, cmderr = proc.communicate()
        
        if (cmdout == '' and cmderr == '') or  (cmdout != '' and cmderr != ''):
            self.assertEqual(True, False, 'Error retreiving the version information: '+cmdout+' '+cmderr)
 
        elif cmdout == '':
            val = cmderr.strip().split()[1].decode('unicode_escape').encode('ascii','ignore').split('.') 
        
        elif cmderr == '':
            val = cmdout.strip().split()[1].decode('unicode_escape').encode('ascii','ignore').split('.')
        print val
        self.assertGreaterEqual(int(val[0]), 1, 'The major version of Titan must be 1 or greater')
        if int(val[0])>1:
            return
        self.assertGreaterEqual(int(val[1]), 3, 'The minor version of Titan must be 3 or greater')
        if int(val[0])>3:
            return
        self.assertGreaterEqual(int(val[2]), 0, 'The patch version of Titan must be 0 or greater')

    def test_make_cmd(self):
        comp = component_main.Component()
        comp.args = self.args
        cmd,cmd_args = comp.make_cmd()
        cmd_args = ' '.join(map(str,cmd_args))
        
        #The actual resulting command:
        real_command = component_reqs.requirements['R']+' --no-save --args' 
        real_command_args = ['1','./component_test/infile',
                             './component_test/cnfile',
                             '/share/lustre/dgrewal/Miscellaneous/component_tests/test_bam/GRCh37-lite.map.ws_1000.wig',
                             '1','4','2','./component_test/outfile',
                             './component_test/params',
                             '0','TRUE','1','map','5','1e-300','1e9','1e9','2500','20000','8', 'TRUE',
                             './component_test/obj',
                             '<',os.path.abspath('./component_seed')+'/titan.R']
        
        real_command_args = ' '.join(real_command_args)
        
        print cmd_args
        print real_command_args
        #Ensure that the commands match exactly
        self.assertEqual(real_command, cmd, 'Please recheck the cmd variable in make_cmd')
        
        #Ensure that each of the args are present in the command args list
        #Exact match not possible since order can change 
        self.assertEqual(real_command_args, cmd_args , 'Please recheck the cmd_args list in make_cmd')
                
    def test_params(self):
        try:
            from component_params import input_files,input_params,output_files,return_value
        except:
            self.assertEqual(True,False,'Please complete the params file')
        
        try:
            import component_ui   
        except:
            #cannot run this test if running in unittest mode as ui isn't available
            self.assertEqual(True, True, '') 
            return
            
        arg_act = defaultdict(tuple)
        for val in component_ui.parser._actions[1:]:
            arg_act[val.dest] = (val.required,val.default)
            if val.required == None:
                self.assertEqual(val.default, None, 'The optional argument: '+ val.dest+' has no default value')
        
        params_dict = dict(input_files.items() + input_params.items() + output_files.items())
        for dest,(req,default) in arg_act.iteritems():
            if req == True:
                self.assertEqual(params_dict[dest], '__REQUIRED__', 'params and ui dont match')
            else:
                if not params_dict[dest] in [default,'__OPTIONAL__']:
                    self.assertEqual(True, False, 'Please ensure that either default or ' +\
                                     '__OPTIONAL__ flag is provided for: '+params_dict[dest])
        
 
    
def run():
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    
    checkreqs = loader.loadTestsFromTestCase(check_requirements)
    
    suite.addTests(checkreqs)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
