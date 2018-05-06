# -*- coding: utf-8 -*-

from ..variable.candles import CandleList
from ..variable.constant import *
from ..indicator import ma, para, rsi


class Chart():
    def __init__(self, chart_id: str, indicator_info: dict, candles_df: dict):
        self.subject_code, self.type, self.time_unit = chart_id.split('_')
        self.indicators = {}
        self.index = -1
        self.candles = candles_df

        for indicator_name in indicator_info:
            self.indicators[indicator_name] = []
            if indicator_name == MA:
                for info in indicator_info[indicator_name]:
                    self.indicators[indicator_name].append(ma.Variable(self.candles, info))

            elif indicator_name == PARA:
                for info in indicator_info[indicator_name]:
                    self.indicators[indicator_name].append(para.Variable(self.candles, info))

            elif indicator_name == RSI:
                for info in indicator_info[indicator_name]:
                    self.indicators[indicator_name].append(rsi.Variable(self.candles, info))

    def __str__(self) -> str:
        return "subject_code=" + str(self.subject_code) + " type=" + str(self.type) + " time_unit=" + str(self.time_unit) + " candles=" + str(self.candles)


