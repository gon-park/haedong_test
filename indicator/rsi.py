# -*- coding: utf-8 -*-

from pickle import OBJ

from variable.constant import *
from pprint import pprint
from talib.abstract import RSI

class Variable():

    def __init__(self,  candles: dict, indicator_info: dict):
        self.candles = candles
        self.LENGTH = indicator_info[LENGTH]

        self.RSI = RSI(candles, timeperiod=self.LENGTH)



class Calc():
    pass