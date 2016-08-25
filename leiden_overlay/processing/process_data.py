###---###---###---###---###
#   Combines all the raw leiden data with VEP and ExAC data for a given gene
#
#   Assumes that Andrew Hill's scripts have been run to produce a GENE.vep.txt
#   file and a GENE.txt file in the dat folder
#
#   Outputs GENE_final_output.txt and GENE_concise_output.txt in the dat folder
###---###---###---###---###

import re
import math
import sys
import utilities

# cleans up a given hgvs coordinate to standardise it
# based on Andrew Hill's scripts
def convert_hgvs(hgvs_coord):
    hgvs_notation = utilities.remove_times_reported(hgvs_coord)
    hgvs_notation = utilities.correct_hgvs_parentheses(hgvs_notation)
    return hgvs_notation

# returns the band an allele frequency falls in
# used branches because logs are an overkill - CONSIDER SWITCHING THIS TO SWITCHES
def get_band(f):
    if f < 0.000000001:
        return "9"
    elif f < 0.00000001:
        return "8"
    elif f < 0.0000001:
        return "7"
    elif f < 0.000001:
        return "6"
    elif f < 0.00001:
        return "5"
    elif f < 0.0001:
        return "4"
    elif f < 0.001:
        return "3"
    elif f < 0.01:
        return "2"
    elif f < 0.1:
        return "1"
    else:
        return "0"


# get the input gene from terminal arguments
input_gene = sys.argv[1]

# get the already extracted VEP data for the given gene
gene_vep_file = open("../dat/" + input_gene + ".vep.txt")
lines = [line.rstrip('\n').split('\t') for line in gene_vep_file]
gene_vep_file.close()


###-
# Set up Leiden data
###-

# prepare all the extracted leiden data
leiden_file = open("../dat/" + input_gene + ".txt")
leiden_lines = leiden_file.readlines()
leiden_file.close()
leiden_cols = leiden_lines[0].rstrip('\n').split('\t')

# remove the dna_change column name; going to be extracted manually
del leiden_cols[1]

# remove the line of column names
del leiden_lines[0]
leiden_dict = {}

# for each line, pick out the dna_change and assign its properties to it
for line in leiden_lines:
    values = line.rstrip('\n').split('\t')
    dna_change = values[1]
    del values[1] # remove dna_change from the sequenece of values
    leiden_dict[dna_change] = values

# get the already extracted pathogenicity data for the given gene
path_file = open("../dat/" + input_gene + "_pathogenicity.txt")
path_lines = [line.rstrip('\n') for line in path_file.readlines()]
path_file.close()

# assign the pathogenicity level of each listed variant in the pathogenicity
# file to the variant's (standardised) HGVS coordinate
# HGVS coordinate is standardised to match the variant format of the
# existing leiden data retrieved above
path_dict = {}
for line in path_lines:
    pieces = line.split('\t')
    path_dict[convert_hgvs(pieces[0])] = pieces[1]

###-
# Start combining the data together
###-


# remove all the header comments from the VEP file
i = 0 # current line
while lines[i][0][0]=='#':
    i+=1
# i now points to the first line after the header comments - one line under
# the column names
col_names = lines[i-1]
col_names[0] = col_names[0][1:] # get rid of the hashtag in the first col name
rows = lines[i:] # the rest of the lines under the column names are data rows

# open up the final output files
# 'output_file' contains the details of all variants in the database
# 'concise_file' only contains variants with relevant ExAC data
output_file = open("../dat/" + input_gene + "_final_output.txt", "w")
concise_file = open("../dat/" + input_gene + "_concise_output.txt", "w")

# mark important row attribute indices [correspond with columns]
var_name_ind = col_names.index("Uploaded_variation")
location_ind = col_names.index("Location")
extra_index = col_names.index("Extra")

# column names in the output files
first_row_names = ["leiden_reported_variant", "location", "type","raw_allele_frequency", "deduced_new_base", "deduced_allele_frequency", "band", "reported_pathogenicity"] + (leiden_cols)
first_row_out = '\t'.join(first_row_names)+'\n'
concise_file.write(first_row_out)
output_file.write(first_row_out)

var_type = "?"

var_info = {}

for line in rows:
    # get out allele frequency information from the extra ExAC data
    extra_data = line[col_names.index("Extra")].split(';')
    freq_data = next((x.split('=')[1] for x in extra_data if "ExAC_Adj_MAF=" in x), None)
    orig_freq_data = freq_data if freq_data else '-'

    band = "NA"
    formed_base = "-"
    add_to_concise = True

    var_name = line[var_name_ind]
    reported_pathogenicity = path_dict[var_name.split(':')[1]]

    # deduce allele frequency from options - really straightforward with SNPs,
    # much more difficult for ins, del, dup, etc.
    if '>' in var_name and freq_data:
        # the variant is an SNP
        # get the correct variation and its frequency from the ExAC allele freq data
        tmp_freq_data = freq_data.replace(',', ':')
        res_list = tmp_freq_data.split(':')
        new_base = var_name[-1]
        formed_base = new_base
        try:
            main_ind = res_list.index(new_base)
            freq_data = "%.9f"%(float(res_list[main_ind+1]))
            band = get_band(float(freq_data))
        except:
            # we didn't have ExAC data for this particular variation
            freq_data = "No relevant ExAC data"
            add_to_concise = False

    elif freq_data:
        # not an snp so much more difficult to work with
        # here we just choose the most common variant presented in the ExAC database
        tmp_freq_data = freq_data.replace(',', ':')
        res_list = tmp_freq_data.split(':')
        # get the most common one in as the guess...
        possibilities = []
        values = []
        for i in range(0, len(res_list)):
            if i % 2 == 0:
                possibilities.append(res_list[i])
            else:
                values.append(res_list[i])
        poss_count = {x: possibilities.count(x) for x in possibilities}

        # get max poss
        max_count = -1
        max_item = None
        for key in poss_count:
            if poss_count[key] > max_count:
                max_count = poss_count[key]
                max_item = key

        freq_data = "%.9f"%(float(values[possibilities.index(max_item)]))
        band = get_band(float(freq_data))
        formed_base = max_item

    if freq_data == None:
        freq_data = "No ExAC data for variant"
        add_to_concise = False

    if '>' in var_name:
        var_type = "snp"
    elif 'del' in var_name:
        var_type = "del"
    elif 'dup' in var_name:
        var_type = "dup"
    else:
        var_type = "other"


    # add the row to the relevant files
    row_to_add = [line[var_name_ind], line[location_ind], var_type, orig_freq_data, formed_base, freq_data, band, reported_pathogenicity] + (leiden_dict[line[var_name_ind]])
    row_str = '\t'.join(row_to_add) + '\n'
    output_file.write(row_str)
    if add_to_concise:
        concise_file.write(row_str)

output_file.close()
concise_file.close()
