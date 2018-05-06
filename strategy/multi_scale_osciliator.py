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

    def check_contract_in_candle(self, subject_code: str, current_price: float):
        order_info = None

        res = []
        for chart_key in self.charts:
            res.append({})
            res[-1]['cnt'] = 0
            res[-1]['sum'] = 0

            for indicator_name in self.charts[chart_key].indicators:
                for indicator in self.charts[chart_key].indicators[indicator_name]:
                    indicator_calc = None
                    if indicator_name == RSI: indicator_calc = rsi.Calc
                    elif indicator_name == MA: indicator_calc = ma.Calc

                    signal = indicator_calc.get_signal(indicator, self.charts[chart_key].index)

                    res[-1]['cnt'] += 1
                    res[-1]['sum'] += signal

            score = float(res[-1]['sum']) / res[-1]['cnt']
            res[-1]['score'] = score
        # print(current_price)
        # print(res)


        if subject_code in self.contracts and MSO.get_contract_count(subject_code, self.contracts, MSO) > 0:
            # print(MSO.get_contract_count(subject_code, self.contracts, MSO))
            # print()

            # 계약 있을 때
            contracts = self.get_contracts(subject_code, self.contracts, MSO)

            if contracts[0].매도수구분 == 신규매수:
                if all(obj['score'] < 0 for obj in res):
                    order_info = {
                        신규주문: True,
                        종목코드: subject_code,
                        매도수구분: 신규매도,
                        매매전략: MSO,
                        수량: 2,
                        가격: current_price
                    }

            else:
                if all(obj['score'] > 0 for obj in res):
                    order_info = {
                        신규주문: True,
                        종목코드: subject_code,
                        매도수구분: 신규매수,
                        매매전략: MSO,
                        수량: 2,
                        가격: current_price
                    }
        else:
            if all(obj['score'] > 0.5 for obj in res):
                print(res)
                order_info = {
                    신규주문: True,
                    종목코드: subject_code,
                    매도수구분: 신규매수,
                    매매전략: MSO,
                    수량: 2,
                    가격: current_price
                }

            elif all(obj['score'] < -0.5 for obj in res):

                order_info = {
                    신규주문: True,
                    종목코드: subject_code,
                    매도수구분: 신규매도,
                    매매전략: MSO,
                    수량: 2,
                    가격: current_price
                }

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

