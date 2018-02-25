# -*- coding: utf-8 -*-
from variable.constant import *
from strategy import __base_strategy
from indicator import ma
import math
import os
from variable import subject

class FullPara(__base_strategy.BaseStrategy):

    def __init__(self, charts: dict, subject_code: str, main_chart: str, strategy_var: dict, contracts: dict):
        super(FullPara, self).__init__()
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
        # 메인차트 Index가 부족 할 때 거래 안함
        if self.charts[self.main_chart_id].index < 3000:
            return None

        main_chart = self.charts[self.main_chart_id]
        para = main_chart.indicators[PARA][0]
        order_info = None
        if subject_code in self.contracts and FullPara.get_contract_count(subject_code, self.contracts, 풀파라) > 0:
            # 계약이 있을 때
            if para.FLOW == 상향:
                #현재캔들최고수익 = main_chart.candles.고가[main_chart.index + 1] - self.charts[self.main_chart_id].indicators[PARA][0].SARS[-1]
                최고가대비손절틱 = para.EP - main_chart.candles.저가[main_chart.index + 1]
                최고가대비손절틱 = math.floor(최고가대비손절틱 / subject.info[subject_code[:2]][단위]) * subject.info[subject_code[:2]][단위]

                if main_chart.candles.저가[main_chart.index + 1] < para.SAR:
                    # 반전시
                    price = math.floor(para.SAR * (1 / subject.info[subject_code[:2]][단위])) / (1 / subject.info[subject_code[:2]][단위])
                    self.log.info('하향 반전으로 is_it_sell() 콜, SAR : %s, current_price : %s' % (para.SAR, price))
                    order_info = self.is_it_sell(subject_code, price)

                # elif len(self.profit_tick) > 0 and 현재캔들최고수익 >= self.profit_tick[0][0] * subject.info[subject_code[:2]][단위]:
                #     # 익절틱
                #     price = self.charts[self.main_chart_id].indicators[PARA][0].SARS[-1] + self.profit_tick[0][0] * \
                #                                                                           subject.info[subject_code[:2]][단위]
                #     order_info = self.is_it_sell(subject_code, price)
                #     if order_info != None:
                #         self.profit_tick.pop(0)
                elif para.EP - math.ceil(para.SARS[-1] / subject.info[subject_code[:2]][단위]) * subject.info[subject_code[:2]][단위] >= self.profit_tick[0][0] * subject.info[subject_code[:2]][단위] and \
                    para.EP - main_chart.candles.저가[main_chart.index + 1] >= self.profit_dribble_tick[0] * subject.info[subject_code[:2]][단위]:
                    # 익절 수익 이후 익절드리블틱 이하로 가격이 떨어졌을 때
                    price = para.EP - self.profit_dribble_tick[0] * subject.info[subject_code[:2]][단위]
                    self.log.info("익절수익 이후 익절드리블 틱 이하로 가격이 떨어져 is_it_sell() 콜, 직전SAR: %s, 최고가 : %s, 현재가 : %s" % (
                    para.SARS[-1], para.EP, price))
                    order_info = self.is_it_sell(subject_code, price)

                elif len(self.sonjul_tick) > 0 and 최고가대비손절틱 >= self.sonjul_tick[0][0] * subject.info[subject_code[:2]][단위]:
                    # 손절틱
                    price = math.floor(para.SARS[-1] / subject.info[subject_code[:2]][단위]) * subject.info[subject_code[:2]][단위] - self.sonjul_tick[0][0] * subject.info[subject_code[:2]][단위]
                    self.log.info("손절틱 이상 떨어져 is_it_sell() 콜")
                    order_info = self.is_it_sell(subject_code, price)

            elif para.FLOW == 하향:
                최고가대비손절틱 = main_chart.candles.저가[main_chart.index + 1] - para.EP
                최고가대비손절틱 = math.floor(최고가대비손절틱 / subject.info[subject_code[:2]][단위]) * subject.info[subject_code[:2]][단위]

                if main_chart.candles.고가[main_chart.index + 1] > para.SAR:
                    # 반전시
                    price = math.ceil(para.SAR * (1 / subject.info[subject_code[:2]][단위])) / (1 / subject.info[subject_code[:2]][단위])
                    self.log.info('상향 반전으로 is_it_sell() 콜, SAR : %s, current_price : %s' % (para.SAR, price))
                    order_info = self.is_it_sell(subject_code, price)

                # elif len(self.profit_tick) > 0 and 현재캔들최고수익 >= self.profit_tick[0][0] * subject.info[subject_code[:2]][단위]:
                #     # 익절틱
                #     price = self.charts[self.main_chart_id].indicators[PARA][0].SARS[-1] + self.profit_tick[0][0] * \
                #                                                                           subject.info[subject_code[:2]][단위]
                #     order_info = self.is_it_sell(subject_code, price)
                #     if order_info != None:
                #         self.profit_tick.pop(0)
                elif math.floor(para.SARS[-1] / subject.info[subject_code[:2]][단위]) * subject.info[subject_code[:2]][단위] - para.EP >= self.profit_tick[0][0] * subject.info[subject_code[:2]][단위] and \
                    main_chart.candles.고가[main_chart.index + 1] - para.EP >= self.profit_dribble_tick[0] * subject.info[subject_code[:2]][단위]:
                    # 익절 수익 이후 익절드리블틱 이하로 가격이 떨어졌을 때
                    price = para.EP + self.profit_dribble_tick[0] * subject.info[subject_code[:2]][단위]
                    self.log.info("익절수익 이후 익절드리블 틱 이하로 가격이 떨어져 is_it_sell() 콜, 직전SAR: %s, 최저가 : %s, 현재가 : %s" % (para.SARS[-1], para.EP, price))
                    order_info = self.is_it_sell(subject_code, price)
                elif len(self.sonjul_tick) > 0 and 최고가대비손절틱 >= self.sonjul_tick[0][0] * subject.info[subject_code[:2]][단위]:
                    # 손절틱
                    price = math.ceil(para.SARS[-1] / subject.info[subject_code[:2]][단위]) * \
                            subject.info[subject_code[:2]][단위] + self.sonjul_tick[0][0] * \
                                                                 subject.info[subject_code[:2]][단위]
                    self.log.info("손절틱 이상 떨어져 is_it_sell() 콜")
                    order_info = self.is_it_sell(subject_code, price)

        else:
            # 계약이 없을 때
            if para.FLOW is 상향:
                if main_chart.candles.저가[main_chart.index + 1] < para.SAR:
                    # 하향 반전
                    current_price = math.floor(para.SAR * (1 / subject.info[subject_code[:2]][단위])) / (
                    1 / subject.info[subject_code[:2]][단위])
                    order_info = self.is_it_ok(subject_code, current_price)
                    self.log.debug('하향 반전, SAR : %s, current_price : %s' % (para.SAR, current_price))
            elif para.FLOW is 하향:
                if para.SAR < main_chart.candles.고가[main_chart.index + 1]:
                    # 상향 반전
                    current_price = math.ceil(para.SAR * (1 / subject.info[subject_code[:2]][단위])) / (1 / subject.info[subject_code[:2]][단위])
                    order_info = self.is_it_ok(subject_code, current_price)
                    self.log.debug('상향 반전, SAR : %s, current_price : %s' % (para.SAR, current_price))

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
                log.info("맞틀틀맞 다음으로 %s 진입.(pid = %s)" % ('신규매도' if _매도수구분 == 1 else '신규매수', self.pid))

        elif 파라.맞틀리스트[-3:] == [맞, 맞, 틀] and 직전플로우수익 < 0:
            if abs(파라.SARS[-4] - 파라.SARS[-3]) < abs(파라.SARS[-3] - 파라.SARS[-2]):
                log.debug("맞맞틀틀, 처음 맞 수익이 다음 맞 수익보다 적어서 %s 포기.(pid = %s)" % ('신규매도' if _매도수구분 == 1 else '신규매수', self.pid))
                return None
            else:
                log.info("맞맞틀틀 다음으로 %s 진입.(pid = %s)" % ('신규매도' if _매도수구분 == 1 else '신규매수', self.pid))

        elif 파라.맞틀리스트[-3:] == [맞, 틀, 틀] and 직전플로우수익 < 0:
            if 지지난플로우수익 < - 10:
                log.debug("맞틀틀틀, 지지난플로우수익 -10틱 미만으로 %s 포기.(pid = %s)" % ('신규매도' if _매도수구분 == 1 else '신규매수', self.pid))
                return None
            else:
                log.info("맞틀틀틀 다음으로 %s 진입.(pid = %s)" % ('신규매도' if _매도수구분 == 1 else '신규매수', self.pid))

        elif 파라.맞틀리스트[-2:] == [틀, 맞] and 직전플로우수익 < 0:
            if 지지난플로우수익 > 70:
                log.debug("틀맞맞, 지지난플로우수익 70틱 초과로 %s 포기.(pid = %s)" % ('신규매도' if _매도수구분 == 1 else '신규매수', self.pid))
                return None
            else:
                log.info("틀맞맞 다음으로 %s 진입.(pid = %s)" % ('신규매도' if _매도수구분 == 1 else '신규매수', self.pid))

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
            매매전략: 풀파라,
            수량: 2,
            가격: current_price
        }
        log.info("FullPara.is_it_ok(): %s, %s 진입.(pid = %s)" % (메인차트.candles.체결시간[메인차트.index], self.order_contents, self.pid))
        # 익절, 손절틱 복사
        self.profit_tick = self.strategy_var[익절틱][:]
        self.sonjul_tick = self.strategy_var[손절틱][:]
        self.profit_dribble_tick = self.strategy_var[수익드리블틱][:]
        self.sonjul_dribble_tick = self.strategy_var[손절드리블틱][:]

        return self.order_contents

    def is_it_sell(self, subject_code: str, current_price: float):
        log = self.log

        # 변수 선언
        메인차트 = self.charts[self.main_chart_id]
        파라 = 메인차트.indicators[PARA][0]
        현재플로우 = 파라.FLOW
        보유계약 = FullPara.get_contracts(subject_code, self.contracts, 풀파라)

        if 현재플로우 == 상향:
            최고가대비손절틱 = 파라.EP - current_price
            if len(self.sonjul_tick) > 0 and 최고가대비손절틱 >= self.sonjul_tick[0][0] * subject.info[subject_code[:2]][단위]:
                log.info("손절가가 되어 매수계약 청산 요청, 현재가 : %s(pid = %s)" % (current_price, self.pid))
                self.order_contents = {
                    신규주문: True,
                    종목코드: subject_code,
                    매도수구분: 신규매도,
                    매매전략: 풀파라,
                    수량: int(len(보유계약) * self.sonjul_tick[0][1]),
                    가격: current_price
                }

                self.sonjul_tick.pop(0)
                if len(self.sonjul_dribble_tick) > 0:
                    self.sonjul_dribble_tick.pop(0)
                return self.order_contents

            if 파라.EP - math.ceil(파라.SARS[-1] / subject.info[subject_code[:2]][단위]) * subject.info[subject_code[:2]][단위] >= self.profit_tick[0][0] * subject.info[subject_code[:2]][단위] and \
                                    파라.EP - 메인차트.candles.저가[메인차트.index + 1] >= self.profit_dribble_tick[0] * subject.info[subject_code[:2]][단위]:
                log.info("익절드리블 후(%s틱) 손절가가 되어 매수계약 청산 요청, 현재가 : %s(pid = %s)" % ((current_price - math.ceil(파라.SARS[-1] / subject.info[subject_code[:2]][단위]) * subject.info[subject_code[:2]][단위]) / subject.info[subject_code[:2]][단위], current_price, self.pid))

                self.order_contents = {
                    신규주문: True,
                    종목코드: subject_code,
                    매도수구분: 신규매도,
                    매매전략: 풀파라,
                    수량: int(len(보유계약) * self.profit_tick[0][1]),
                    가격: current_price
                }

                self.profit_tick.pop(0)
                if len(self.profit_dribble_tick) > 0:
                    self.profit_dribble_tick.pop(0)

                return self.order_contents

            if current_price < 파라.SAR:
                log.info("하향 반전으로 매수계약 청산 요청, 현재가 : %s(pid = %s)" % (current_price, self.pid))
                self.order_contents = {
                    신규주문: True,
                    종목코드: subject_code,
                    매도수구분: 신규매도,
                    매매전략: 풀파라,
                    수량: len(보유계약),
                    가격: current_price
                }
                return self.order_contents
        elif 현재플로우 == 하향:
            최고가대비손절틱 = current_price - 파라.EP
            if len(self.sonjul_tick) > 0 and 최고가대비손절틱 >= self.sonjul_tick[0][0] * subject.info[subject_code[:2]][단위]:
                log.info("손절가가 되어 매도계약 청산 요청, 현재가 : %s(pid = %s)" % (current_price, self.pid))
                self.order_contents = {
                    신규주문: True,
                    종목코드: subject_code,
                    매도수구분: 신규매수,
                    매매전략: 풀파라,
                    수량: int(len(보유계약) * self.sonjul_tick[0][1]),
                    가격: current_price
                }

                log.debug(self.order_contents)
                self.sonjul_tick.pop(0)
                if len(self.sonjul_dribble_tick) > 0:
                    self.sonjul_dribble_tick.pop(0)
                return self.order_contents

            if math.floor(파라.SARS[-1] / subject.info[subject_code[:2]][단위]) * subject.info[subject_code[:2]][단위] - 파라.EP >= self.profit_tick[0][0] * subject.info[subject_code[:2]][단위] and \
                                    메인차트.candles.고가[메인차트.index + 1] - 파라.EP >= self.profit_dribble_tick[0] * \
                            subject.info[subject_code[:2]][단위]:
                log.info("익절드리블 후(%s틱) 손절가가 되어 매도계약 청산 요청, 현재가 : %s(pid = %s)" % ((math.floor(파라.SARS[-1] / subject.info[subject_code[:2]][단위]) * subject.info[subject_code[:2]][단위] - current_price) / subject.info[subject_code[:2]][단위], current_price, self.pid))
                self.order_contents = {
                    신규주문: True,
                    종목코드: subject_code,
                    매도수구분: 신규매수,
                    매매전략: 풀파라,
                    수량: int(len(보유계약) * self.profit_tick[0][1]),
                    가격: current_price
                }

                self.profit_tick.pop(0)
                if len(self.profit_dribble_tick) > 0:
                    self.profit_dribble_tick.pop(0)

                return self.order_contents

            if current_price > 파라.SAR:
                log.info("상향 반전으로 매도계약 청산 요청, 현재가 : %s(pid = %s)" % (current_price, self.pid))
                self.order_contents = {
                    신규주문: True,
                    종목코드: subject_code,
                    매도수구분: 신규매수,
                    매매전략: 풀파라,
                    수량: len(보유계약),
                    가격: current_price
                }
                return self.order_contents

        return None

