# -*- coding: utf-8 -*-

from pywin.mfc.object import Object

from variable.candles import CandleList
from variable.constant import *
from indicator import ma, para


class Chart(Object):
    def __init__(self, chart_id: str, indicator_info: dict, candles_dict: dict):
        self.subject_code, self.type, self.time_unit = chart_id.split('_')
        self.indicators = {}
        self.index = -1
        self.candles = CandleList()
        self.candles.시가 = candles_dict[시가]
        self.candles.현재가 = candles_dict[현재가]
        self.candles.고가 = candles_dict[고가]
        self.candles.저가 = candles_dict[저가]
        self.candles.체결시간 = candles_dict[체결시간]
        self.candles.거래량 = candles_dict[거래량]

        for indicator_name in indicator_info:
            self.indicators[indicator_name] = {}

            if indicator_name == MA:
                self.indicators[indicator_name] = []
                for info in indicator_info[indicator_name]:
                    self.indicators[indicator_name].append(ma.Variable(self.candles, info))

            elif indicator_name == PARA:
                self.indicators[indicator_name] = []
                for info in indicator_info[indicator_name]:
                    self.indicators[indicator_name].append(para.Variable(self.candles, info))

    def __str__(self) -> str:
        return "subject_code=" + str(self.subject_code) + " type=" + str(self.type) + " time_unit=" + str(self.time_unit) + " candles=" + str(self.candles)


