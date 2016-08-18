# form the final result output
echo "Generating result file..."
python process_data.py

# sort the data
echo "Sorting by frequency..."
python sort_data.py
awk '!x[$1]++' ./../dat/$1_sorted.txt > ./../dat/$1_sorted_nodup.txt

# extract snps
echo "Extracting SNPs..."
python extract_snps.py
awk '!x[$1]++' ./../dat/$1_snp_fixed.txt > ./../dat/$1_snp_fixed_nodup.txt

# separate into powers of 10
echo "Producing logarithmic-grouping data..."
python group_data.py

#results
echo "Finalising results folder..."
mkdir -p ./../results/$1
cp ./../dat/DYSF_final_output.txt ./../results/$1/DYSF_raw_output.txt
cp ./../dat/DYSF_sorted.txt ./../results/$1/DYSF_concise_sorted.txt
cp ./../dat/DYSF_grouped.txt ./../results/$1/
uniq ./../results/$1/DYSF_raw_output.txt > ./../results/$1/DYSF_full_output.txt
# done!
echo "Processing complete for $1."
