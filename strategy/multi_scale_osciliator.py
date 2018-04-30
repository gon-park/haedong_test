# -*- coding: utf-8 -*-
from variable.constant import *
from strategy import __base_strategy
from indicator import ma, rsi
import math
import os
from variable import subject
from variable.report import Report


class MSO(__base_strategy.BaseStrategy):

    def __init__(self, charts: dict, subject_code: str, main_chart: str, strategy_var: dict, contracts: dict):
        super(MSO, self).__init__()
        self.charts = charts
        self.main_chart_id = subject_code + '_' + main_chart
        self.strategy_var = strategy_var
        self.pid = os.getpid()
        self.order_contents = {}
        self.contracts = contracts

    def print(self):
        from pprint import pprint

        for chart in self.charts:
            pprint(self.charts[chart].indicators[RSI][0].RSI)

    def check_contract_in_candle(self, subject_code: str):
        order_info = None

        res = []
        for chart_key in self.charts:
            res.append({});
            for indicator_name in self.charts[chart_key].indicators:
                for indicator in self.charts[chart_key].indicators[indicator_name]:
                    indicator_calc = None
                    if indicator_name == RSI: indicator_calc = rsi.Calc
                    elif indicator_name == MA: indicator_calc = ma.Calc

                    res[chart_key][indicator_calc.get_signal(indicator, self.charts[chart_key].index)] += 1

        if subject_code in self.contracts and MSO.get_contract_count(subject_code, self.contracts, MSO) > 0:
            contracts = self.get_contracts(subject_code, self.contracts, 풀파라)

            if contracts[0].매도수구분 == 신규매수:
                pass
            else:
                pass
        else:
            pass


        return order_info

    def check_contract_in_tick(self, subject_code, current_price):
        pass

    def is_it_ok(self, subject_code: str, current_price: float):
        log = self.log

        return self.order_contents

    def is_it_sell(self, subject_code: str, current_price: float):
        log = self.log

        return None

    def post_trade(self, report: Report):
        pass

