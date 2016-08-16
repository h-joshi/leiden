input_gene = "DYSF"

gene_csv = open("../dat/" + input_gene + "_concise_output.txt")
lines = [line.rstrip('\n').split('\t') for line in gene_csv]
gene_csv.close()

col_list = lines[0]
col_names = '\t'.join(col_list)
del lines[0]

freq_index = col_list.index("deduced_allele_frequency")

results = sorted(lines, key = lambda x: float(x[freq_index]))
results_concat = [('\t'.join(line)) for line in results]
output = col_names + '\n' + '\n'.join(results_concat)

with open("./../dat/" + input_gene + "_sorted.txt", "w") as f:
    f.write(output)