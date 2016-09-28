import numpy as np
import matplotlib.pyplot as plt
import sys
import math
import scipy #get rid of this? useless - replace later use

input_gene = sys.argv[1]

gene_csv = open("../results/" + input_gene + "/" + input_gene + "_full_output.txt")
mat_dat = open("mat_dat/ALL_"+input_gene+".mat", "w")
lines = [line.rstrip('\n').split('\t') for line in gene_csv]
gene_csv.close()


with open("resc/inheritance_patterns.txt", "r") as f:
    patterns = [x.rstrip('\n').rstrip('\r').split('\t') for x in f.readlines()]
col_names = patterns.pop(0)

gene_ind = col_names.index("Gene")
ar_ind = col_names.index("AR")
ad_ind = col_names.index("AD")
xl_ind = col_names.index("XL")
is_ind = col_names.index("IS")

pat_dict = {pat[gene_ind]:pat[ar_ind:is_ind+1] for pat in patterns}

if input_gene in pat_dict:
    vals = pat_dict[input_gene]
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


col_list = lines[0]
col_names = '\t'.join(col_list)

columns = ["gene", "variant", "genomic_coord", "exac_freq", "type", "inher_pat"]
mat_dat.write('\t'.join(columns) + '\n')

del lines[0]
band_index = col_list.index("band")
type_index = col_list.index("type")
name_index = col_list.index("leiden_reported_variant")
pathogenicity_index = col_list.index("reported_pathogenicity")
location_index = col_list.index("location")
al_freq_index = col_list.index("deduced_allele_frequency")

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
        if 'No' in line[al_freq_index]:
            ex_freq = '-'
        else:
            ex_freq = line[al_freq_index]
        mat_dat.write("\t".join([input_gene, line[name_index], line[location_index], ex_freq, line[pathogenicity_index], ip]) + '\n')
        snp_count += 1

#band_pairs = [(int(k),v) for k,v in bands.items()]
#band_pairs = sorted(band_pairs, key = lambda x: x[0])

mat_dat.close()
