import urllib.request
import urllib
import re
import json
import Utility as ut


class FoundationDayData:
    __date = ""
    __net = 0
    __total_net = 0
    __inc = 0
    __rate = 0

    def __init__(self, dayJson):
        self.__date = dayJson["date"]
        self.__net = float(dayJson["net"])
        self.__total_net = float(dayJson["totalnet"])
        self.__inc = float(dayJson["inc"])
        self.__rate = float(dayJson["rate"])

    def __lt__(self, value):
        return self.__date < value.__date

    def Date(self):
        return self.__date

    def Net(self):
        return self.__net

    def Rate(self):
        return self.__rate

    def Buy(self, money):
        return money / self.__net

    def Sell(self, num):
        return num * self.__net


class Foundation:
    __cur_day_data = None
    __cur_day = 0
    __all_day_data = []
    __date_arr = []

    __name = ""
    __code = 0

    __inited = False

    def __init__(self, foundationName, foundationCode):
        self.__name = foundationName
        self.__code = foundationCode

    def LoadData(self):
        with open("JsonData" + self.__name + ".txt", "r") as f:
            history_json = json.load(f)
            for item in history_json:
                day_data = FoundationDayData(item)
                self.__all_day_data.append(day_data)
                self.__date_arr.append(day_data.Date())
            self.__all_day_data.sort()
            self.__date_arr.sort()

        if self.__all_day_data:
            self.__cur_day = 0
            self.__cur_day_data = self.__all_day_data[self.__cur_day]
            self.__inited = True

        if not self.__inited:
            print("基金初始化失败,name:{0},code:{1}".format(
                self.__name, self.__code))
        return self.__inited

    def Buy(self, money):
        if not self.__cur_day_data:
            print("数据错误,没有今日数据")
            return

        data = self.__cur_day_data
        rate = ut.GetBuyCharge(money)
        pure_money = money / (1 + rate)
        charge = money - pure_money
        buy_num = data.Buy(pure_money)

        return {"money": money,
                "charge": charge,
                "net": data.Net(),
                "num": buy_num,
                "buy_date": data.Date(),
                "keep_date": self.GetKeepBeginDate(data.Date())}
        # return money, charge, data.Net(), buyNum, data.Date(), self.GetKeepBeginDate(data.Date())

    def Sell(self, num, rate):
        if not self.__cur_day_data:
            print("数据错误,没有今日数据")
            return

        data = self.__cur_day_data
        money = data.Sell(num)
        charge = money * rate
        pureMoney = money - charge

        return {"money": pureMoney,
                "charge": charge,
                "net": data.Net(),
                "num": num}
        # return pureMoney, charge, data.Net(), num

    def Iter(self):
        if not self.__all_day_data:
            return

        length = len(self.__all_day_data)
        i = 0
        while True:
            if self.__cur_day >= length:
                return
            yield self.__all_day_data[i]

            i = i + 1

    def NextDay(self):
        if not self.__all_day_data:
            print("没有基金数据")
            return
        self.__cur_day += 1
        self.__cur_day_data = self.__all_day_data[self.__cur_day]

    def DataLength(self):
        if not self.__all_day_data:
            return 0
        return len(self.__all_day_data)

    def GetKeepBeginDate(self, date):
        if not self.__date_arr:
            return

        if date in self.__date_arr:
            idx = self.__date_arr.index(date)
            if idx <= len(self.__date_arr) - 2:
                return self.__date_arr[idx + 1]
        return

    def CurRate(self):
        if not self.__cur_day_data:
            return 0
        return self.__cur_day_data.Rate()

    def CurNet(self):
        if not self.__cur_day_data:
            return 0
        return self.__cur_day_data.Net()

    def CurDate(self):
        if not self.__cur_day_data:
            return None
        return self.__cur_day_data.Date()


class PurchasedFoundation:
    __net = 0
    __num = 0
    __buy_rate = 0
    __buy_date = None
    __keep_date = None

    def __init__(self, net, num, buy_rate, date1, date2):
        self.__net = net
        self.__num = num
        self.__buy_rate = buy_rate
        self.__buy_date = date1
        self.__keep_date = date2

    # def __lt__(self, value):
    #     return self.__buy_date < value.__buy_date

    def Date(self):
        return self.__buy_date

    def KeepDate(self):
        return self.__keep_date

    def BuyRate(self):
        return self.__buy_rate

    def Net(self):
        return self.__net

    def Num(self):
        return self.__num
