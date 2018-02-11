from variable.constant import *


class Variable():
    candles = {}
    TYPE = None # 추후에 단순종가이동평균선을 제외한 다른 이동평균선도 같이 구할때 개발하기 위해 남겨놓음
    LENGTH = 0
    MA = []

    def __init__(self, candles, indicator_info):
        self.candles = candles
        self.LENGTH = indicator_info[LENGTH]


class Calc():
    @staticmethod
    def calc(var, index):
        if index < var.LENGTH - 1:
            var.MA.append(None)

        else:
            var.MA.append(float(sum(var.candles[현재가][index - var.LENGTH + 1:index + 1])) / float(var.LENGTH))