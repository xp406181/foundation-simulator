import urllib.request
import urllib
import re
import json
import Foundation as fd
import Utility as ut
import Player as pl


# ut.DownloadFoundationHtml(110022)
# ut.SaveHistoryNetValue("易方达消费行业股票.txt")

wz = pl.Player(10000)
wz.KnowFoundation("易方达消费行业股票", 110022)
# wz.BuyFoundation(10000)
# wz.SellFoundation()
