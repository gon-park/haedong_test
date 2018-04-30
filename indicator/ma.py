# -*- coding: utf-8 -*-

from pickle import OBJ

from variable.candles import CandleList
from variable.constant import *
from pprint import pprint
from talib.abstract import SMA

class Variable():

    def __init__(self,  candles: dict, indicator_info: dict):
        self.candles = candles
        self.LENGTH = indicator_info[LENGTH]

        self.MA = SMA(candles, timeperiod=self.LENGTH)

        # 계산에 사용되는 임시변수
        #self.tmp_sum = 0


class Calc():

    # @staticmethod
    # def calc(var: Variable, index: int):
    #     if index < var.LENGTH - 1:
    #         var.MA.append(None)
    #     elif index == var.LENGTH - 1:
    #         var.tmp_sum = sum(var.candles.현재가[index - var.LENGTH + 1:index + 1])
    #         var.MA.append(float(var.tmp_sum) / float(var.LENGTH))
    #     else:
    #         var.tmp_sum += (var.candles.현재가[index] - var.candles.현재가[index - var.LENGTH])
    #         var.MA.append(float(var.tmp_sum) / float(var.LENGTH))

    @staticmethod
    def get_signal(var:Variable, index:int):
        if index <= 0: return 0
        return 1 if var.MA.iloc[index] > var.MA.iloc[index-1] else -1 if var.MA.iloc[index] < var.MA.iloc[index-1] else 0


    @staticmethod
    def is_sorted(ma_list: list):
        if len(ma_list) < 2:
            return 알수없음

        ma = []
        for i in range(0, len(ma_list)):
            ma.append(ma_list[i].MA[-1])

        asc = ma[:]
        asc.sort()
        desc = asc[:]
        desc.reverse()

        if ma == asc:
            return 하락세
        if ma == desc:
            return 상승세

        return 알수없음
