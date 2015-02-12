import string, urllib
import urllib.request
from lxml import etree
import re
from MCScrapper import const
import time
import pickle

#import httplib
#httplib.HTTPConnection._http_vsn = 10
#httplib.HTTPConnection._http_vsn_str = 'HTTP/1.0'

xpath_mapping = {'Company': '//*[@id="nChrtPrc"]/div[3]/h1/text()',
                 'ISIN' : '//*[@id="nChrtPrc"]/div[4]/div[1]/text()[3]',
                 'Price': '//*[@id="Bse_Prc_tick"]/strong/text()',
                 'Market Cap': '//*[@id="nChrtPrc"]/div[11]/div[1]/div[2]/div[8]/div[1]/div[1]/div[1]/div[1]/div[2]/text()',
                 'P/E': '//*[@id="nChrtPrc"]/div[11]/div[1]/div[2]/div[8]/div[1]/div[1]/div[1]/div[2]/div[2]/text()',
                 'Book Value': '//*[@id="nChrtPrc"]/div[11]/div[1]/div[2]/div[8]/div[1]/div[1]/div[1]/div[3]/div[2]/text()',
                 'Div %': '//*[@id="nChrtPrc"]/div[11]/div[1]/div[2]/div[8]/div[1]/div[1]/div[1]/div[4]/div[2]/text()',
                 'Industry P/E': '//*[@id="nChrtPrc"]/div[11]/div[1]/div[2]/div[8]/div[1]/div[1]/div[1]/div[6]/div[2]/text()',
                 'EPS (TTM)': '//*[@id="nChrtPrc"]/div[11]/div[1]/div[2]/div[8]/div[1]/div[1]/div[2]/div[1]/div[2]/text()',
                 'P/C': '//*[@id="nChrtPrc"]/div[11]/div[1]/div[2]/div[8]/div[1]/div[1]/div[2]/div[2]/div[2]/text()', #price / cashflow
                 'Price/Book': '//*[@id="nChrtPrc"]/div[11]/div[1]/div[2]/div[8]/div[1]/div[1]/div[2]/div[3]/div[2]/text()',
                 'Div Yield %': '//*[@id="nChrtPrc"]/div[11]/div[1]/div[2]/div[8]/div[1]/div[1]/div[2]/div[4]/div[2]/text()',
                 'Face Value': '//*[@id="nChrtPrc"]/div[11]/div[1]/div[2]/div[8]/div[1]/div[1]/div[2]/div[5]/div[2]/text()',
}

def defaultFunc( value ):
    return( value )

def floatFunc( value ):
    value = re.sub( ',', '', value )
    value = re.sub( '%', '', value )
    return( float( value) )

def ISINFunc( value ):
    value = re.sub( 'ISIN: ', '', value)
    value = re.sub( ' ', '', value )
    return( value )

lambda_mapping = {
                    'Company' : defaultFunc,
                    'ISIN' : ISINFunc,
                    'Price' : floatFunc,
                    'Market Cap': floatFunc,
                    'P/E': floatFunc,
                    'Book Value': floatFunc,
                    'Div %': floatFunc,
                    'Industry P/E': floatFunc,
                    'EPS (TTM)': floatFunc,
                    'P/C': floatFunc,
                    'Price/Book': floatFunc,
                    'Div Yield %': floatFunc,
                    'Face Value': floatFunc,
}

def getValueForKey(html, key):
    xpath = xpath_mapping[ key ]
    xpath = html.xpath(xpath)
    func = lambda_mapping[key]
    if xpath:
        return( func( xpath[0] ) )
    return ''

def getAllSectorLinks(parent_url):
    page = urllib.request.urlopen(parent_url)
    data = page.read()
    page.close()
    html = etree.HTML(data)
    xpath = html.xpath('/html/body/div/div[2]/div[7]/div[1]/div[7]/div[1]/div[2]/ul');
    links = [];
    for element in xpath[0]:
        link_path = etree.tostring(element).decode("utf-8")
        relative_path = re.search('href=\"(.+?)\"', link_path)
        if relative_path:
            link = "http://www.moneycontrol.com/" + relative_path.group(1)
            links.append(link)
    return links


