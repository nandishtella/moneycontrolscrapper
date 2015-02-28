__author__ = 'nandi_000'

# Run this script after running saveLinks

from MCScrapper import utils, const

links = utils.readAllTickerLinks()

links_covered = 0
length = len( links )
#length = 90
while( links_covered < length ):
    try:  #Incase the file has not been created yet
        stats = utils.readStatsFromFile()
    except:
        stats = {}
    links_subset = links[ links_covered: links_covered + 100 ]
    links_covered += 100
    stats = utils.getStatsFromLinks( links_subset, stats )
    utils.saveStatsToFile( stats )
    print( "links covered: " + str( links_covered ) )
#print( stats )

stats_array = []
for stat in stats:
    data = stats[ stat ]
    if( data[ 'P/E' ] != '' ):
        stats_array.append( data )
        #break