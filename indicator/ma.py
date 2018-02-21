# -*- coding: utf-8 -*-

from pickle import OBJ

from pywin.mfc.object import Object

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