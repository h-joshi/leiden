import math
mat = open("all_data.txt", "w")

genes = open("good_genes.txt", "r")
lines = [x.rstrip('\n') for x in genes.readlines()]
genes.close()

col_names = "Gene\tType\t" + '\t'.join(["< %0.9f"%(math.pow(10, -(k))) for k in range(0, 10, 1)])
mat.write(col_names + '\n')

for gene in lines:
    print gene + "..."
    try:
        f = open("../dat/" + gene + "_table_data.txt", "r")
    except:
        continue
    gene_lines = f.readlines()
    f.close()
    freqs = [x.rstrip('\n').split(',') for x in gene_lines]

    P = [x[0] for x in freqs]
    NP = [x[1] for x in freqs]
    UN = [x[2] for x in freqs]

    mat.write(gene + '\t' + 'Pathogenic\t' + '\t'.join(P) + '\n')
    mat.write(gene + '\t' + 'Not Pathogenic\t' + '\t'.join(NP) + '\n')
    mat.write(gene + '\t' + 'Unknown\t' + '\t'.join(UN) + '\n')
