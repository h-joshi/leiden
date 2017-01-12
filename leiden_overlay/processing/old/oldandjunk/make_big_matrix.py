

import math
new_mat = open("full_matrix.txt", "w")
genes = open("good_genes.txt", "r")
lines = [x.rstrip('\n') for x in genes.readlines()]
genes.close()

with open("resc/inheritance_patterns.txt", "r") as f:
    patterns = [x.rstrip('\n').rstrip('\r').split('\t') for x in f.readlines()]
col_names = patterns.pop(0)

gene_ind = col_names.index("Gene")
ar_ind = col_names.index("AR")
ad_ind = col_names.index("AD")
xl_ind = col_names.index("XL")
is_ind = col_names.index("IS")

pat_dict = {pat[gene_ind]:pat[ar_ind:is_ind+1] for pat in patterns}
#print pat_dict["DYSF"]
powers = ["< %0.9f"%(math.pow(10, -(k))) for k in range(0, 10, 1)]
#new_mat.write("\t".join(["Gene", "inher_pat", "Type", "Freq_Range", "Count"]) + '\n')
new_mat.write('\t'.join(["gene", "variant", "genomic_coord", "exac_freq", "type", "inher_pat"]) + '\n')
for gene in lines:
    print gene + "..."
    # get inheritance pattern
    if gene in pat_dict:
        vals = pat_dict[gene]
        result = []
        if vals[0] == "Y":
            result.append("AR")
        if vals[1] == "Y":
            result.append("AD")
        if vals[2] == "Y":
            result.append("XL")
        if vals[3] == "Y":
            result.append("IS")
        if len(result) == 0:
            ip = "none"
        else:
            ip = ','.join(result)

    else:
        ip = "-"

    try:
        f = open("../dat/" + gene + "_table_data.txt", "r")
        g = open("../dat/" + input_gene + "_snp_fixed_nodup.txt")
    except:
        continue
    gene_lines = f.readlines()
    snp_lines = [line.rstrip('\n').split('\t') for line in g]

    f.close()
    freqs = [x.rstrip('\n').split(',') for x in gene_lines]

    P = [x[0] for x in freqs]
    NP = [x[1] for x in freqs]
    UN = [x[2] for x in freqs]

    for i in range(len(P)):
        item = str(P[i])
        new_mat.write(gene + '\t' + ip + '\t' + 'Pathogenic\t' + powers[i] + '\t'+ item + '\n')
    for i in range(len(P)):
        item = str(NP[i])
        new_mat.write(gene + '\t' + ip + '\t' + 'Not Pathogenic\t' + powers[i] + '\t'+ item + '\n')
    for i in range(len(P)):
        item = str(UN[i])
        new_mat.write(gene + '\t' + ip + '\t' + 'Unknown\t' + powers[i] + '\t'+ item + '\n')


    mat.write(gene + '\t' + ip + '\t' + 'Pathogenic\t' + '\t'.join(P) + '\n')
    mat.write(gene + '\t' + ip + '\t' + 'Not Pathogenic\t' + '\t'.join(NP) + '\n')
    mat.write(gene + '\t' + ip + '\t' + 'Unknown\t' + '\t'.join(UN) + '\n')

mat.close()
new_mat.close()
