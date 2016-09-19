
library(timelineR)
library(magrittr)
library(readr) # friendly way to read csv file / not the fastest : use data.tables' fread
library(stringr)
library(dplyr)

#### Inspiration :   
#http://www.buildingwidgets.com/blog/2015/12/30/week-52-d3kittimeline

#Main data directory "C:\\Users\\FRURAJC\\SGL\\Dataviz\\zikaViz\\data"

#### Steps : 
# Create the dataset
# Generate the Javascript code


### Create the dataset
# Extract from the exported CSV file
fileIn = "C:/Users/FRURAJC/SGL/Dataviz/zikaViz/data/zikatest.csv"
zika_data <- read.csv2(fileIn,sep=",",dec=".")
# Filetr to get only 2016 data
zika = zika_data %>% filter(Year == '2016') %>% select(Date , Country, Territory) %>% transform(str_trim(Territory))
zika = zika %>% mutate(AffectedArea = str_c(
  zika$Country,  
    ifelse(zika$Territory != " ",str_c("(", str_trim(zika$Territory),")"),"")
  )
  )

zikaGraph = zika %>% select(Date, AffectedArea) 
### Target dataset : date (YYYY-MM-DD) / affected area (Country (Territory, if applicable))
# E.g : 
graph_data <- data.frame(
  time = zikaGraph$Date,
  zone = zikaGraph$AffectedArea,
  stringsAsFactors = FALSE
)

tchart<-d3kit_timeline(
  graph_data,
  direction = "right",
  # time is default but show as example of flexible argument types
  timeFn = ~time,
  textFn = htmlwidgets::JS(
    "
    function(d){
    return new Date(d.time).getFullYear() + ' - ' + d.zone;
    }
    "
  ),
  labelBgColor = "#FFB612",
  margin = list(left = 20, right = 50, top = 20, bottom = 40),
  width = 1000,
  height = 850
  ) 
htmlwidgets::JS("tchart.data(graph_data).resizeToFit()")
tchart
