#! /usr/bin/env sh

# Make (or remake) the "grouped data" results file for each of the genes
# in the "good_genes.txt" list.

while read p; do
  echo "GENE: $p"
  python group_data.py $p
  cp ./../dat/$p\_grouped.txt ./../results/$p/
done < good_genes.txt
