# -*- coding: utf-8 -*-
from variable.constant import *
from strategy import __base_strategy
from indicator import ma
import math
from variable import subject
import os

class FullPara(__base_strategy.BaseStrategy):

    def __init__(self, charts: dict, subject_code: str, main_chart: str, strategy_var: dict):
        super(FullPara, self).__init__()
        self.charts = charts
        self.main_chart_id = subject_code + '_' + main_chart
        self.strategy_var = strategy_var
        self.pid = os.getpid()
        self.order_contents = {}

    def check_contract_in_candle(self, subject_code: str, contracts: dict):
        # 메인차트 Index가 부족 할 때 거래 안함
        if self.charts[self.main_chart_id].index < 3000:
            return None

        main_chart = self.charts[self.main_chart_id]
        para = main_chart.indicators[PARA][0]
        order_info = None
        if subject_code in contracts and len(contracts[subject_code]) > 0:
            # 계약이 있을 때
            pass
        else:
            # 계약이 없을 때
            if para.FLOW is 상향:
                if main_chart.candles.저가[main_chart.index + 1] < para.SAR:
                    # 하향 반전
                    current_price = math.floor(para.SAR * (1 / subject.info[subject_code[:2]][단위])) / (
                    1 / subject.info[subject_code[:2]][단위])
                    order_info = self.is_it_ok(subject_code, current_price)
                    # print('하향 반전, SAR : %s, current_price : %s' % (para.SAR, current_price))
            elif para.FLOW is 하향:
                if para.SAR < main_chart.candles.고가[main_chart.index + 1]:
                    # 상향 반전
                    current_price = math.ceil(para.SAR * (1 / subject.info[subject_code[:2]][단위])) / (1 / subject.info[subject_code[:2]][단위])
                    order_info = self.is_it_ok(subject_code, current_price)
                    # print('상향 반전, SAR : %s, current_price : %s' % (para.SAR, current_price))

        return order_info

    def check_contract_in_tick(self, subject_code, current_price):
        pass

    def is_it_ok(self, subject_code: str, current_price: float):
        log = self.log

        # 변수 선언
        메인차트 = self.charts[self.main_chart_id]
        _매도수구분 = None
        직전플로우수익 = 0
        파라 = 메인차트.indicators[PARA][0]
        현재플로우 = 파라.FLOW

        # 반전 확인
        if 현재플로우 == 상향 and current_price < 파라.SAR:
            # 하향 반전
            직전플로우수익 = (파라.SARS[-1] - current_price) / subject.info[subject_code[:2]][단위]
            log.debug("하향 반전, 현재가 : %s, 직전플로우수익 : %s(pid = %s)" % (current_price, 직전플로우수익, self.pid))

            if ma.Calc.is_sorted(메인차트.indicators[MA]) == 하락세:
                _매도수구분 = 신규매도
            else:
                log.debug("이동평균선이 맞지 않아 매도 포기.(pid = %s)" % self.pid)
        elif 현재플로우 == 하향 and current_price > 파라.SAR:
            # 상향 반전
            직전플로우수익 = (current_price - 파라.SARS[-1]) / subject.info[subject_code[:2]][단위]
            log.debug("상향 반전, 현재가 : %s, 직전플로우수익 : %s(pid = %s)" % (current_price, 직전플로우수익, self.pid))

            if ma.Calc.is_sorted(메인차트.indicators[MA]) == 상승세:
                _매도수구분 = 신규매수
            else:
                log.debug("이동평균선이 맞지 않아 매도 포기.(pid = %s)" % self.pid)

        if _매도수구분 is None:
            return None

        # 맞틀리스트 확인
        지지난플로우수익 = abs(파라.SARS[-1] - 파라.SARS[-2]) # 계산의 편의를 위해 절대값을 취함.

        if 파라.맞틀리스트[-1] == 맞 and 직전플로우수익 < 0 and 지지난플로우수익 > 70:
            # 맞틀리스트[-1]이 맞이므로 지지난플로우수익은 항상 양수
            log.debug("지지난 플로우가 70틱 이상 수익으로 %s 포기.(pid = %s)" % ('신규매도' if _매도수구분 == 1 else '신규매수', self.pid))
            return None

        if 파라.맞틀리스트[-3:] == [틀, 틀, 틀] and 직전플로우수익 < 0:
            # 맞틀리스트가 틀틀틀틀 이므로 지지난플로우수익은 항상 음수
            지지난플로우수익 = abs(파라.SARS[-1] - 파라.SARS[-2])
            if 지지난플로우수익 < abs(직전플로우수익) and 지지난플로우수익 < 15:
                log.debug("틀틀틀틀 조건에 맞지 않아 %s 포기.(pid = %s)" % ('신규매도' if _매도수구분 == 1 else '신규매수', self.pid))
                return None
            else:
                log.debug("틀틀틀틀 다음으로 %s 진입.(pid = %s)" % ('신규매도' if _매도수구분 == 1 else '신규매수', self.pid))

        elif 파라.맞틀리스트[-3:] == [틀, 맞, 맞] and 직전플로우수익 < 0:
            log.debug("틀맞맞틀 다음으로 %s 진입.(pid = %s)" % ('신규매도' if _매도수구분 == 1 else '신규매수',  self.pid))

        elif 파라.맞틀리스트[-3:] == [틀, 맞, 틀] and 직전플로우수익 < 0:
            log.debug("틀맞틀틀 다음으로 %s 진입.(pid = %s)" % ('신규매도' if _매도수구분 == 1 else '신규매수',  self.pid))

        elif 파라.맞틀리스트[-3:] == [맞, 틀, 틀] and 직전플로우수익 > 0:
            if 직전플로우수익 > 10:
                log.debug("맞틀틀맞, 직전플로우 수익이 10틱 초과로 %s 포기.(pid = %s)" % ('신규매도' if _매도수구분 == 1 else '신규매수', self.pid))
                return None
            else:
                log.debug("맞틀틀맞 다음으로 %s 진입.(pid = %s)" % ('신규매도' if _매도수구분 == 1 else '신규매수', self.pid))

        elif 파라.맞틀리스트[-3:] == [맞, 맞, 틀] and 직전플로우수익 < 0:
            if abs(파라.SARS[-4] - 파라.SARS[-3]) < abs(파라.SARS[-3] - 파라.SARS[-2]):
                log.debug("맞맞틀틀, 처음 맞 수익이 다음 맞 수익보다 적어서 %s 포기.(pid = %s)" % ('신규매도' if _매도수구분 == 1 else '신규매수', self.pid))
                return None
            else:
                log.debug("맞맞틀틀 다음으로 %s 진입.(pid = %s)" % ('신규매도' if _매도수구분 == 1 else '신규매수', self.pid))

        elif 파라.맞틀리스트[-3:] == [맞, 틀, 틀] and 직전플로우수익 < 0:
            if 지지난플로우수익 < - 10:
                log.debug("맞틀틀틀, 지지난플로우수익 -10틱 미만으로 %s 포기.(pid = %s)" % ('신규매도' if _매도수구분 == 1 else '신규매수', self.pid))
                return None
            else:
                log.debug("맞틀틀틀 다음으로 %s 진입.(pid = %s)" % ('신규매도' if _매도수구분 == 1 else '신규매수', self.pid))

        elif 파라.맞틀리스트[-2:] == [틀, 맞] and 직전플로우수익 < 0:
            if 지지난플로우수익 > 70:
                log.debug("틀맞맞, 지지난플로우수익 70틱 초과로 %s 포기.(pid = %s)" % ('신규매도' if _매도수구분 == 1 else '신규매수', self.pid))
                return None
            else:
                log.debug("틀맞맞 다음으로 %s 진입.(pid = %s)" % ('신규매도' if _매도수구분 == 1 else '신규매수', self.pid))

        else:
            log.debug("맞틀 조건에 맞지 않아 %s 포기.(pid = %s)" % ('신규매도' if _매도수구분 == 1 else '신규매수', self.pid))
            return None

        # 매매시간 확인
        if subject_code == 'GCG18':
            pass
        else:
            pass

        # 매매진입
        self.order_contents = {
            신규주문: True,
            종목코드: subject_code,
            매도수구분: _매도수구분,
            수량: 2,
            가격: current_price
        }
        log.debug("FullPara.is_it_ok(): %s 진입.(pid = %s)" % (self.order_contents, self.pid))

        # 익절, 손절틱 복사
        self.profit_tick = self.strategy_var[익절틱]
        #self.sonjul_tick = self.strategy_var[손절틱]

        return self.order_contents

    def is_it_sell(self, subject_code, current_price):
        return None
