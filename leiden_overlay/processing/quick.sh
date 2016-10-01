#! /usr/bin/env sh
#USE: ./quick.sh DYSF

# Use this if you want to rerun the "./run_script" process without the
# very time-consuming web-scraping and VEP compilation stages.
# Only run this if the full ./run_script script has been run on the gene
# previously, and the associated data has not been removed from the 'dat' folder.

if [ "$#" -ne 1 ]; then
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

# divide into different lists
echo "Separating into categories..."
python categorise_types.py $1
awk '!x[$1]++' ./../dat/$1_snp_fixed.txt > ./../dat/$1_snp_fixed_nodup.txt

# separate into powers of 10
echo "Producing logarithmic-grouping data..."
python group_data.py $1

# move results into the results folder
echo "Finalising results folder..."
mkdir -p ./../results/$1
cp ./../dat/$1_final_output.txt ./../results/$1/$1_raw_output.txt
cp ./../dat/$1_sorted.txt ./../results/$1/$1_concise_sorted.txt
cp ./../dat/$1_grouped.txt ./../results/$1/
uniq ./../results/$1/$1_raw_output.txt > ./../results/$1/$1_full_output.txt

#echo "Clearing temporary files..."
#rm ./../dat/*

# create the bar chart
echo "Creating image..."
python make_chart.py $1

# done!
echo "Processing complete for $1."
