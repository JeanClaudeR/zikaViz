####################################################
# Goal : Scraping the data on Zika virus           #
# Author : Jean-Claude Razafindrakoto              #
# Date : 2016-09-06                                #
# Python : 3.5.2 (Anaconda 4.1.11)                 #
####################################################

# Libraries import
from lxml import html
from lxml.html.clean import clean_html
import requests
import cytoolz as ct #functional programming
import cytoolz.curried as ctc as ct #functional programming

### Target URL
outbreakNewsURL = "http://www.who.int/csr/don/archive/disease/zika-virus-infection/en/"
page = requests.get(outbreakNewsURL)
tree = html.fromstring(page.content)
#html.open_in_browser(tree)
#datesXPath = '//*[@id="content"]/div/div[1]/ul'
newsXPath = '//li'
zikaNews = tree.xpath(newsXPath)

### Stroe the relevant news in a list
zikaNews_dirty = [p.text_content() for p in zikaNews]
zikaNews_content = [s for s in zikaNews_dirty if re.search(r"Zika virus infection ", s)]
# Extract only the items with the pattern "Zika virus infection "
#sample=[ 'Biorisk reduction\n', '\n22 April 2016\n\t\t\tZika virus infection – Papua New Guinea\n']
#subsample =sample[1]

substituteNonUnicode = lambda s : re.sub(r"\s"," ",s)
removeSpace = lambda s: s.strip()
zikaNews_Clean = [cytoolz.pipe(s, removeSpace, substituteNonUnicode) for s in zikaNews_content]

### Extracting the dates as well as the countries
key=re.compile('((.*)(Zika virus infection)(.*))') #issue with the dash after Zika virus infection
zikaDateCountries = [key.match(s).group(2,4) for s in zikaNews_Clean]
#zikaDateCountries[2] #('20 April 2016   ', '– Saint Lucia')
### Regex results is a tuple group(1 , 2, 3, 4)
# 1 : matched string
# 2 : the date of event
# 3 : the key 'Zika virus infection'
# 4 : the countries hit by the outbreak
###

### Cleaning the countries name
test=zikaDateCountries[20][1] #'– United States of America - Puerto Rico'
test.replace("- ","@")
key2=re.compile('(-.\w+)')
#key2=re.compile('^(.*?)(-)(.*)')
print(key2.findall(' - Puerto Rico'))
print(key2.findall(test))

