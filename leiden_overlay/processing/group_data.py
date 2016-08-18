input_gene = "DYSF"

gene_csv = open("../dat/" + input_gene + "_snp_fixed_nodup.txt")
lines = [line.rstrip('\n').split('\t') for line in gene_csv]
gene_csv.close()

result = open("../dat/" + input_gene + "_grouped.txt", "w")
freq_ind = lines[0].index("deduced_allele_frequency")
j = 1
for i in range(9, -1, -1):
    ten_pow = 10 ** (-i)
    count = 0
    result.write("< %0.9f\n"%(ten_pow))
    result_part = ""
    while j < len(lines) and float(lines[j][freq_ind]) < ten_pow:
        result_part += ("---> %s\t%0.9f\n"%(lines[j][0], float(lines[j][freq_ind])))
        count += 1
        j+=1
    result_part += ('\n')
    result.write("TOTAL: %d\n"%(count))
    result.write(result_part)

result.close()
