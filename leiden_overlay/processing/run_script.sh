#! /usr/bin/env sh

#USE: ./run_script DYSF

echo "Gathering data from Leiden..."
# create the initial files using andrew's scripts
python ./../../bin/extract_data.py --leiden_url http://www.dmd.nl/nmdb2/ -o ../dat --gene_list $1
echo "../dat/$1.txt" > file_list.txt
echo "Generating VCF file..."
python ./../../bin/generate_annotated_vcf.py -f file_list.txt


# use VEP to gather all the data together
echo "Bringing data in from VEP and ExAC..."
perl ~/ensembl-tools-release-84/scripts/variant_effect_predictor/variant_effect_predictor.pl -i ../dat/$1.vcf --cache --port 3337 --maf_exac --force_overwrite -o ./../dat/$1.vep.txt

# form the final result output
echo "Generating result file..."
python process_data.py

# done!
echo "Result file generated for $1!"
