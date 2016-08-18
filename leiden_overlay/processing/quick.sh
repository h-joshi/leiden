if [ "$#" -ne 1]; then
    echo "Error: No gene argument supplied"
    exit 1
fi

# form the final result output
echo "Generating result file..."
python process_data.py $1

# sort the data
echo "Sorting by frequency..."
python sort_data.py $1
awk '!x[$1]++' ./../dat/$1_sorted.txt > ./../dat/$1_sorted_nodup.txt

# extract snps
echo "Extracting SNPs..."
python extract_snps.py $1
awk '!x[$1]++' ./../dat/$1_snp_fixed.txt > ./../dat/$1_snp_fixed_nodup.txt

# separate into powers of 10
echo "Producing logarithmic-grouping data..."
python group_data.py $1

#results
echo "Finalising results folder..."
mkdir -p ./../results/$1
cp ./../dat/$1_final_output.txt ./../results/$1/$1_raw_output.txt
cp ./../dat/$1_sorted.txt ./../results/$1/$1_concise_sorted.txt
cp ./../dat/$1_grouped.txt ./../results/$1/
uniq ./../results/$1/$1_raw_output.txt > ./../results/$1/$1_full_output.txt

# create the bar chart
echo "Creating image..."
python make_chart.py $1

# done!
echo "Processing complete for $1."
