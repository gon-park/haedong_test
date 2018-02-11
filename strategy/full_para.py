# -*- coding: utf-8 -*-

from variable.constant import *
from strategy import __base_strategy

class Full_Para(__base_strategy.BaseStrategy):
    def __init__(self, charts):
        self.charts = charts

    def is_it_ok(self, subject_code, current_price):
        pass

    def is_it_sell(self, subject_code, current_price):
        pass

    def check_contract_in_candle(self, subject_code, index):
        # 고가 저가에서 is_it_ok 날리든 sar에서 날리든 어쨋든 체크해서 매매 리턴
        계약있냐 = True
        # if 계약있냐:
        #     return self.is_it_sell(subject_code, current_price)
        # else:
        #     return self.is_it_ok(subject_code, current_price)