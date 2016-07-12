'''
Created on Apr 29, 2014

@author: jtaghiyar
'''
input_files  = {'tumour':'__OPTIONAL__', 
                'normal':'__OPTIONAL__', 
                'reference':'__REQUIRED__', 
                'model':'__REQUIRED__',
                'config':'metadata.config', 
                'positions_file':None}

output_files = {'export_features':None,
                'log_file':'mutationSeq_run.log',
                'out':'__REQUIRED__'}

input_params = {'all':'__FLAG__', 
                'buffer_size':'2G',
                'coverage':4,
                'deep':'__FLAG__',
                'interval':None,
                'no_filter':'__FLAG__',
                'normalized':'__FLAG__',
                'normal_variant':25,
                'purity':70,
                'mapq_threshold':20,
                'baseq_threshold':10,
                'indl_threshold':0.05,
                'manifest':'__OPTIONAL__',
                'single':'__FLAG__',
                'threshold':0.5,
                'tumour_variant':2,
                'features_only':'__FLAG__',
                'verbose':'__FLAG__',
                'titan_mode':'__FLAG__'}

return_value = []

                    
                    
