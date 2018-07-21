import urllib.request
import urllib
import re
import json
import Foundation as fd
import Utility as ut

CONST_BUY_EACH = 100


class Player:
    __cur_money = 0
    __copies = 0
    __purchased_lst = []

    __foundation = None

    def __init__(self, initMoney):
        self.__cur_money = initMoney

    def KnowFoundation(self, foundationName, foundationCode):
        self.__foundation = fd.Foundation(foundationName, foundationCode)
        if self.__foundation.LoadData():
            print("发现一个基金,基金名称:{0},代码:{1}".format(
                foundationName, foundationCode))
            return True
        else:
            print("找不到基金数据,基金名称:{0},代码:{1}".format(
                foundationName, foundationCode))
            self.__foundation = None
            return False

    def BuyFoundation(self, buy_money):
        if not self.__foundation:
            print("不了解任何基金,无法购买")
            return False
        if self.__cur_money < buy_money:
            print("身上的钱不足以购买基金,当前:{0}".format(self.__cur_money))
            return False

        buy_ret = self.__foundation.Buy(buy_money)
        if buy_ret:
            self.__copies += buy_ret["num"]

            self.__cur_money -= buy_ret["money"]

            purchased_item = fd.PurchasedFoundation(
                buy_ret["net"],
                buy_ret["num"],
                ut.GetBuyCharge(buy_money),
                buy_ret["buy_date"],
                buy_ret["keep_date"])
            self.__purchased_lst.append(purchased_item)

            self.__foundation.NextDay()
            print("购买成功,金额:{0:.2f},手续费:{1:.2f},净值:{2:.4f},购买份额:{3:.2f},持有份额:{4:.2f}".format(
                buy_ret["money"], buy_ret["charge"], buy_ret["net"], buy_ret["num"], self.__copies))
            return True
        else:
            print("购买失败")
            return False

    def SellFoundation(self):
        if not self.__foundation:
            print("不了解任何基金,无法卖出")
            return False
        if not self.__purchased_lst:
            print("没有持有基金,不能卖出")
            return False

        cur_net = self.__foundation.CurNet()
        cur_date = self.__foundation.CurDate()
        max_gain = -999
        sell_item = None
        for purchased_item in self.__purchased_lst:
            keep_day = ut.GetDateDiff(cur_date, purchased_item.KeepDate())
            print(cur_date, purchased_item.KeepDate(), keep_day)
            if keep_day == 0:
                print("持有基金为0天,不能卖出")
                return False
            s_charge = ut.GetSellCharge(keep_day)
            charge_ratio = ut.GetChargeRatio(
                purchased_item.BuyRate(), s_charge)

            gain_ratio = (cur_net * charge_ratio - purchased_item.Net()) / \
                purchased_item.Net()

            if gain_ratio > max_gain:
                max_gain = gain_ratio
                sell_item = purchased_item

        if sell_item:
            sell_rate = ut.GetSellCharge(
                ut.GetDateDiff(sell_item.KeepDate(), cur_date))
            sell_ret = self.__foundation.Sell(sell_item.Num(), sell_rate)
            if sell_ret:
                self.__copies -= sell_ret["num"]

                self.__cur_money += sell_ret["money"]

                self.__purchased_lst.remove(sell_item)

                self.__foundation.NextDay()
                print("卖出成功,金额:{0:.2f},手续费:{1:.2f},净值:{2:.4f},卖出份额:{3:.2f},持有份额:{4:.2f}".format(
                    sell_ret["money"], sell_ret["charge"], sell_ret["net"], sell_ret["num"], self.__copies))
                return True
            else:
                print("卖出失败")
        else:
            print("卖出失败,没有合适的净值可以出售")
        return False


# ut.DownloadFoundationHtml(110022)
ut.SaveHistoryNetValue("易方达消费行业股票.txt")

# wz = Player(10000)
# wz.KnowFoundation("易方达消费行业股票", 110022)
# wz.BuyFoundation(10000)
# wz.SellFoundation()
