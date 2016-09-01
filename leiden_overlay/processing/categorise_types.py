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


snp_file = open("./../dat/" + input_gene + "_snp.txt", "w")
snps_fixed = open("./../dat/" + input_gene + "_snp_fixed.txt", "w")

del_file = open("./../dat/" + input_gene + "_del.txt", "w")
dup_file = open("./../dat/" + input_gene + "_dup.txt", "w")

snp_file.write(col_names + '\n')
snps_fixed.write(col_names + '\n')
del_file.write(col_names + '\n')
dup_file.write(col_names + '\n')

for line in lines:
    if line[type_index] == "snp":
        freq = line[freq_index]
        del line[type_index]
        snp_file.write('\t'.join(line) + '\n')
        if not 'No' in freq:
            snps_fixed.write('\t'.join(line) + '\n')
    elif line[type_index] == "del":
        del line[type_index]
        del_file.write('\t'.join(line) + '\n')
    elif line[type_index] == "dup":
        del line[type_index]
        dup_file.write('\t'.join(line) + '\n')
    else:
        print line[0] + " could not be categorised..."

#PUT THE FILES IN A DICT INSTEAD
snp_file.close()
snps_fixed.close()
del_file.close()
dup_file.close()
