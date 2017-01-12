###---###---###---###---###
#   Separates all the gathered sorted data into different files based on the
#   variant's type: SNPS (snp), deletions (del), duplications (dup) and other (other).
#
#   Moreover, makes a second file for only those SNPs with ExAC data available -
#   called GENE_snp_fixed.txt.
#
#   Requires the 'GENE_sorted.txt' to have been made, which comes from the
#   sort_data.py script.
#
#   Outputs GENE_snp.txt, GENE_snp_fixed.txt, GENE_del.txt, GENE_dup.txt, and
#   GENE_other.txt all in the dat folder.
###---###---###---###---###

import sys

# get the gene name from the terminal
input_gene = sys.argv[1]

# open the original sorted table
gene_csv = open("../dat/" + input_gene + "_sorted.txt")
lines = [line.rstrip('\n').split('\t') for line in gene_csv]
gene_csv.close()

col_list = lines[0]
type_index = col_list.index("type")
freq_index = col_list.index("deduced_allele_frequency")
del col_list[type_index]
col_names = '\t'.join(col_list)
del lines[0]


snp_file = open("./../dat/" + input_gene + "_snp.txt", "w")
snps_fixed = open("./../dat/" + input_gene + "_snp_fixed.txt", "w")
del_file = open("./../dat/" + input_gene + "_del.txt", "w")
dup_file = open("./../dat/" + input_gene + "_dup.txt", "w")
other_file = open("./../dat/" + input_gene + "_other.txt", "w")

# write the column names to each file
snp_file.write(col_names + '\n')
snps_fixed.write(col_names + '\n')
del_file.write(col_names + '\n')
dup_file.write(col_names + '\n')
other_file.write(col_names+'\n')

# perform the separation - write the relevant variants to each file
for line in lines:
    if line[type_index] == "snp":
        freq = line[freq_index]
        del line[type_index]
        snp_file.write('\t'.join(line) + '\n')

        # if the ExAC data is available, add it into GENE_snp_fixed as well
        if not 'No' in freq:
            snps_fixed.write('\t'.join(line) + '\n')
    elif line[type_index] == "del":
        del line[type_index]
        del_file.write('\t'.join(line) + '\n')
    elif line[type_index] == "dup":
        del line[type_index]
        dup_file.write('\t'.join(line) + '\n')
    else:
        del line[type_index]
        other_file.write('\t'.join(line) + '\n')

snp_file.close()
snps_fixed.close()
del_file.close()
dup_file.close()
