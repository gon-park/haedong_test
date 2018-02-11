from variable.constant import *


class Variable():
    candles = {}
    INIT_AF = 0.0
    MAX_AF = 0.0

    SARS = []
    FLOWS = []
    EP = 0.0
    AF = 0.0
    INDEX = 0

    def __init__(self, candles, indicator_info):
        self.candles = candles
        self.INIT_AF = indicator_info[INIT_AF]
        self.MAX_AF = indicator_info[MAX_AF]


class Calc():
    @staticmethod
    def calc(var, index):
        if var.INDEX < 5:
            var.SARS.append(None)
            var.FLOWS.append(None)
        elif var.INDEX == 5:
            Calc.init_sar(var, index)
        else:
            Calc.calc_sar(var, index)
        pass

    @staticmethod
    def init_sar(var, index):
        pass

    @staticmethod
    def calc_sar(var, index):
        pass