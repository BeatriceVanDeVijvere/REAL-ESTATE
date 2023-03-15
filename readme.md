# Real Estate Price Prediction

# We scrape a website:
    https://www.immoweb.be/
Build a dataset from scratch
   
Implement a strategy to collect as much data as possible: Here sitemap is used



Locality\
Type of property (House/apartment)\
Subtype of property (Bungalow, Chalet, Mansion, ...)\
Price\
Type of sale (Exclusion of life sales)\
Number of rooms\
Living Area\
Fully equipped kitchen (Yes/No)\
Furnished (Yes/No)\
Open fire (Yes/No)\
Terrace (Yes/No)\
If yes: Area\
Garden (Yes/No)\
If yes: Area\
Surface of the land\
Surface area of the plot of land\
Number of facades\
Swimming pool (Yes/No)\
State of the building (New, to be renovated, ...)\

with airflow\
dag with tasks to scrape \
build the links \
get info from the links\
all in docker container\
put data on postgres database \
compare for doubles\
make accesible in API
