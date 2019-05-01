# -*- coding: utf-8 -*-

from pickle import OBJ

from variable.candles import CandleList
from variable.constant import *
import time, datetime
from pprint import pprint


class Variable():

    def __init__(self,  candles: CandleList, indicator_info: dict):
        self.candles = candles
        self.LENGTH = indicator_info[LENGTH]
        self.MA = []

        # 계산에 사용되는 임시변수
        self.tmp_sum = 0


class Calc():

    @staticmethod
    def calc(var: Variable, index: int, viewer_data: dict):
        if viewer_data != None and var.LENGTH not in viewer_data[MA]:
            viewer_data[MA][var.LENGTH] = {}

        if index < var.LENGTH - 1:
            var.MA.append(None)
        elif index == var.LENGTH - 1:
            var.tmp_sum = sum(var.candles.현재가[index - var.LENGTH + 1:index + 1])
            var.MA.append(float(var.tmp_sum) / float(var.LENGTH))
        else:
            var.tmp_sum += (var.candles.현재가[index] - var.candles.현재가[index - var.LENGTH])
            var.MA.append(float(var.tmp_sum) / float(var.LENGTH))

        if viewer_data != None and index == var.LENGTH - 1:
            viewer_data[MA][var.LENGTH] = {}
            viewer_data[MA][var.LENGTH][ADDED] = []
            print(var.candles.체결시간[index])
            viewer_data[MA][var.LENGTH][ADDED].append({
                체결시간: int(time.mktime(var.candles.체결시간[index].timetuple()) * 1000),
                VALUE: var.MA[-1]
            })
        elif viewer_data != None and index > var.LENGTH - 1:
            viewer_data[MA][var.LENGTH][ADDED].append({
                체결시간: int(time.mktime(var.candles.체결시간[index].timetuple()) * 1000),
                VALUE: var.MA[-1]
            })
        if index == 130:
            print("A")



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
