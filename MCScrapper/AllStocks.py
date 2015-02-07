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
                 'Price': '//*[@id="Bse_Prc_tick"]/strong/text()',
                 'MARKET CAP (RS CR)': '//*[@id="nChrtPrc"]/div[10]/div[1]/div[2]/div[8]/div[1]/div[1]/div[1]/div[1]/div[2]/text()',
                 'P/E': '//*[@id="nChrtPrc"]/div[11]/div[1]/div[2]/div[8]/div[1]/div[1]/div[1]/div[2]/div[2]/text()',
                 'BOOK VALUE (RS)': '//*[@id="nChrtPrc"]/div[11]/div[1]/div[2]/div[8]/div[1]/div[1]/div[1]/div[3]/div[2]/text()',
                 'DIV (%)': '//*[@id="nChrtPrc"]/div[11]/div[1]/div[2]/div[8]/div[1]/div[1]/div[1]/div[4]/div[2]/text()',
                 'INDUSTRY P/E': '//*[@id="nChrtPrc"]/div[11]/div[1]/div[2]/div[8]/div[1]/div[1]/div[1]/div[6]/div[2]/text()',
                 'EPS (TTM)': '//*[@id="nChrtPrc"]/div[11]/div[1]/div[2]/div[8]/div[1]/div[1]/div[2]/div[1]/div[2]/text()',
                 'P/C( price / cashflow )': '//*[@id="nChrtPrc"]/div[11]/div[1]/div[2]/div[8]/div[1]/div[1]/div[2]/div[2]/div[2]/text()',
                 'PRICE/BOOK': '//*[@id="nChrtPrc"]/div[11]/div[1]/div[2]/div[8]/div[1]/div[1]/div[2]/div[3]/div[2]/text()',
                 'DIV YIELD.(%)': '//*[@id="nChrtPrc"]/div[11]/div[1]/div[2]/div[8]/div[1]/div[1]/div[2]/div[4]/div[2]/text()',
                 'FACE VALUE (RS)': '//*[@id="nChrtPrc"]/div[11]/div[1]/div[2]/div[8]/div[1]/div[1]/div[2]/div[5]/div[2]/text()'
}


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


def getValueAtXpath(html, xpath):
    xpath = html.xpath(xpath)
    if xpath:
        return xpath[0]
    return ''


def symbolStats(symbol_url):
    page = urllib.request.urlopen(symbol_url)
    data = page.read()
    page.close()
    html = etree.HTML(data)
    symbol_stats = {}
    for key in xpath_mapping:
        symbol_stats[key] = getValueAtXpath(html, xpath_mapping[key])
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