def getTickersForSector(sector_url):
    page = urllib.request.urlopen(sector_url )
    data = page.read()
    page.close()
    html = etree.HTML(data)
    xpath = html.xpath('/html/body/div/div[2]/div[7]/div[1]/div[7]/div[2]/div/table');
    links = [];
    for element in xpath[0]:
        link_path = etree.tostring(element).decode("utf-8")
        relative_path = re.search('href=\"(.+?)\"', link_path)
        if relative_path:
            link = "http://www.moneycontrol.com/" + relative_path.group(1)
            links.append(link)
    return links


def getAllTickerLinks(parent_url):
    sector_links = getAllSectorLinks(parent_url)
    all_links = []
    for sector_url in sector_links:
        print("Processing ..." + sector_url)
        repeat_count = const.SECTOR_LINKS_REPEAT_COUNT
        while( repeat_count > 0 ):
            try:
                new_links = getTickersForSector(sector_url)
                all_links = list(set(all_links) | set(new_links))
                break
            except:
                time.sleep( const.SECTOR_LINKS_ERROR_SLEEP_TIME )
                repeat_count = repeat_count - 1
                if( repeat_count == 0 ):
                    print( "Failed to Process .." + sector_url )
    return all_links


def saveAllTickerLinks( links ):
    file = open(const.LINKS_FILENAME, 'w')
    for link in links:
        file.write( link )
        file.write( "\n" )
    file.close()

def readAllTickerLinks():
    file = open( const.LINKS_FILENAME, 'r' )
    lines = file.read().splitlines()
    links = [];
    for line in lines:
        links.append( line )
    return( links )


def symbolStats(symbol_url):
    page = urllib.request.urlopen(symbol_url)
    data = page.read()
    page.close()
    html = etree.HTML(data)
    symbol_stats = {}
    for key in xpath_mapping:
        symbol_stats[key] = getValueForKey(html, key)
    symbol_stats[ "Date" ] = time.strftime("%x")
    return symbol_stats

def getStatsFromLinks( links, stats = {} ):
    counter = 0
    for link in links:
        counter = counter + 1
        print( counter )
        if( link in stats ):
            print( "Already Parsed :" + link )
            continue

        print(link)
        repeat_count = const.SYMBOL_LINKS_REPEAT_COUNT
        while( repeat_count > 0):
            try:
                symbol_stats = symbolStats(link)
                print( symbol_stats )
                stats[ link ] = symbol_stats
                break
            except:
                time.sleep( const.SYMBOL_LINKS_ERROR_SLEEP_TIME )
                repeat_count = repeat_count - 1
                if( repeat_count == 0 ):
                    print("Cannot parse " + link)
    return stats

def getStats(parent_url):
    all_links = getAllTickerLinks(parent_url)
    stats = getStatsFromLinks( all_links )
    return stats

def saveStatsToFile( stats ):
    file = open( const.TICKER_STATS_FILENAME, 'wb')
    pickle.dump( stats, file)
    file.close()

def readStatsFromFile():
    file = open( const.TICKER_STATS_FILENAME, 'rb' )
    stats = pickle.load( file )
    return stats

#parent_url = 'http://www.moneycontrol.com/stocks/marketinfo/marketcap/bse/index.html'
#stats = getStats(parent_url)

#parent_url = 'http://www.moneycontrol.com/stocks/marketinfo/marketcap/bse/index.html'
#links = getAllTickerLinks( parent_url )
#saveAllTickerLinks( links )

#links = readAllTickerLinks();
#print( links )

#parent_url = 'http://www.moneycontrol.com/stocks/marketinfo/marketcap/bse/index.html'
#links = getAllSectorLinks(parent_url)
#saveAllTickerLinks( links )

#sector_url = 'http://www.moneycontrol.com/stocks/marketinfo/marketcap/bse/steel-pig-iron.html'
#links = getTickersForSector( sector_url )
#print links


#parent_url = 'http://www.moneycontrol.com/stocks/marketinfo/marketcap/bse/index.html'
#all_links = getAllTickerLinks( parent_url )
#print all_links
#print len( all_links )

#symbol_url = 'http://www.moneycontrol.com//india/stockpricequote/financeinvestments/nagreekacapitalinfrastructure/CRG'
#print( symbolStats( symbol_url ) )
