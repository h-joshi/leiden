"""
GOAL [DONE]: get all data into a workable list from DYSF.txt
    -> open file
    -> get in all data as lines
    -> first row is col names, rest of the rows are values
    -> make a separate list for each row and append them to a container list [set?]

GOAL: try adding in a column for converting coordinates
"""
import pyhgvs
from pygr.seqdb import SequenceFileDB

# set up column names and split up rows
gene_csv = open("../dat/DYSF.txt", 'r')
rows = [line.rstrip('\n').split('\t') for line in gene_csv]
gene_csv.close()
col_names = rows.pop(0)

# add in a column for converted coordinates
for row in rows:
    hgvs_coord = row[col_names.index("dna_change")]
    
