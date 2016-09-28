#! /usr/bin/env sh

#while read p; do
#  echo "GENE: $p"
#  python compile_all_genes.py $p
#done < good_genes.txt

echo > big_mat.txt
cat ./mat_dat/ALL_DYSF.mat | head -1 > big_mat.txt
for f in ./mat_dat/*; do
  echo "processing $f"
  cat $f | tail -n+2 >> big_mat.txt
done
