from future.backports import datetime

__author__ = 'nandi_000'

import unittest
from MCScrapper import utils, const
import time

class testUtils(unittest.TestCase):
#check if the values for LT are valid

    def test_symbolStats( self ):
        url = 'http://www.moneycontrol.com/india/stockpricequote/infrastructure-general/larsentoubro/LT'
        stats = utils.symbolStats( url )
        print( stats )
        self.assertIsNotNone( stats )
        numericalFields = [ "Price",
                            "Standalone Price/Book",
                            "Consolidated Price/Book",
                            "Face Value",
                            "Standalone EPS (TTM)",
                            "Consolidated EPS (TTM)",
                            "Market Cap",
                            "Industry P/E",
                            "Standalone P/E",
                            "Consolidated P/E",
                            "Standalone P/C",
                            "Consolidated P/C",
                            "Standalone Book Value",
                            "Consolidated Book Value",
                            "Div Yield %",
                            "Div %"
                          ]

        for field in numericalFields:
            data = stats[field]
            self.assertGreater( data, 0.1 )
        self.assertEqual( stats[ "Company"], "Larsen and Toubro" )
        self.assertEqual( stats[ "ISIN"], "INE018A01030" )
        self.assertEqual( stats["Date"], time.strftime("%x") )
        #Test for Error Values
        url = 'http://www.moneycontrol.com/india/stockpricequote/transport-logistics/jetairways/JA01' #Airlines never make profits
        stats = utils.symbolStats( url )
        self.assertIsNotNone( stats )
        numericalFields = [ "Price",
                            "Face Value",
                            "Market Cap",
                            "Industry P/E",
                          ]
        errorFields = [ "Standalone Price/Book",
                        "Consolidated Price/Book",
                        "Standalone EPS (TTM)",
                        "Consolidated EPS (TTM)",
                        "Standalone P/E",
                        "Consolidated P/E",
                        "Standalone P/C",
                        "Consolidated P/C",
                        "Standalone Book Value",
                        "Consolidated Book Value",
                        "Div Yield %",
                        "Div %",
                      ]
        for field in numericalFields:
            data = stats[field]
            self.assertGreater( data, 0.1 )

        for field in errorFields:
            data = stats[field]
            self.assertLessEqual( data, 0.0 )

        self.assertEqual( stats[ "Company"], "Jet Airways" )
        self.assertEqual( stats[ "ISIN"], "INE802G01018" )
        self.assertEqual( stats["Date"], const.DATE )
        print( stats )



if __name__ == '__main__':
    unittest.main()

