#! /usr/bin/env sh

while read p; do
  echo "GENE: $p"
  python group_data.py $p
  cp ./../dat/$p\_grouped.txt ./../results/$p/
done < good_genes.txt
