from variable.constant import *


class Variable():

    def __init__(self, candles, indicator_info):
        self.candles = candles
        self.INIT_AF = indicator_info[INIT_AF]
        self.MAX_AF = indicator_info[MAX_AF]

        self.SARS = []
        self.FLOWS = []
        self.EP = 0.0
        self.AF = 0.0
        self.INDEX = 0


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