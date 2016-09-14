
library(timelineR)
starwars_data <- data.frame(
  time = c(
    "1977-04-25",
    "1980-04-17",
    "1984-04-25",
    "1999-04-19",
    "2002-04-16",
    "2005-04-19",
    "2015-11-18"
  ),
  episode = c(4,5,6,1,2,3,7),
  name = c(
    'A New Hope',
    'The Empire Strikes Back',
    'Return of the Jedi',
    'The Phantom Menace',
    'Attack of the Clones',
    'Revenge of the Sith',
    'The Force Awakens'
  ),
  stringsAsFactors = FALSE
)

d3kit_timeline(
  starwars_data,
  direction = "right",
  # time is default but show as example of flexible argument types
  timeFn = ~time,
  textFn = htmlwidgets::JS(
    "
    function(d){
    return new Date(d.time).getFullYear() + ' - ' + d.name;
    }
    "
  ),
  width = 400,
  height = 250
  )