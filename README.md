#parse_titan

reads titan seg files, filters and writes the output in tsv format



###Development information

```

Date created : Mar 2, 2015

Last update  : Sep 16, 2015

Developer: Diljot Grewal (dgrewal@bccrc.ca)

Input        : tsv file

Output       : tsv file

Version: 1.0.0

Parameters: 

	label_mapping

	project

	segment_size_threshold

	chromosomes

	normal_id

	genes

	tumour_id

	types

Inputs: 

	all_files

	paramsfile

	infile

Outputs: 

	result

Seed: create_case_gene_type_titan.py create_case_gene_type_titan.pyc titanparser.py

```



###Usage

```

usage: component_ui.py [-h] (--all_files ALL_FILES | --infile INFILE)

                       [--paramsfile [PARAMSFILE [PARAMSFILE ...]]]

                       [--tumour_id TUMOUR_ID] [--normal_id NORMAL_ID]

                       [--label_mapping LABEL_MAPPING] [--genes GENES]

                       [--segment_size_threshold SEGMENT_SIZE_THRESHOLD]

                       [--types [TYPES [TYPES ...]]] [--result RESULT]

                       [--project PROJECT]

                       [--chromosomes [CHROMOSOMES [CHROMOSOMES ...]]]



optional arguments:

  -h, --help            show this help message and exit

  --all_files ALL_FILES

                        Input directory

  --infile INFILE       Input files

  --paramsfile [PARAMSFILE [PARAMSFILE ...]]

                        params files for the infiles (only required when

                        params file is specified)

  --tumour_id TUMOUR_ID

                        tumour id for the infile (only required when infile is

                        specified)

  --normal_id NORMAL_ID

                        normal id for the infile (only required when infile is

                        specified)

  --label_mapping LABEL_MAPPING

                        File with labels for each case

  --genes GENES         filters out all the genes except the ones specified

                        here (default : no filtering)

  --segment_size_threshold SEGMENT_SIZE_THRESHOLD

                        filters out all the segments that are smaller than the

                        threshold(default : 5000 bases)

  --types [TYPES [TYPES ...]]

                        filters out all the states except the ones specified

                        here (default : no filtering)

  --result RESULT       Resulting file name

  --project PROJECT     The project name for the input files

  --chromosomes [CHROMOSOMES [CHROMOSOMES ...]]

                        all chromosomes except the ones provided will be

                        filtered (default: no filtering)



```

###Dependencies

python



###Known Issues







###Change Log

