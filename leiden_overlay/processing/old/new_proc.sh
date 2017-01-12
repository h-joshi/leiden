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
#python add_pathogenicity.py $1
#echo "Generating result file..."
#python process_data.py $1

# move results into the results folder
echo "Finalising results folder..."
mkdir -p ./../results/$1/new
cp ./../dat/$1_full_output.txt ./../results/$1/new/$1_raw_output.txt
uniq ./../results/$1/new/$1_raw_output.txt > ./../results/$1/new/$1_full_output.txt

# create the bar chart
#echo "Creating image..."
#python make_full_chart.py $1

# done!
echo "Processing complete for $1."
