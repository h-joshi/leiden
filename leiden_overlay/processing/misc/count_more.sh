#! /usr/bin/env bash

rm -rf tmp_data.txt
touch tmp_data.txt
cd ./../../results

gene_count=0
variant_count=0
for f in `ls`; do
	echo $f
	cd $f
	if ls *.png; then
		((++gene_count))
		((--variant_count))
		curr=`wc -l < $f\_full_output.txt`
		variant_count=`expr $variant_count + $curr`
		cat $f\_full_output.txt | tail -n +2 >> ./../../processing/misc/tmp_data.txt
	else
		echo $f 'failed'
	fi
	cd ..
done
echo $gene_count ': ' $variant_count
