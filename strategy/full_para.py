# -*- coding: utf-8 -*-
from variable.constant import *
from strategy import __base_strategy
import math
from variable import subject


class Full_Para(__base_strategy.BaseStrategy):
    def __init__(self, trader):
        self.charts = trader.charts
        self.trader = trader
        type, time_unit = trader.main_chart.split('_')
        subject_code = trader.subject_code

        self.main_chart_id = subject_code + '_' + type + '_' + time_unit

    def is_it_ok(self, subject_code, current_price):
        return None

    def is_it_sell(self, subject_code, current_price):
        return None

    def check_contract_in_candle(self, subject_code):
        # 메인차트 Index가 부족 할 때 거래 안함
        if self.charts[self.main_chart_id].index < 3000:
            return None

        main_chart = self.charts[self.main_chart_id]
        para = main_chart.indicators[PARA][0]
        if subject_code in self.trader.contracts and len(self.trader.contracts[self.trader.subject_code]) > 0:
            # 계약이 있을 때
            pass
        else:
            # 계약이 없을 때
            if para.FLOW is 상향:
                if main_chart.candles[저가][main_chart.index + 1] < para.SAR:
                    # 하향 반전
                    current_price = math.floor(para.SAR * (1 / subject.info[subject_code[:2]][단위])) / (
                    1 / subject.info[subject_code[:2]][단위])
                    order_info = self.is_it_ok(subject_code, current_price)
                    print('하향 반전, SAR : %s, current_price : %s' % (para.SAR, current_price))
            elif para.FLOW is 하향:
                if para.SAR < main_chart.candles[고가][main_chart.index + 1]:
                    # 상향 반전
                    current_price = math.ceil(para.SAR * (1 / subject.info[subject_code[:2]][단위])) / (1 / subject.info[subject_code[:2]][단위])
                    order_info = self.is_it_ok(subject_code, current_price)
                    print('상향 반전, SAR : %s, current_price : %s' % (para.SAR, current_price))

    def check_contract_in_tick(self, subject_code, current_price):
        pass