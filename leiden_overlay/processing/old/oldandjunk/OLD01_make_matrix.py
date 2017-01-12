import math
mat = open("all_data.txt", "w")

genes = open("good_genes.txt", "r")
lines = [x.rstrip('\n') for x in genes.readlines()]
genes.close()

col_names = "Gene\t" + '\t'.join(['> ' + str(math.pow(10, -(k+1))) for k in range(0, 10, 1)])
mat.write(col_names + '\n')

for gene in lines:
    print gene + "..."
    try:
        f = open("../dat/" + gene + "_table_data.txt", "r")
    except:
        continue
    mat.write(gene + '\t' + '\t'.join([x.rstrip('\n') for x in f.readlines()]) + '\n')
    f.close()
