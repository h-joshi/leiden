"""
GOAL [DONE]: get all data into a workable list from DYSF.txt
    -> open file
    -> get in all data as lines
    -> first row is col names, rest of the rows are values
    -> make a separate list for each row and append them to a container list [set?]

GOAL: try adding in a column for converting coordinates
"""
import pyhgvs
import pyhgvs.utils
from pygr.seqdb import SequenceFileDB
import re

input_gene = "DYSF"
# set up column names and split up rows
print "Importing data..."
gene_csv = open("../dat/" + input_gene + ".txt", 'r')
rows = [line.rstrip('\n').split('\t') for line in gene_csv]
gene_csv.close()
col_names = rows.pop(0)

print "Setting up transcript/genome..."
# set up genome and reference paths - based on Andrew's scripts
genome_path = "resources/hg19.fa"
refseq_path = "resources/genes.refGene"

# read RefSeq transcripts into a python dict - based on Andrew's scripts
genome = SequenceFileDB(genome_path)
with open(refseq_path) as ref_file:
	transcript = pyhgvs.utils.read_transcripts(ref_file) #this takes a while

# add in a column for converted coordinates
# HGVS change based on Andrew's scripts
print "Translating coordinates..."
col_names.append('chromosome_number')
col_names.append('position')
col_names.append('ref_seq')
col_names.append('alt_seq')
#col_names.append('change') #CHECK THIS? IS REFSEQ>ALTSEQ REALLY THE CHANGE?
def get_transcript(name):
	return transcript.get(name)

bed_file = open("../dat/" + input_gene + ".BED", "w")

for row in rows:
    hgvs_coord = str(row[col_names.index("dna_change")])
    try:
        chrom_num, pos, ref_seq, alt_seq = pyhgvs.parse_hgvs_name(hgvs_coord, genome, get_transcript=get_transcript)
        # group(1) means get the first paranthesised match
        chrom_num = re.match('chr(.+)', chrom_num).group(1)
        row.extend([chrom_num, str(pos), ref_seq, alt_seq])

        # add to the bed file
        bed_out = "%s\t%s\t%s\n"%(chrom_num, pos, str(int(pos) + len(ref_seq) - 1))
        bed_file.write(bed_out)

    except:
		# couldn't translate this
		row.extend(['-', '-', '-', '-'])

# copy the output to a new file
output_file = open("../dat/" + input_gene + "_extended.txt", "w")
output_file.write('\t'.join(col_names))
output_file.write('\n')
for row in rows:
   output_file.write('\t'.join(row))
   output_file.write('\n')
output_file.close()



print "Processing done!"
