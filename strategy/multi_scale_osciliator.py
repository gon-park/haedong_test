# -*- coding: utf-8 -*-
from variable.constant import *
from strategy import __base_strategy
from indicator import ma
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

    def check_contract_in_candle(self, subject_code: str):
        order_info = None

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

