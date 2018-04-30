# -*- coding: utf-8 -*-
from variable.constant import *
from manager import __manager
from variable.chart import Chart
from indicator import ma, para


class ChartManger(__manager.ManagerClass):

    @staticmethod
    def create_charts(subject_code: str, strategy_var: dict, candles: dict):
        charts = {}

        for chart_id in candles.keys():
            for chart_info in strategy_var[CHARTS]:
                _subject_code, type, time_unit = chart_id.split('_')
                if subject_code == _subject_code:
                    charts[chart_id] = Chart(chart_id, chart_info[INDICATORS], candles[chart_id])

        return charts

    @staticmethod
    def candle_push(chart: Chart, index: int):
        chart.index += 1

        # for indicator_name in chart.indicators:
        #     if indicator_name == MA:
        #         for indicator in chart.indicators[indicator_name]:
        #             ma.Calc.calc(indicator, chart.index)
        #     elif indicator_name == PARA:
        #         for indicator in chart.indicators[indicator_name]:
        #             para.Calc.calc(indicator, chart.index)

    def get_name(self):
        return str(self.__class__.__name__)

    def print_status(self):
        print(self.__getattribute__())
