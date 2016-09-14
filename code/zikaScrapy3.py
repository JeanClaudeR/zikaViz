####################################################
# Goal : Scraping the data on Zika virus           #
# Author : Jean-Claude Razafindrakoto              #
# Date : 2016-09-06                                #
# Python : 3.5.2 (Anaconda 4.1.11)                 #
####################################################

# Libraries import
from lxml import html
import requests
import pandas as pd
# FOR FUNCTIONAL PROGRAMMING
import cytoolz # pipe
import cytoolz.curried #map


### Target URL
outbreakNewsURL = "http://www.who.int/csr/don/archive/disease/zika-virus-infection/en/"
page = requests.get(outbreakNewsURL)
tree = html.fromstring(page.content)
#html.open_in_browser(tree)
#datesXPath = '//*[@id="content"]/div/div[1]/ul'
newsXPath = '//li'
zikaNews = tree.xpath(newsXPath)

### Store the relevant news in a list
zikaNews_dirty = [p.text_content() for p in zikaNews]
# Extract only the items containing the pattern "Zika virus infection "
#sample= '\n22 April 2016\n\t\t\tZika virus infection – Papua New Guinea - USA\n'
zikaNews_content = [s for s in zikaNews_dirty if re.search(r"Zika virus infection ", s)]

#### Data cleansing using Pandas
substitudeUnicodeDash = lambda s : re.sub(u'–',"@", s)
substituteNonUnicode = lambda s : re.sub(r"\s"," ",s)
removeSpace = lambda s: s.strip()
zikaNews_dirty = [cytoolz.pipe(s, removeSpace, substituteNonUnicode) for s in zikaNews_content] # a bit ugly
zikaNews_dirty = [s.split("Zika virus infection") for s in zikaNews_dirty ]
zika = pd.DataFrame(zikaNews_dirty, columns = ["Date","Locations"])

### Removing the first dash sign / for zika["Locations"]
# Step 1 : transform in a list of strings, via str.split()
# Step 2 : copy the list, except the first element list[1:]
# Step 3 : reconstitute the entire string using ' '.join(list[1:])
### All in one : use cytoolz.pipe and cytoolz.curried.map()


# Step 1 : transform in a list of strings, via str.split()
zika["Split_Locations"] = pd.Series(zika["Locations"].iloc[i].split()  for i in range(len(zika)))
# Step 2 : copy the list, except the first element list[1:]
zika["Split_Locations"] = pd.Series([s[1:] for s in zika["Split_Locations"]])
# Step 3 : reconstitute the entire string using ' '.join(list[1:])
zika["Split_Locations"] = pd.Series([" ".join(s) for s in zika["Split_Locations"]])
zika["Split_Locations"] = pd.Series([s.split("-") for s in zika["Split_Locations"]])
zika["Split_Date"] = pd.Series([s.split() for s in zika["Date"]])

# Extract Day / Month / Year in the Split_Date column, 1 row is of the form [21, January, 2016]
zika["Day"]= pd.Series(zika["Split_Date"].iloc[i][0] for i in range(len(zika)))
zika["Month"]= pd.Series(zika["Split_Date"].iloc[i][1] for i in range(len(zika)))
zika["Year"]= pd.Series(zika["Split_Date"].iloc[i][2] for i in range(len(zika)))

# Extract Country and Territory
zika["Split_Locations"].iloc[21][0]
zika["Country"] = pd.Series(zika["Split_Locations"].iloc[i][0] for i in range(len(zika))) 
zika["Territory"] = pd.Series(zika["Split_Locations"].iloc[i][len(zika["Split_Locations"].iloc[i])-1] for i in range(len(zika)))

zika["Territory"] =pd.Series(zika["Territory"][i] if zika["Territory"][i] != zika["Country"][i]  else " " for i in range(len(zika)))

zikaExport = zika[["Day","Month", "Year", "Country", "Territory"]] 
zikaJSON = zikaExport.to_json(path_or_buf="c:\\users\\frurajc\\sgl\dataviz\\zikaViz\\zikatest.json", orient="index")
zikaCSV=zikaExport.to_csv(path_or_buf="c:\\users\\frurajc\\sgl\dataviz\\zikaViz\\zikatest.csv")
# EXPORT THE RELEVANT DATA TO BE GRAPHED
