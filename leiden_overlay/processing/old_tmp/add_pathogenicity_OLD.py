from bs4 import BeautifulSoup
import urllib
import unicodedata
import math

def to_ascii(string):
    return unicodedata.normalize('NFKD', string).encode('ascii', 'ignore')

print "Processing overall table..."

variant_name = "DYSF"
r = urllib.urlopen('http://www.dmd.nl/nmdb2/variants.php?select_db='+ variant_name +'&action=view_all').read()
#http://www.dmd.nl/nmdb2/variants.php?action=view_all&limit=100&order=Variant%2FDNA%2CASC&page=1
soup = BeautifulSoup(r, "html.parser")

num_entries = int(soup.find(lambda tag: tag.get('class') == [u'S11']).get_text().split(' ')[0])
num_per_page = 100
num_pages = int(math.ceil(num_entries*1.0/num_per_page*1.0))



variant_dict = {}

i = 0
for page_number in range(1, num_pages+1):

    print "Reached page %d"%(page_number)

    page_url = 'http://www.dmd.nl/nmdb2/variants.php?select_db='+variant_name+ "&action=view_all&limit=100&order=Variant%%2FDNA%%2CASC&page=" + str(page_number)
    #print 'http://www.dmd.nl/nmdb2/variants.php?action=view_all&limit=100&order=Variant%2FDNA%2CASC&page=' + str(page_number)
    #print page_url
    curr_page_soup = BeautifulSoup(urllib.urlopen(page_url).read(), "html.parser")
    #print "HERE"
    #print curr_page_soup
    #print "THERE"
    variant_table = curr_page_soup.find_all(lambda tag: tag.name == "table" and tag.get('class') == [u'data'])[1]
    #print curr_page_soup
    variant_details = variant_table.find_all('tr')
    #for row in variant_details:
    #    print row
    #exit(1)
    #print variant_details
    #del variant_details[0]
    #print variant_details[0], variant_details[1]
    for row in variant_details:
        print ("Processing row %d of %d [%0.3f%% done]...")%(i, num_entries, i*100.0/num_entries)
        i+=1
        print row
        #url = "http://www.dmd.nl" + row[u'onclick'].split(' = ')[1].replace("'", "")[:-1]

out_file = open("./../dat/" + variant_name + "_pathogenicity.txt", "w")
for key in variant_dict:
    out_file.write(key + "\t" + variant_dict[key] + "\n")
out_file.close()

print "Variant pathogenicity gathered."
