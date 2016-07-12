'''
Created on May 26, 2014

@author: dgrewal
'''
input_files  = {'infile':'__REQUIRED__',
                'cnfile':'__REQUIRED__', 
                'map':'__REQUIRED__'
                }

output_files = {'outfile':'__REQUIRED__',
                'outparam':'__REQUIRED__',
                'obj_outfile':'__REQUIRED__'
                }

input_params = {'id':'__REQUIRED__', 
                'num_clusters':'1',
                'num_cores':'4',
                'ploidy':'2',
                'myskew':'0',
                'estimate_ploidy':'TRUE',
                'normal_param_nzero':'__REQUIRED__',
                'normal_estimate_method':'map',
                'max_iters':'5',
                'pseudo_counts':'1e-300',
                'txn_exp_len':'1e9',
                'txn_z_strength':'1e9',
                'alpha_k':'2500',
                'alpha_high':'20000',
                'max_copynumber':'8',
                'symmetric':'TRUE',
                'genome_type': '__REQUIRED__',
                'chromosomes': None,
                'y_threshold': '20',
                'max_depth':'200',
                }

return_value = []
