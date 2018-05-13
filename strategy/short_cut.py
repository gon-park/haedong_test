# -*- coding: utf-8 -*-
from variable.constant import *
from strategy import __base_strategy
from indicator import ma, rsi
import math
import os
from variable import subject
from variable.report import Report


class ShortCut(__base_strategy.BaseStrategy):

    def __init__(self, charts: dict, subject_code: str, main_chart: str, strategy_var: dict, contracts: dict):
        super(ShortCut, self).__init__()
        self.charts = charts
        self.main_chart_id = subject_code + '_' + main_chart
        self.strategy_var = strategy_var
        self.pid = os.getpid()
        self.order_contents = {}
        self.contracts = contracts

    def print(self):
        from pprint import pprint
        pass

    def check_contract_in_candle(self, subject_code: str, current_price: float):
        order_info = None

        main_chart = self.charts[self.main_chart_id]

        if main_chart.index < 10: return None

        if subject_code in self.contracts and ShortCut.get_contract_count(subject_code, self.contracts, ShortCut) > 0:
            # 계약 있을 때
            contracts = self.get_contracts(subject_code, self.contracts, ShortCut)
            현재캔들 = main_chart.candles.iloc[main_chart.index + 1]

            for price in 현재캔들.price_list.split(','):
                if contracts[0].매도수구분 == 신규매수:
                    self.strategy_var[최극가] = max(float(self.strategy_var[최극가]), float(price))
                else:
                    self.strategy_var[최극가] = min(float(self.strategy_var[최극가]), float(price))

                order_info = self.is_it_sell(subject_code, float(price))

                if order_info is not None:
                    return order_info

        else:
            보조캔들 = main_chart.candles.iloc[main_chart.index]
            기준캔들 = main_chart.candles.iloc[main_chart.index - 1]

            #self.log.debug("기준캔들 시간: %s" % 기준캔들.date)
            if 기준캔들.volume < self.strategy_var[기준거래량]:
                #self.log.debug("기준캔들.volume(%s) < self.strategy_var[기준거래량](%s)" % (기준캔들.volume, self.strategy_var[기준거래량]))
                return None

            if 기준캔들.high - 기준캔들.low < self.strategy_var[기준캔들길이] * subject.info[subject_code[:2]][단위]:
                #self.log.debug("기준캔들.high - 기준캔들.low(%s) < self.strategy_var[기준캔들길이] * subject.info[subject_code[:2]][단위](%s)" % (기준캔들.high - 기준캔들.low, self.strategy_var[기준캔들길이] * subject.info[subject_code[:2]][단위]))
                return None

            if abs(기준캔들.open - 기준캔들.close) < self.strategy_var[기준캔들몸통길이] * subject.info[subject_code[:2]][단위]:
                #self.log.debug("abs(기준캔들.open - 기준캔들.close)(%s) < self.strategy_var[기준캔들몸통길이] * subject.info[subject_code[:2]][단위](%s)" % (abs(기준캔들.open - 기준캔들.close), self.strategy_var[기준캔들몸통길이] * subject.info[subject_code[:2]][단위]))
                return None

            if 보조캔들.volume > 기준캔들.volume * self.strategy_var[거래량비]:
                #self.log.debug("보조캔들.volume(%s) > 기준캔들.volume * self.strategy_var[거래량비](%s)" % (보조캔들.volume, 기준캔들.volume * self.strategy_var[거래량비]))
                return None

            if abs(보조캔들.open - 보조캔들.close) > self.strategy_var[보조캔들몸통길이] * subject.info[subject_code[:2]][단위]:
                #self.log.debug("abs(보조캔들.open - 보조캔들.close)(%s) > self.strategy_var[보조캔들몸통길이] * subject.info[subject_code[:2]][단위](%s)" % (abs(보조캔들.open - 보조캔들.close), self.strategy_var[보조캔들몸통길이] * subject.info[subject_code[:2]][단위]))
                return None

            _매도수구분 = 신규매수 if 기준캔들.close < 기준캔들.open else 신규매도

            if _매도수구분 == 신규매수:
                if (기준캔들.close - 기준캔들.open) * (보조캔들.close - 보조캔들.open) > 0 and \
                                보조캔들.open == 보조캔들.low and \
                                보조캔들.close == 보조캔들.high:
                    return None

            if _매도수구분 == 신규매도:
                if (기준캔들.close - 기준캔들.open) * (보조캔들.close - 보조캔들.open) > 0 and \
                                보조캔들.open == 보조캔들.high and \
                                보조캔들.close == 보조캔들.low:
                    return None

            order_info = {
                신규주문: True,
                종목코드: subject_code,
                매도수구분: _매도수구분,
                매매전략: ShortCut,
                수량: 1,
                가격: current_price
            }

            self.strategy_var[최극가] = current_price

        return order_info

    def check_contract_in_tick(self, subject_code, current_price):
        pass

    def is_it_ok(self, subject_code: str, current_price: float):
        log = self.log

        return self.order_contents

    def is_it_sell(self, subject_code: str, current_price: float):
        log = self.log
        contracts = self.get_contracts(subject_code, self.contracts, ShortCut)

        order_info = None

        if contracts[0].매도수구분 == 신규매수:
            if round((current_price - contracts[0].체결표시가격) / subject.info[subject_code[:2]][단위]) >= self.strategy_var[익절틱][1][0]:
                log.debug("매수 중 익절 청산")
                order_info = {
                    신규주문: True,
                    종목코드: subject_code,
                    매도수구분: 신규매도,
                    매매전략: ShortCut,
                    수량: 1,
                    가격: current_price
                }
            elif round((self.strategy_var[최극가] - contracts[0].체결표시가격) / subject.info[subject_code[:2]][단위]) >= self.strategy_var[익절틱][0][0] and \
                                    round((self.strategy_var[최극가] - current_price) / subject.info[subject_code[:2]][단위]) >= self.strategy_var[수익드리블틱][0]:
                # 익절 드리블 중 청산
                # log.debug("round((self.strategy_var[최극가] - contracts[0].체결표시가격) / subject.info[subject_code[:2]][단위]) : %s" % round((self.strategy_var[최극가] - contracts[0].체결표시가격) / subject.info[subject_code[:2]][단위]))
                # log.debug("(round(self.strategy_var[최극가] - current_price)) / subject.info[subject_code[:2]][단위] : %s" % round((self.strategy_var[최극가] - current_price) / subject.info[subject_code[:2]][단위]))
                log.debug("매수 중 드리블 청산.")
                order_info = {
                    신규주문: True,
                    종목코드: subject_code,
                    매도수구분: 신규매도,
                    매매전략: ShortCut,
                    수량: 1,
                    가격: current_price
                }
            elif round((contracts[0].체결표시가격 - current_price) / subject.info[subject_code[:2]][단위]) >= self.strategy_var[손절틱][0][0]:
                # 손절 청산
                log.debug("매수 중 손절 청산.")
                order_info = {
                    신규주문: True,
                    종목코드: subject_code,
                    매도수구분: 신규매도,
                    매매전략: ShortCut,
                    수량: 1,
                    가격: current_price
                }
        else:
            if round((contracts[0].체결표시가격 - current_price) / subject.info[subject_code[:2]][단위]) >= self.strategy_var[익절틱][1][0]:
                log.debug("매도 중 익절 청산")
                order_info = {
                    신규주문: True,
                    종목코드: subject_code,
                    매도수구분: 신규매수,
                    매매전략: ShortCut,
                    수량: 1,
                    가격: current_price
                }
            elif round((contracts[0].체결표시가격 - self.strategy_var[최극가]) / subject.info[subject_code[:2]][단위]) >= self.strategy_var[익절틱][0][0] and \
                                    round((current_price - self.strategy_var[최극가]) / subject.info[subject_code[:2]][단위]) >= self.strategy_var[수익드리블틱][0]:
                # 익절 드리블 중 청산
                log.debug("매도 중 드리블 청산.")
                order_info = {
                    신규주문: True,
                    종목코드: subject_code,
                    매도수구분: 신규매수,
                    매매전략: ShortCut,
                    수량: 1,
                    가격: current_price
                }
            elif round((current_price - contracts[0].체결표시가격) / subject.info[subject_code[:2]][단위]) >= self.strategy_var[손절틱][0][0]:
                # 손절 청산
                log.debug("매도 중 손절 청산.")
                order_info = {
                    신규주문: True,
                    종목코드: subject_code,
                    매도수구분: 신규매수,
                    매매전략: ShortCut,
                    수량: 1,
                    가격: current_price
                }
        return order_info

    def post_trade(self, report: Report):
        pass

