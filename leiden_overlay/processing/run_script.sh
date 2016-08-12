#! /usr/bin/env sh

# create the initial files using andrew's scripts
python ./../../bin/extract_data.py --leiden_url http://www.dmd.nl/nmdb2/ -o ../dat --gene_list $1
echo "../dat/$1.txt" > file_list.txt
python ./../../bin/generate_annotated_vcf.py -f file_list.txt

# use VEP to gather all the data together
perl ~/ensembl-tools-release-84/scripts/variant_effect_predictor/variant_effect_predictor.pl -i ../dat/$1.vcf --cache --port 3337 --maf_exac --force_overwrite -o ./../dat/$1\_VEP_FINAL.txt

