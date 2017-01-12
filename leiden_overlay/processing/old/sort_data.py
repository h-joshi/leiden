###---###---###---###---###
#   Sorts the data in the "GENE_concise_output.txt" table with respect to
#   the ExAC frequency column.
#
#   Requires that the GENE_concise_output.txt file actually exists. This file
#   is produced by the process_data.py script, and so that script must be run first.
#
#   Outputs GENE_sorted.txt in the dat folder
###---###---###---###---###

import sys

# get the gene_name from the terminal input
input_gene = sys.argv[1]

# open up the table
gene_csv = open("../dat/" + input_gene + "_concise_output.txt")
lines = [line.rstrip('\n').split('\t') for line in gene_csv]
gene_csv.close()

col_list = lines[0]
col_names = '\t'.join(col_list)

# remove the column names from the table before sorting
del lines[0]

# sort the list and make the resulting file
freq_index = col_list.index("deduced_allele_frequency")
results = sorted(lines, key = lambda x: float(x[freq_index]))
results_concat = [('\t'.join(line)) for line in results]
output = col_names + '\n' + '\n'.join(results_concat)

# write the result file into the dat folder
with open("./../dat/" + input_gene + "_sorted.txt", "w") as f:
    f.write(output)
