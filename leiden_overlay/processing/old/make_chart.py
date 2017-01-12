###---###---###---###---###
#   Makes a chart for a given gene that displays the spread of the variants based
#   on ExAC frequency, with the variants marked based on pathogenicity (whether
#   they are pathogenic, non-pathogenic, or unknown).
#
#   The script also outputs the table data for the gene that will be used to
#   create the Leiden matrix. This is for efficiency purposes, as they both need
#   to calculate similar data with regards to pathogenicity, etc.
#
#   The script requires ./run_script to have been run on this particular gene
#   at least once beforehand, and the data to not have been deleted from its
#   results folder or from the dat folder.
#
#   Outputs GENE_chart.png in the gene's results folder. Also outputs
#   GENE_table_data.txt in the dat folder.
###---###---###---###---###

import numpy as np
import matplotlib.pyplot as plt
import sys
import math
import scipy # possibly remove this
import seaborn as sb

# set chart style using seaborn
sb.set_style("whitegrid")

# get the gene name
input_gene = sys.argv[1]

# get the gene's data
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

# get the count for each type of pathogenicity (essentially yes, no, and unknown)
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

# remove those with no ExAC data (marked as NA in the table)
if 'NA' in bands:
    snp_count -= bands['NA']
    del bands['NA']
    del pathogenics['NA']

bands_dic = {int(k):v for k,v in bands.items()}
pathogenics = {int(k):v for k,v in pathogenics.items()}

####----
# Create the stacked chart
####----

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

fig = plt.figure()
ax = fig.add_subplot(111)
ax.xaxis.grid(False)
ax.yaxis.grid(alpha=0.4)
plt.gcf().subplots_adjust(bottom=0.15)

edgecol = "black"
rect_unknown = ax.bar(x_axis, threshold_unknown, color='b', align='center', edgecolor = edgecol)
rect_no = ax.bar(x_axis, threshold_no, bottom=threshold_unknown, color='y', align='center', edgecolor = edgecol)
rect_yes = ax.bar(x_axis, threshold_yes, bottom=[threshold_no[i] + threshold_unknown[i] for i in range(0, 10)], color='r', align='center', edgecolor = edgecol)

ax.set_ylabel("# of Variants")
ax.set_xlabel("Frequency Range") # PUT IN A KEY
ax.set_yticks(scipy.arange(0, max(y_axis)+5, 2))
ax.set_xticks(np.arange(0, 10, 1))
ax.set_xticklabels(['< ' + str(math.pow(10, -(k))) for k in x_axis], rotation=25, fontsize=8)
ax.set_title("%s SNP Band Count"%(input_gene))

legend1 = plt.legend((rect_yes, rect_no, rect_unknown), ("Pathogenic/probably pathogenic", "Not pathogenic/probably not pathogenic", "Unknown pathogenicity or mixed reports"), fontsize='x-small', loc=1)

# save the chart
fig.savefig("../results/" + input_gene + "/" + input_gene + "_chart.png")
#plt.show()

####----
# Matrix-related data output
####----

# Output the pathogenicity-related table data for the Leiden matrix into its own file
table_data = open("../dat/" + input_gene + "_table_data.txt", "w")
for i in range(0, 10):
    if i in pathogenics:
        table_data.write(','.join([str(x) for x in pathogenics[i]]) + '\n')
    else:
        table_data.write('0,0,0\n')
table_data.close()
