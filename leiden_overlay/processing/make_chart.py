import numpy as np
import matplotlib.pyplot as plt
import sys
import scipy #get rid of this? useless - replace later use
input_gene = sys.argv[1]

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

#band_pairs = [(int(k),v) for k,v in bands.items()]
#band_pairs = sorted(band_pairs, key = lambda x: x[0])

bands_dic = {int(k):v for k,v in bands.items()}
x_axis = np.arange(0, 10)
y_axis = [0 for i in range(0, 10)]

for key in bands_dic:
    y_axis[key] = bands_dic[key]

#y_axis = []
#for val in band_pairs:
#    x_axis.append(val[0])
#    y_axis.append(val[1])

fig = plt.figure()
ax = fig.add_subplot(111)

rects=ax.bar(x_axis, y_axis, align='center')
ax.set_ylabel("Frequency")
ax.set_xlabel("Band Number")
ax.set_yticks(scipy.arange(0, max(y_axis)+5, 2))
ax.set_xticks(np.arange(0, 10, 1))
ax.set_title("%s SNP Band Count"%(input_gene))

#plt.setp(ax.set_xticklabels(x_axis))

fig.savefig("../results/" + input_gene + "/" + input_gene + "_chart.png")
