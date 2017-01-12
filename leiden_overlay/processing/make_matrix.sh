#! /usr/bin/env sh

# Generates a full complete matrix for all the genes in the Leiden database
# that were retrieved using ./big_script.
# Outputs it as big_mat.txt - a tab delimited file

# Two stages. Uncomment or comment out the first stage to skip it if preferred.

# Stage 1: Generate all the separate matrix files for each of the genes.
while read p; do
  echo "GENE: $p"
  python compile_gene_data.py $p
done < good_genes.txt

# Stage 2: Concatenate all these matrix files into one large and complete matrix.
echo > big_mat.txt
cat ./mat_dat/ALL_DYSF.mat | head -1 > big_mat.txt # adds in the column names
for f in ./mat_dat/*; do
  echo "processing $f"
  cat $f | tail -n+2 >> big_mat.txt
done
