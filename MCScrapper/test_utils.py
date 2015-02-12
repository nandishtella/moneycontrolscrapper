from future.backports import datetime

__author__ = 'nandi_000'

import unittest
from MCScrapper import utils
import time

class testUtils(unittest.TestCase):
#check if the values for LT are valid
    def test_symbolStats( self ):
        url = 'http://www.moneycontrol.com/india/stockpricequote/infrastructure-general/larsentoubro/LT'
        stats = utils.symbolStats( url )
        self.assertIsNotNone( stats )
        numericalFields = [ "Price",
                            "Price/Book",
                            "Face Value",
                            "EPS (TTM)",
                            "Market Cap",
                            "Industry P/E",
                            "P/E",
                            "P/C",
                            "Book Value",
                          ]

        for field in numericalFields:
            data = stats[field]
            self.assertGreater( data, 0.1 )
        self.assertEqual( stats[ "Company"], "Larsen and Toubro" )
        self.assertEqual( stats[ "ISIN"], "INE018A01030" )
        self.assertEqual( stats["Date"], time.strftime("%x") )
        print( stats )

if __name__ == '__main__':
    unittest.main()

