#! /usr/bin/env sh

while read p; do
  echo "GENE: $p"
  python make_chart.py $p
done < good_genes.txt
