###---###---###---###---###
#   Makes a final table for a specific given gene that puts together all the
#   necessary information needed to create the final Leiden Matrix later on.
#
#   Run this script only using the encompassing "finish_mat.sh" script, which also
#   completes the data processing to produce the final matrix in a tab-delimited
#   format.
#
#   Outputs ALL_GENE.mat into the mat_dat folder in the current directory.
###---###---###---###---###

import sys

# get the current gene name
input_gene = sys.argv[1]

# open all the gene's relevant data
gene_csv = open("../results/" + input_gene + "/" + input_gene + "_full_output.txt")
lines = [line.rstrip('\n').split('\t') for line in gene_csv]
gene_csv.close()

mat_dat = open("mat_dat/ALL_"+input_gene+".mat", "w")

# open inheritance pattern information
with open("resc/inheritance_patterns.txt", "r") as f:
    patterns = [x.rstrip('\n').rstrip('\r').split('\t') for x in f.readlines()]
col_names = patterns.pop(0)

gene_ind = col_names.index("Gene")
ar_ind = col_names.index("AR")
ad_ind = col_names.index("AD")
xl_ind = col_names.index("XL")
is_ind = col_names.index("IS")

pat_dict = {pat[gene_ind]:pat[ar_ind:is_ind+1] for pat in patterns}

# map the input gene to its inheritance pattern in the OMIM dataset
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

columns = ["gene", "variant", "genomic_coord", "protein_change", "exac_freq", "type", "inher_pat", "occurrence_factor"]
mat_dat.write('\t'.join(columns) + '\n')

del lines[0]
band_index = col_list.index("band")
type_index = col_list.index("type")
name_index = col_list.index("leiden_reported_variant")
protein_change_index = col_list.index("protein_change")
pathogenicity_index = col_list.index("reported_pathogenicity")
location_index = col_list.index("location")
al_freq_index = col_list.index("deduced_allele_frequency")

bands = {}
pathogenics = {}
snp_count = 0

# write each row to the table appropriately
for line in lines:
    # we only want SNPs in the final matrix for now
    if line[type_index] == 'snp':
        # don't use this at the moment, but uncomment if needed
        """
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
        """
        # check if it has ExAC data or not
        if 'No' in line[al_freq_index]:
            ex_freq = '-'
        else:
            ex_freq = line[al_freq_index]

        # find occurrence factor
        factor = ""
        if ex_freq == "-":
            factor = "-"
        else:
            int_freq = lineal_freq_index
            if input_gene == "DMD":
                factor = str(ex_freq / (1.0/3500))
            elif ip == "AD":
                factor = str(ex_freq / (1.0/5000))
            elif ip == "AR":
                factor = str(ex_freq / (1.0/100))
            elif ip == "AR,AD":
                factor = str(ex_freq / (1.0/100)) + ", " + str(ex_freq / (1/5000))
            elif ip == "XL":
                factor = str(ex_freq / (1.0/10000))
            else:
                factor = "?"

        # write the row to the table
        mat_dat.write("\t".join([input_gene, line[name_index], line[location_index], line[protein_change_index], ex_freq, line[pathogenicity_index], ip, factor]) + '\n')
        snp_count += 1

mat_dat.close()
