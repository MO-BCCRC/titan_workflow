# -*- coding: utf-8 -*-
"""
Last Updated: Jun 3 2015

@author dgrewal

reads titan seg files, filters and writes the output in tsv format
"""


input_files = {
               'all_files': '__OPTIONAL__',
               'infile': '__OPTIONAL__',
               'paramsfile':'__OPTIONAL__'}

output_files = {'result': '__REQUIRED__'}


input_params = {
                'tumour_id':'__OPTIONAL__',
                'normal_id':'__OPTIONAL__',
                'label_mapping':'__OPTIONAL__',
                'genes':'__OPTIONAL__',
                'segment_size_threshold': '5000',
                'types':'__OPTIONAL__',
                'project':'__OPTIONAL__',
                'chromosomes':None,
                }

return_value = []
