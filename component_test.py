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
import component_ui

 #class args():
 #    def __init__(self):
 #        self.tumour = '/share/lustre/dgrewal/Miscellaneous/component_tests/test_bam/DG1136a_5Mbp.bam'
 #        self.normal = '/share/lustre/dgrewal/Miscellaneous/component_tests/test_bam/DG1136N_5Mbp.bam'
 #        self.reference = '/share/lustre/reference/genomes/GRCh37-lite.fa'
 #        self.model = os.path.join(os.path.abspath('./component_seed'),'model_v4.1.1.npz')
 #        self.config = os.path.join(os.path.abspath('./component_seed'),'metadata.config')
 #        self.positions_file = None
 #        self.export_features = None
 #        self.log_file = './component_test/log'
 #        self.out = './component_test/out'
 #        self.all = None
 #        self.coverage = 4
 #        self.buffer_size = '2G'
 #        self.deep = None
 #        self.interval = 1
 #        self.no_filter = True
 #        self.normalized  = None
 #        self.normal_variant = 25
 #        self.purity =70
 #        self.mapq_threshold = 20
 #        self.baseq_threshold = 10
 #        self.single = None
 #        self.threshold = 0.5
 #        self.tumour_variant = 2 
 #        self.features_only = None
 #        self.varbose = None
 #        self.titan_mode = None
 #        self.return_cov =  None
 
class componentTests(unittest.TestCase):
    def setUp(self):
        self.args = component_ui.args
        self.tumour = '/share/lustre/dgrewal/Miscellaneous/component_tests/test_bam/DG1136a_5Mbp.bam'
        self.normal = '/share/lustre/dgrewal/Miscellaneous/component_tests/test_bam/DG1136N_5Mbp.bam'
        self.reference = '/share/lustre/reference/genomes/GRCh37-lite.fa'
        self.model = os.path.join(os.path.abspath('./component_seed'),'model_v4.1.1.npz')       
  
      
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
        filecmp.cmp('./component_test/out', './component_ref/out_ref')
        
        os.remove(self.args.out)
        os.remove(self.args.log)

    def test_make_cmd(self):
        comp = component_main.Component()
        comp.args = self.args
        cmd,cmd_args = comp.make_cmd(chunk = None)
        cmd_args = ' '.join(map(str,cmd_args))
        
        #The actual resulting command:
        real_command = os.path.join(os.path.abspath('./component_seed'), 'classify.py') 
        real_command_args = []

        print '*'*50
        print cmd_args
	print '*'*50        

        #Ensure that the commands match exactly
        self.assertEqual(real_command, cmd, 'Please recheck the cmd variable in make_cmd')
        
        #Ensure that each of the args are present in the command args list
        #Exact match not possible since order can change 
        for val in real_command_args:
            if not val in cmd_args:
                self.assertEqual(True, False, 'Please recheck the cmd_args list in make_cmd')
                
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
        
        #merge all the dictionaries together
        params_dict = dict(input_files.items() + input_params.items() + output_files.items())
        
        for dest,(req,default) in arg_act.iteritems():
            if req == True:
                self.assertEqual(params_dict[dest], '__REQUIRED__', 'params and ui dont match')
            else:
                if not params_dict[dest] in [default,'__OPTIONAL__', '__FLAG__']:
                    self.assertEqual(True, False, 'Please ensure that either default or ' +\
                                     '__OPTIONAL__ flag is provided for: '+dest)

def run():
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    
    checkreqs = loader.loadTestsFromTestCase(componentTests)
    
    suite.addTests(checkreqs)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
