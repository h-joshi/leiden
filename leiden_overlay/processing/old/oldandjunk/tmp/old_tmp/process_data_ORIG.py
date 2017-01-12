import re

input_gene = "DYSF"

gene_vep_file = open("../dat/" + input_gene + ".vep.txt")
lines = [line.rstrip('\n').split('\t') for line in gene_vep_file]
gene_vep_file.close()

####
# prepare all leiden data
leiden_file = open("../dat/" + input_gene + ".txt")
leiden_lines = leiden_file.readlines()
leiden_file.close()
leiden_cols = leiden_lines[0].rstrip('\n').split('\t')
del leiden_cols[1]
del leiden_lines[0]
leiden_dict = {}

for line in leiden_lines:
    values = line.rstrip('\n').split('\t')
    d_change = values[1]
    del values[1]
    leiden_dict[d_change] = values

####

i = 0
while lines[i][0][0]=='#':
    i+=1

col_names = lines[i-1]
col_names[0] = col_names[0][1:]
rows = lines[i:]
#print col_names
extra_index = col_names.index("Extra")

#print col_names

output_file = open("../dat/" + input_gene + "_final_output.txt", "w")
concise_file = open("../dat/" + input_gene + "_concise_output.txt", "w")
var_name_ind = col_names.index("Uploaded_variation")
location_ind = col_names.index("Location")
conseq_ind = col_names.index("Consequence")

var_type = "?"

first_row_names = ["leiden_reported_variant", "location", "type", "consequence", "raw_allele_frequency", "deduced_new_base", "deduced_allele_frequency"] + (leiden_cols)
first_row_out = '\t'.join(first_row_names)+'\n'

concise_file.write(first_row_out)
output_file.write(first_row_out)

var_info = {}

for line in rows:
    extra_data = line[col_names.index("Extra")].split(';')
    freq_data = next((x.split('=')[1] for x in extra_data if "ExAC_Adj_MAF=" in x), None)
    orig_freq_data = freq_data if freq_data else '-'

    formed_base = "-"

    add_to_concise = True
    #for SNPs this always works because we know what it's going to change to???
    #get the actual change from freq_data - TODO: CHECK THIS WITH HIMANSHU
    var_name = line[var_name_ind]


    if '>' in var_name and freq_data:
        tmp_freq_data = freq_data.replace(',', ':')
        res_list = tmp_freq_data.split(':')
        # get the correct variant
        new_base = var_name[-1]
        formed_base = new_base
        try:
            main_ind = res_list.index(new_base)
            freq_data = "%.9f"%(float(res_list[main_ind+1]))
        except:
            freq_data = "No relevant ExAC data"
            add_to_concise = False
    elif freq_data:
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
        formed_base = max_item

        """poss_count = {}
        for x in possibilities:
            try:
                poss_count[x] += 1
            except:
                poss_count[x] = 1"""

    #print line[var_name_ind], line[location_ind], line[conseq_ind], freq_data
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

    row_to_add = [line[var_name_ind], line[location_ind], var_type, line[conseq_ind], orig_freq_data, formed_base, freq_data] + (leiden_dict[line[var_name_ind]])
    row_str = '\t'.join(row_to_add) + '\n'
    #row_to_add = ("%s\t%s\t%s\t%s\t%s\t%s\n")%(line[var_name_ind], line[location_ind], line[conseq_ind], orig_freq_data, formed_base, freq_data)
    output_file.write(row_str)
    if add_to_concise:
        concise_file.write(row_str)
    #output_file.write("%s\t%s\t%s\t%s\t%s\t%s

output_file.close()
concise_file.close()
