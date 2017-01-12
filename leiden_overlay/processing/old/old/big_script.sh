#! /usr/bin/env sh
#USE: ./big_script

# Runs the data grabber script (./run_script) on all the reported genes in the
# Leiden database [as retrieved from get_gene_list.py in ../dat/gene_list.txt]
# Requires no previous program to have run beforehand.

echo "Gathering gene names from Leiden..."
python get_gene_list.py
loc="./../dat/gene_list.txt"
echo "Performing analysis..."
num="`wc -l < $loc`"

var=1
rm -rf bad_genes.txt
rm -rf good_genes.txt
touch bad_genes.txt
touch good_genes.txt

while read p; do
  echo "Gene $var out of $num [$p]..."
  ./run_script.sh $p

  # categorise it as a good gene or bad gene depending on if its data could be
  # retrieved from the Leiden site (bad means no data is available)
  if [ $? -eq 0 ]; then
    echo $p >> good_genes.txt
  else
    echo $p >> bad_genes.txt
  fi

  ((++var))

  # wait 6 seconds - this is to prevent being blocked from accessing the Leiden
  # site due to too many requests
  sleep 6

done < $loc
