from variable.constant import *
from indicator import ma, para

class Chart():
    subject_code = None
    type = None
    time_unit = 0
    candles = {}
    indicators = {}
    index = -1

    def __init__(self, chart_id, indicator_info, candles):
        self.subject_code, self.type, self.time_unit = chart_id.split('_')
        self.candles = candles
        for indicator_name in indicator_info:
            self.indicators[indicator_name] = {}

            if indicator_name == MA:
                self.indicators[indicator_name] = ma.Variable(candles, indicator_info[indicator_name])
            elif indicator_name == PARA:
                self.indicators[indicator_name] = para.Variable(candles, indicator_info[indicator_name])


    def __str__(self) -> str:
        return "subject_code=" + str(self.subject_code) + " type=" + str(self.type) + " time_unit=" + str(self.time_unit) + " candles=" + str(self.candles)


