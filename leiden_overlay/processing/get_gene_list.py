from bs4 import BeautifulSoup
import urllib

r = urllib.urlopen("http://www.dmd.nl/nmdb2/home.php?action=switch_db").read()
soup = BeautifulSoup(r, "html.parser")

option_screen = soup.find(lambda tag: tag.name == "select")
values = option_screen.find_all('option')

f = open("../dat/gene_list.txt", "w")
for value in values:
    f.write(value.get_text().split(' ')[0] + "\n")
f.close()
