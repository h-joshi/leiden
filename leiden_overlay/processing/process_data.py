import re

input_gene = "DYSF"

gene_vep_file = open("../dat/" + input_gene + "_VEP_FINAL.txt")
lines = [line.rstrip('\n').split('\t') for line in gene_vep_file]
gene_vep_file.close()

i = 0
while lines[i][0][0]=='#':
    i+=1

col_names = lines[i-1]
col_names[0] = col_names[0][1:]
rows = lines[i:]
print col_names
extra_index = col_names.index("Extra")

output_file = open("../dat/" + input_gene + "_final_output.txt", "w")
var_name_ind = col_names.index("Uploaded_variation")
location_ind = col_names.index("Location")
conseq_ind = col_names.index("Consequence")

first_row_out = ("%s\t%s\t%s\t%s\n")%("Uploaded_variation", "Location", "Consequence", "Result")
output_file.write(first_row_out)
for line in rows:
    extra_data = line[col_names.index("Extra")].split(';')
    freq_data = next((x for x in extra_data if "ExAC_Adj_MAF=" in x), None)
    print line[var_name_ind], line[location_ind], line[conseq_ind], freq_data
    if freq_data == None:
        freq_data = "NULL"
    row_to_add = ("%s\t%s\t%s\t%s\n")%(line[var_name_ind], line[location_ind], line[conseq_ind], freq_data)
    output_file.write(row_to_add)
    #output_file.write("%s\t%s\t%s\t%s\t%s\t%s

output_file.close()
