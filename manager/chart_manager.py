# -*- coding: utf-8 -*-
from variable.constant import *
from manager import __manager
from variable.chart import Chart


class ChartManger(__manager.ManagerClass):

    @staticmethod
    def create_charts(strategy_var, candles):
        charts = {}

        for chart_id in candles:
            for chart_info in strategy_var[CHARTS]:
                subject_code, type, time_unit = chart_id.split('_')
                if chart_info[TYPE] == type and chart_info[TIME_UNIT] == time_unit:
                    charts[chart_id] = Chart(chart_id, chart_info[INDICATORS], candles[chart_id])

        return charts

    @staticmethod
    def candle_push(chart, index):
        pass

    
    def get_name(self):
        return str(self.__class__.__name__)

    def print_status(self):
        print(self.__getattribute__())
