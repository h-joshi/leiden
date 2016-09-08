import sys
import math
input_gene = sys.argv[1]

# input files - we assume they are sorted by frequency
gene_csv = open("../dat/" + input_gene + "_snp_fixed_nodup.txt")
lines = [line.rstrip('\n').split('\t') for line in gene_csv]
gene_csv.close()

result = open("../dat/" + input_gene + "_grouped.txt", "w") # output file

# get indices of important columns in the table
freq_ind = lines[0].index("deduced_allele_frequency")
path_ind = lines[0].index("reported_pathogenicity")
genom_ind = lines[0].index("location")
band_ind = lines[0].index("band")

col_names = ["freq_range", "variant", "genomic_coord", "exac_allele_freq", "reported_leiden_pathogenicity"]
result.write("\t".join(col_names) + '\n')

for j in range(1,len(lines)):
    freq_cat = "< " + "%.9f"%(math.pow(10, -int(lines[j][band_ind])))
    result_sol = [freq_cat, lines[j][0], lines[j][genom_ind], "%.9f"%(float(lines[j][freq_ind])), lines[j][path_ind]]
    result.write("\t".join(result_sol) + '\n')

result.close()
