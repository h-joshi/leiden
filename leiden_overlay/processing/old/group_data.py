###---###---###---###---###
#   Groups all the variants for a given gene based on which frequency band
#   they fall into (on a logarithmic scale) - the buckets are < 1e-9, < 1e-8,
#   ..., < 1.0.
#
#   Requires ./run_script to have been run on the gene at least once before, and
#   the dat folder to not have been cleaned out afterwards.
#
#   Outputs the grouped data into GENE_grouped.txt in the dat folder.
###---###---###---###---###

import sys
import math

# get the gene name from the terminal argument
input_gene = sys.argv[1]

# input files - sorted by ExAC frequency [done in a previous script]
gene_csv = open("../dat/" + input_gene + "_snp_fixed_nodup.txt")
lines = [line.rstrip('\n').split('\t') for line in gene_csv]
gene_csv.close()

# output file
result = open("../dat/" + input_gene + "_grouped.txt", "w") # output file

# get indices of important columns in the table
freq_ind = lines[0].index("deduced_allele_frequency")
path_ind = lines[0].index("reported_pathogenicity")
genom_ind = lines[0].index("location")
band_ind = lines[0].index("band")

col_names = ["freq_range", "variant", "genomic_coord", "exac_allele_freq", "reported_leiden_pathogenicity"]
result.write("\t".join(col_names) + '\n')

# write in the row data for each variant
for j in range(1,len(lines)):
    freq_cat = "< " + "%.9f"%(math.pow(10, -int(lines[j][band_ind])))
    final_row = [freq_cat, lines[j][0], lines[j][genom_ind], "%.9f"%(float(lines[j][freq_ind])), lines[j][path_ind]]
    result.write("\t".join(final_row) + '\n')

result.close()
