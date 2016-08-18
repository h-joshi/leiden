import numpy as np
import matplotlib.pyplot as plt
input_gene = "DYSF"

gene_csv = open("../results/" + input_gene + "/" + input_gene + "_full_output.txt")
lines = [line.rstrip('\n').split('\t') for line in gene_csv]
gene_csv.close()

col_list = lines[0]
col_names = '\t'.join(col_list)

del lines[0]
band_index = col_list.index("band")
type_index = col_list.index("type")

bands = {}
snp_count = 0
for line in lines:
    if line[type_index] == 'snp':
        try:
            bands[line[band_index]] += 1
        except:
            bands[line[band_index]] = 1
        snp_count += 1

snp_count -= bands['NA']
del bands['NA']

band_pairs = [(int(k),v) for k,v in bands.items()]
band_pairs = sorted(band_pairs, key = lambda x: x[0])

x_axis = []
y_axis = []
for val in band_pairs:
    x_axis.append(val[0])
    y_axis.append(val[1])

fig = plt.figure()
ax = fig.add_subplot(111)
width = 0.35

rects=ax.bar(np.arange(len(x_axis)), y_axis)
ax.set_ylabel("Frequency")
ax.set_xlabel("Band Number")
ax.set_title("%s SNP Band Count"%(input_gene))
plt.setp(ax.set_xticklabels(x_axis))
plt.show()
