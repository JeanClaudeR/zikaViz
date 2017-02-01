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
#outbreakNewsURL ="http://www.who.int/csr/don/archive/disease/zika-virus-infection/fr/"
# French version#"http://www.who.int/csr/don/archive/disease/zika-virus-infection/fr/"
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
keywdFR = "Infection à virus Zika" 
keywdEN ="Zika virus infection "
zikaNews_content = [s for s in zikaNews_dirty if re.search(keywdEN, s)]

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

### Extract Day / Month / Year in the Split_Date column, 1 row is of the form [21, January, 2016]
# Refactor this using only 1 (one) function
zika["Day"]= pd.Series(zika["Split_Date"].iloc[i][0] for i in range(len(zika)))
zika["Month"]= pd.Series(zika["Split_Date"].iloc[i][1] for i in range(len(zika)))
zika["Year"]= pd.Series(zika["Split_Date"].iloc[i][2] for i in range(len(zika)))

# Extract Country and Territory
zika["Country"] = pd.Series(zika["Split_Locations"].iloc[i][0] for i in range(len(zika))) 
zika["Territory"] = pd.Series(zika["Split_Locations"].iloc[i][len(zika["Split_Locations"].iloc[i])-1] for i in range(len(zika)))

zika["Territory"] =pd.Series(zika["Territory"][i] if zika["Territory"][i] != zika["Country"][i]  else " " for i in range(len(zika)))

### Mapping/conversion of Month and
# Map Month from a string literal like "April" into a string of length 2 like "04"
monthDict ={
    "January" : "01",
    "February" : "02",
    "March" : "03",
    "April" : "04",
    "May" : "05",
    "June" : "06",
    "July" : "07",
    "August" : "08",
    "September" : "09",
    "October" : "10",
    "November" : "11",
    "December" : "12"
    } 
mapKey = lambda dict,key: dict[key] if key in dict.keys() else None
zika["Month"] = pd.Series(mapKey(monthDict,zika["Month"][i]) for i in range(len(zika)))
# "Day" must be a string of length 2, e.g "8"-> "08"
# convert integer to string but augment the converted integer if it is originally less than 10
# NOTE : could be handled via a pattern matching
augmIntConvToStr = lambda x: "0" + str(x) if len(x) < 2 else str(x) 
zika["Day"] = pd.Series(augmIntConvToStr(zika["Day"][i]) for i in range(len(zika)))
zikaDate = zika[["Year","Month","Day"]] #a simpler way is to concatenate using the "+" operator for strings
#Recreation of a date "YYYY-MM-DD"
joinString = lambda x,y: y.join(x)
zikaDate["Date"] = pd.Series(joinString(zikaDate.iloc[i],"-") for i in range(len(zikaDate)))
zikaTerritory = zika[["Country", "Territory"]]
# EXPORT THE RELEVANT DATA TO BE GRAPHED

zikaExport = zikaDate.join(zikaTerritory) 




