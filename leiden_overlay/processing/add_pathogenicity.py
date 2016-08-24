from bs4 import BeautifulSoup
import urllib
import unicodedata

def to_ascii(string):
    return unicodedata.normalize('NFKD', string).encode('ascii', 'ignore')

print "Processing overall table..."

variant_name = "DYSF"
r = urllib.urlopen('http://www.dmd.nl/nmdb2/variants.php?select_db='+ variant_name +'&action=view_all').read()
#http://www.dmd.nl/nmdb2/variants.php?action=view_all&limit=100&order=Variant%2FDNA%2CASC&page=1
soup = BeautifulSoup(r, "html.parser")

num_entries = int(soup.find(lambda tag: tag.get('class') == [u'S11']).get_text().split(' ')[0])

variant_table = soup.find_all(lambda tag: tag.name == 'table' and tag.get('class') == [u'data'])[1]

variant_details = variant_table.find_all('tr')
del variant_details[0]

variant_dict = {}

i = 0
for row in variant_details:
    print ("Processing row %d of %d [%0.5f%% done]...")%(i, num_entries, i*1.0/num_entries)
    i+=1
    url = "http://www.dmd.nl" + row[u'onclick'].split(' = ')[1].replace("'", "")[:-1]
    row_soup = BeautifulSoup(urllib.urlopen(url).read(), "html.parser")
    variant_info = row_soup.find_all(lambda tag: tag.get('class') == [u'gene'])[1].find_all('tr')[0]
    #cols = [to_ascii(x.get_text()) for x in variant_info.find_all('th')]
    raw_data = [to_ascii(x.get_text()[1:]) for x in variant_info.find_all('tr')]
    row_dict = {}
    #### Temporary
    #cols = []
    #rows = []
    ##
    for item in raw_data:
        pieces = item.split('\n')
        row_dict[pieces[0]] = pieces[1]
        ###temp
        #cols.append(pieces[0])
        #rows.append(pieces[1])
        ####
    #print row_dict

    # CHANGE THIS SO THAT IT ONLY UPDATES IF ITS THE SAME
    dna_name = row_dict['DNA change'].split(' ')[0]
    variant_dict[dna_name] = row_dict['Reported pathogenicity']
    #exit(1)
print variant_dict
