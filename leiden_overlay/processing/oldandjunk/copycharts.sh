#! /usr/bin/env sh 

while read p; do
	echo "GENE: $p"
	cp ./../results/$p/$p\_chart.png ./../backup/charts/
done < good_genes.txt
