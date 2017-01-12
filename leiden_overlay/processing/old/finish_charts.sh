#! /usr/bin/env sh

# Makes (or remakes) all the graphs for every gene within the "good_genes.txt" file.
# Only run this after ./big_script has been run at least once before,
# as it retrieves this gene list.

while read p; do
  echo "GENE: $p"
  python make_chart.py $p
done < good_genes.txt
