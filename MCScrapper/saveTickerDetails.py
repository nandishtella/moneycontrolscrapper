__author__ = 'nandi_000'

# Run this script after running saveLinks

from MCScrapper import AllStocks, const

links = AllStocks.readAllTickerLinks()

links_covered = 0
length = len( links )
length = 90
while( links_covered < length ):
    try:  #Incase the file has not been created yet
        stats = AllStocks.readStatsFromFile()
    except:
        stats = {}
    links_subset = links[ links_covered: links_covered + 100 ]
    links_covered += 100
    stats = AllStocks.getStatsFromLinks( links_subset, stats )
    AllStocks.saveStatsToFile( stats )

print( stats )

