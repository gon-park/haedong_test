# -*- coding: utf-8 -*-

## short cut strategy
## '18.5.7 Hee Jun is coding now..

from variable.constant import *
from strategy import __base_strategy
from indicator import ma
import math
import os
from variable import subject
from variable.report import Report


class ShortCut(__base_strategy.BaseStrategy):

    def __init__(self, charts: dict, subject_code: str, main_chart: str, strategy_var: dict, contracts: dict):
        super(ShortCut, self).__init__()
        self.strategy_name = "short_cut"
        self.charts = charts
        self.main_chart_id = subject_code + '_' + main_chart
        self.strategy_var = strategy_var
        self.pid = os.getpid()
        self.order_contents = {}
        self.profit_tick = [[]]
        self.profit_dribble_tick = []
        self.sonjul_tick = [[]]
        self.sonjul_dribble_tick = []
        self.contracts = contracts

    def check_contract_in_candle(self, subject_code: str):
        pass

    def is_it_ok(self, subject_code: str, current_price: float):
        pass

    def is_it_sell(self, subject_code: str, current_price: float):
        pass

    def check_contract_in_tick(self, subject_code, current_price):
        pass

    def post_trade(self, report: Report):
        pass