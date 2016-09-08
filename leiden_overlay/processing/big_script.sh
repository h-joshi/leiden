#! /usr/bin/env sh
#USE: ./run_script DYSF

echo "Gathering gene names from Leiden..."
python get_gene_list.py
loc="./../dat/gene_list.txt"
echo "Performing analysis..."
var=1
num="`wc -l < $loc`"
# FIX THIS LINE

echo > genes.txt
echo > good_genes

while read p; do
  echo "Gene $var out of $num [$p]..."
  ./run_script.sh $p
  if [ $? -eq 0 ]; then
    echo $p >> genes.txt
  else
    echo $p >> good_genes.txt
  fi
  ((++var))
  sleep 6
done < $loc
