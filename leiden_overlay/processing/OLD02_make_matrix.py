import math
mat = open("all_data.txt", "w")

genes = open("good_genes.txt", "r")
lines = [x.rstrip('\n') for x in genes.readlines()]
genes.close()

band_names = "\t" + '\t\t\t'.join(['> ' + str(math.pow(10, -(k+1))) for k in range(0, 10, 1)])
col_names = 'Gene\t'
for i in range(0, 10):
    col_names += "Pathogenic\tNot Pathogenic\tUnknown\t"
mat.write(band_names + '\n' + col_names + '\n')

for gene in lines:
    print gene + "..."
    try:
        f = open("../dat/" + gene + "_table_data.txt", "r")
    except:
        continue
    mat.write(gene + '\t' + '\t'.join(['\t'.join(x.rstrip('\n').split(',')) for x in f.readlines()]) + '\n')
    f.close()
