# -*- coding: utf-8 -*-

from pickle import OBJ

from variable.candles import CandleList
from variable.constant import *
from pprint import pprint


class Variable(Object):

    def __init__(self,  candles: CandleList, indicator_info: dict):
        self.candles = candles
        self.LENGTH = indicator_info[LENGTH]
        self.MA = []

        # 계산에 사용되는 임시변수
        self.tmp_sum = 0


class Calc(Object):

    @staticmethod
    def calc(var: Variable, index: int):
        if index < var.LENGTH - 1:
            var.MA.append(None)
        elif index == var.LENGTH - 1:
            var.tmp_sum = sum(var.candles.현재가[index - var.LENGTH + 1:index + 1])
            var.MA.append(float(var.tmp_sum) / float(var.LENGTH))
        else:
            var.tmp_sum += (var.candles.현재가[index] - var.candles.현재가[index - var.LENGTH])
            var.MA.append(float(var.tmp_sum) / float(var.LENGTH))

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
            return 상승세
        if ma == desc:
            return 하락세

        return 알수없음
