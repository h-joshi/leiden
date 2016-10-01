###---###---###---###---###
#   Scrapes the pathogenicity data for each variant of a given gene from Leiden
#
#   Stand-alone - does not assume another script has been run before.
#
#   Outputs GENE_pathogenicity.txt in the dat folder
###---###---###---###---###

from bs4 import BeautifulSoup
import urllib
import unicodedata
import math
import sys

# converts unicode string to ascii
def to_ascii(string):
    return unicodedata.normalize('NFKD', string).encode('ascii', 'ignore')

print "Processing overall table..."

# read the given gene name from the terminal
gene_name = sys.argv[1]

# open the relevant Leiden page
r = urllib.urlopen('http://www.dmd.nl/nmdb2/variants.php?select_db='+ gene_name +'&action=view_all').read()
soup = BeautifulSoup(r, "html.parser")

# total number of variants recorded
num_entries = int(soup.find(lambda tag: tag.get('class') == [u'S11']).get_text().split(' ')[0])
# total number of variants displayed per page - max is 1000 on Leiden; can be some (fixed) lower values
num_per_page = 1000
# deduce the number of pages to search
num_pages = int(math.ceil(num_entries*1.0/num_per_page*1.0))

# converts the Leiden format pathogenicity into human-readable form
def convert_path(path):
    if path == "+":
        return "Pathogenic"
    elif path == "+?":
        return "Probably pathogenic"
    elif path == "-":
        return "No known pathogenicity"
    elif path == "-?":
        return "Probably not pathogenic"
    elif path == "?":
        return "Unknown"
    else:
        return "Error"

variant_dict = {}

total_variants = 0
for page_number in range(1, num_pages+1):
    print "Processing page %d of %d..."%(page_number, num_pages)

    # construct the page url for the current page and open it
    # example format (no db manually selected): http://www.dmd.nl/nmdb2/variants.php?action=view_all&limit=100&order=Variant%2FDNA%2CASC&page=1
    page_url = 'http://www.dmd.nl/nmdb2/variants.php?select_db='+gene_name+ "&action=view_all&limit=1000&order=Variant%%2FDNA%%2CASC&page=" + str(page_number)
    curr_page_soup = BeautifulSoup(urllib.urlopen(page_url).read(), "html.parser")

    # get each row from the page
    variant_table = curr_page_soup.find_all(lambda tag: tag.name == "table" and tag.get('class') == [u'data'])[1]
    variant_details = variant_table.find_all('tr')
    del variant_details[0] # get rid of the column names

    for row in variant_details:
        # get the pathogenicities and variant names
        row_details = row.find_all('td')
        pathogenicity =  convert_path(row_details[0].get_text().split('/')[0])
        try:
            dna_change = row_details[2].find(lambda tag: tag.name == 'a' and tag.get('class') == [u'data']).get_text()
        except:
            # Some genes have rearranged columns... see BIN1 vs. DYSF [and most others]
            dna_change = row_details[3].find(lambda tag: tag.name == 'a' and tag.get('class') == [u'data']).get_text()

        if (dna_change in variant_dict) and variant_dict[dna_change] != pathogenicity:
            variant_dict[dna_change] = "Mixed reported pathogenicity"
        elif dna_change not in variant_dict:
            variant_dict[dna_change] = pathogenicity
            total_variants += 1

# write results to a file
out_file = open("./../dat/" + gene_name + "_pathogenicity.txt", "w")
for key in variant_dict:
    out_file.write(key + "\t" + variant_dict[key] + "\n")
out_file.close()

print "%d variant pathogenicities written to file."%(total_variants)
