import sys
input_gene = sys.argv[1]

gene_csv = open("../dat/" + input_gene + "_sorted.txt")
lines = [line.rstrip('\n').split('\t') for line in gene_csv]
gene_csv.close()

col_list = lines[0]
type_index = col_list.index("type")
freq_index = col_list.index("deduced_allele_frequency")
del col_list[type_index]
col_names = '\t'.join(col_list)
del lines[0]


f = open("./../dat/" + input_gene + "_snp.txt", "w")
g = open("./../dat/" + input_gene + "_snp_fixed.txt", "w")
f.write(col_names + '\n')
g.write(col_names + '\n')
for line in lines:
    if line[type_index] == "snp":
        freq = line[freq_index]
        del line[type_index]
        f.write('\t'.join(line) + '\n')
        if not 'No' in freq:
            g.write('\t'.join(line) + '\n')
