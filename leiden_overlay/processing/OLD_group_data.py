import sys
input_gene = sys.argv[1]

# input files - we assume they are sorted by frequency
gene_csv = open("../dat/" + input_gene + "_snp_fixed_nodup.txt")
lines = [line.rstrip('\n').split('\t') for line in gene_csv]
gene_csv.close()

result = open("../dat/" + input_gene + "_grouped.txt", "w") # output file

# get indices of important columns in the table
freq_ind = lines[0].index("deduced_allele_frequency")
path_ind = lines[0].index("reported_pathogenicity")

j = 1
for i in range(9, -1, -1):
    ten_pow = 10 ** (-i)
    count = 0
    result.write("< %0.9f\n"%(ten_pow))
    result_part = ""

    # keep writing the next gene to this band level until we reach the next band
    # or we hit the last variant
    # written info is ---> variant_name pathogenicity   allele frequency
    while j < len(lines) and float(lines[j][freq_ind]) < ten_pow:
        result_part += ("---> %s\t%s\t%0.9f\n"%(lines[j][0], lines[j][path_ind], float(lines[j][freq_ind])))
        count += 1
        j+=1
    result_part += ('\n')
    result.write("TOTAL: %d\n"%(count)) # total number of variants in this band
    result.write(result_part)

result.close()
