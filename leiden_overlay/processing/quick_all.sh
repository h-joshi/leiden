#! /usr/bin/env sh
#USE: ./big_script

# Runs the data grabber script (./run_script) on all the reported genes in the
# Leiden database [as retrieved from get_gene_list.py in ../dat/gene_list.txt]
# Requires no previous program to have run beforehand.

var=0
num=`wc -l good_genes.txt`

while read p; do
  echo "Gene $var out of $num [$p]..."
  ./quick.sh $p
  ((++var))
done < good_genes.txt

# make the matrix
echo "Generating Leiden matrix..."
./make_matrix.sh
