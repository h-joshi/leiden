import numpy as np
import matplotlib.pyplot as plt
import sys
import math
import scipy #get rid of this? useless - replace later use
import seaborn as sb

sb.set_style("whitegrid")

input_gene = sys.argv[1]

gene_csv = open("../results/" + input_gene + "/" + input_gene + "_full_output.txt")
lines = [line.rstrip('\n').split('\t') for line in gene_csv]
gene_csv.close()

col_list = lines[0]
col_names = '\t'.join(col_list)

del lines[0]
band_index = col_list.index("band")
type_index = col_list.index("type")
name_index = col_list.index("leiden_reported_variant")
pathogenicity_index = col_list.index("reported_pathogenicity")

bands = {}
pathogenics = {}
snp_count = 0

for line in lines:
    if line[type_index] == 'snp':
        try:
            bands[line[band_index]] += 1
            if line[pathogenicity_index] == "Pathogenic" or line[pathogenicity_index] == "Probably pathogenic":
                pathogenics[line[band_index]][0] += 1
            elif line[pathogenicity_index] == "No known pathogenicity" or line[pathogenicity_index] == "Probably not pathogenic":
                pathogenics[line[band_index]][1] += 1
            else:
                pathogenics[line[band_index]][2] += 1
        except:
            bands[line[band_index]] = 1
            pathogenics[line[band_index]] = [0,0,0]
            if line[pathogenicity_index] == "Pathogenic" or line[pathogenicity_index] == "Probably pathogenic":
                pathogenics[line[band_index]][0] += 1
            elif line[pathogenicity_index] == "No known pathogenicity" or line[pathogenicity_index] == "Probably not pathogenic":
                pathogenics[line[band_index]][1] += 1
            else:
                pathogenics[line[band_index]][2] += 1
        snp_count += 1
#print pathogenics
#print bands
if 'NA' in bands:
    snp_count -= bands['NA']
    del bands['NA']
    del pathogenics['NA']

#band_pairs = [(int(k),v) for k,v in bands.items()]
#band_pairs = sorted(band_pairs, key = lambda x: x[0])

bands_dic = {int(k):v for k,v in bands.items()}
pathogenics = {int(k):v for k,v in pathogenics.items()}
x_axis = np.arange(0, 10)

y_axis = [0 for i in range(0, 10)]

threshold_yes = [0 for i in range(0, 10)]
threshold_no = [0 for i in range(0, 10)]
threshold_unknown = [0 for i in range(0,10)]
for key in bands_dic:
    y_axis[key] = bands_dic[key]
    #print pathogenics
    threshold_yes[key] = pathogenics[key][0]
    threshold_no[key] = pathogenics[key][1]
    threshold_unknown[key] = pathogenics[key][2]

#y_axis = []
#for val in band_pairs:
#    x_axis.append(val[0])
#    y_axis.append(val[1])

fig = plt.figure()
ax = fig.add_subplot(111)
ax.xaxis.grid(False)
ax.yaxis.grid(alpha=0.4)
plt.gcf().subplots_adjust(bottom=0.15)

#p1 = plt.bar(x_axis, threshold_yes, color = 'r')
#p2 = plt.bar(x_axis, threshold_no, color = 'y')
#p3 = plt.bar(x_axis, threshold_unknown, color = 'b')
edgecol = "black"
rect_unknown = ax.bar(x_axis, threshold_unknown, color='b', align='center', edgecolor = edgecol)
rect_no = ax.bar(x_axis, threshold_no, bottom=threshold_unknown, color='y', align='center', edgecolor = edgecol)
rect_yes = ax.bar(x_axis, threshold_yes, bottom=[threshold_no[i] + threshold_unknown[i] for i in range(0, 10)], color='r', align='center', edgecolor = edgecol)

#plt.gca().set_position((.1, .3, .8, .6))
ax.set_ylabel("# of Variants")
ax.set_xlabel("Frequency Range") # PUT IN A KEY
ax.set_yticks(scipy.arange(0, max(y_axis)+5, 2))
ax.set_xticks(np.arange(0, 10, 1))
ax.set_xticklabels(['< ' + str(math.pow(10, -(k))) for k in x_axis], rotation=25, fontsize=8)
ax.set_title("%s SNP Band Count"%(input_gene))


#ax.suplots_adjust(left=0.09, bottom=0.20)
legend1 = plt.legend((rect_yes, rect_no, rect_unknown), ("Pathogenic/probably pathogenic", "Not pathogenic/probably not pathogenic", "Unknown pathogenicity or mixed reports"), fontsize='x-small', loc=1)


#bandstr = "\n'Band' measures percentage allele frequency within the ExAC sample population.\nBand 0: 10^-1 to 1\n"
#for i in range(1, 9):
#    bandstr+="Band %d: 10^-%d to 10^-%d\n"%(i, i+1, i)

#plt.figtext(.02, .02, bandstr, fontsize='x-small')
#plt.figtext(0.2, 0.2, "'Band' measures the percentage allele frequency within the ExAC sample population.\nA variant is in Band i if its allele frequency is between 10^-(i+1) and 10^-i.\nA variant in a higher band hence implies lower allele frequency.", fontsize="x-small")
#plt.setp(ax.set_xticklabels(x_axis))

### UNCOMMENT IF YOU WANT THE BAND STUFF...
#plt.subplots_adjust(bottom=0.20)
#plt.figtext(0.05, 0.02, "'Band' measures the percentage allele frequency within the ExAC sample population.\nA variant is in Band k if its allele frequency is between 10^-(k+1) and 10^(-k)\nA variant in a higher band hence implies lower allele frequency.")
###

fig.savefig("../results/" + input_gene + "/" + input_gene + "_chart.png")
#plt.show()


# THROW IN NOW THE NEW MATRIX STUFF
table_data = open("../dat/" + input_gene + "_table_data.txt", "w")
for i in range(0, 10):
    if i in pathogenics:
        table_data.write(','.join([str(x) for x in pathogenics[i]]) + '\n')
    else:
        table_data.write('0,0,0\n')
table_data.close()
