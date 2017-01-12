###---###---###---###---###
#   Scrapes the full list of genes from the Leiden website.
#
#   Stand-alone - does not assume another script has been run before.
#
#   Outputs gene_list.txt in the dat folder
###---###---###---###---###

from bs4 import BeautifulSoup
import urllib

# open the Leiden page that switches been gene databases - displays them all
# on a single page
r = urllib.urlopen("http://www.dmd.nl/nmdb2/home.php?action=switch_db").read()
soup = BeautifulSoup(r, "html.parser")

# each option to click correponds to one of the genes
option_screen = soup.find(lambda tag: tag.name == "select")
values = option_screen.find_all('option')

# write the gene list out to a file
f = open("../dat/gene_list.txt", "w")
for value in values:
    f.write(value.get_text().split(' ')[0] + "\n")
f.close()
