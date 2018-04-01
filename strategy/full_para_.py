# -*- coding: utf-8 -*-
import pprint

from variable.constant import *
from strategy import __base_strategy
from indicator import ma, para as indicator_para
import math
import os
from variable import subject
from variable.report import Report
from variable.reports import Reports


class FullPara(__base_strategy.BaseStrategy):

    def __init__(self, charts: dict, subject_code: str, main_chart: str, strategy_var: dict, contracts: dict):
        super(FullPara, self).__init__()
        self.stats_true_false_list = {}
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
        # 메인차트 = self.charts[self.main_chart_id]
        self.main_chart = self.charts[self.main_chart_id]
        self.para = self.main_chart.indicators[PARA][0]

    def check_contract_in_candle(self, subject_code: str):
        # 메인차트 Index가 부족 할 때 거래 안함
        if self.charts[self.main_chart_id].index < 3000:
            return None

        para = self.para
        main_chart = self.main_chart

        order_info = None

        # 계약이 있을 때
        if subject_code in self.contracts and FullPara.get_contract_count(subject_code, self.contracts, 풀파라) > 0:
            보유계약 = FullPara.get_contracts(subject_code, self.contracts, 풀파라)
            if para.FLOW == 상향:
                if para.SAR > main_chart.candles.저가[main_chart.index + 1] or \
                    (len(self.profit_tick) > 0 and max(para.EP, main_chart.candles.고가[main_chart.index + 1]) - 보유계약[0].체결표시가격 >= self.profit_tick[0][0] * subject.info[subject_code[:2]][단위] and \
                    max(para.EP, main_chart.candles.고가[main_chart.index + 1]) - main_chart.candles.저가[main_chart.index + 1] >= self.profit_dribble_tick[0] * subject.info[subject_code[:2]][단위]) or \
                    (len(self.sonjul_tick) > 0 and round((para.EP - main_chart.candles.저가[main_chart.index + 1]) / subject.info[subject_code[:2]][단위]) >= self.sonjul_tick[0][0]):

                    for price in main_chart.candles.가격들[main_chart.index + 1]:
                        if para.EP < price: para.EP = price

                        최고가대비손절틱 = para.EP - price
                        최고가대비손절틱 = round(최고가대비손절틱 / subject.info[subject_code[:2]][단위]) * subject.info[subject_code[:2]][단위]

                        if price < para.SAR:
                            # 반전시
                            self.log.debug('하향 반전으로 is_it_sell() 콜, SAR : %s, current_price : %s' % (para.SAR, price))
                            order_info = self.is_it_sell(subject_code, price)

                        elif len(self.profit_tick) > 0 and para.EP - 보유계약[0].체결표시가격 >= self.profit_tick[0][0] * subject.info[subject_code[:2]][단위] and \
                            para.EP - price >= self.profit_dribble_tick[0] * subject.info[subject_code[:2]][단위]:
                            # 익절 수익 이후 익절드리블틱 이하로 가격이 떨어졌을 때
                            self.log.debug("익절수익 이후 익절드리블 틱(%s) 이하로 가격이 떨어져 is_it_sell() 콜, %s, 직전SAR: %s, 최고가 : %s, 현재가 : %s" % (self.profit_dribble_tick[0],main_chart.candles.체결시간[main_chart.index+1], para.SARS[-1], para.EP, price))
                            order_info = self.is_it_sell(subject_code, price)

                        elif len(self.sonjul_tick) > 0 and 최고가대비손절틱 >= self.sonjul_tick[0][0] * subject.info[subject_code[:2]][단위]:
                            # 손절틱
                            self.log.debug("손절틱(%s) 이상 떨어져 is_it_sell() 콜, 시간:%s" % (self.sonjul_tick[0][0],main_chart.candles.체결시간[main_chart.index+1]))
                            order_info = self.is_it_sell(subject_code, price)

                        if order_info is not None: break

            elif para.FLOW == 하향:
                if para.SAR < main_chart.candles.고가[main_chart.index + 1] or \
                    (len(self.profit_tick) > 0 and 보유계약[0].체결표시가격 - min(para.EP, main_chart.candles.저가[main_chart.index + 1]) >= self.profit_tick[0][0] * subject.info[subject_code[:2]][단위] and \
                    main_chart.candles.고가[main_chart.index + 1] - min(para.EP, main_chart.candles.저가[main_chart.index + 1]) >= self.profit_dribble_tick[0] * subject.info[subject_code[:2]][단위]) or \
                    (len(self.sonjul_tick) > 0 and round((main_chart.candles.고가[main_chart.index + 1] - para.EP) / subject.info[subject_code[:2]][단위]) >= self.sonjul_tick[0][0]):

                    for price in main_chart.candles.가격들[main_chart.index + 1]:
                        if para.EP > price: para.EP = price

                        최고가대비손절틱 = price - para.EP
                        최고가대비손절틱 = round(최고가대비손절틱 / subject.info[subject_code[:2]][단위]) * subject.info[subject_code[:2]][단위]

                        if price > para.SAR:
                            # 반전시
                            self.log.debug('상향 반전으로 is_it_sell() 콜, SAR : %s, current_price : %s' % (para.SAR, price))
                            order_info = self.is_it_sell(subject_code, price)

                        elif len(self.profit_tick) > 0 and 보유계약[0].체결표시가격 - para.EP >= self.profit_tick[0][0] * subject.info[subject_code[:2]][단위] and \
                            price - para.EP >= self.profit_dribble_tick[0] * subject.info[subject_code[:2]][단위]:
                            # 익절 수익 이후 익절드리블틱 이하로 가격이 떨어졌을 때
                            self.log.debug("익절수익 이후 익절드리블 틱(%s) 이하로 가격이 떨어져 is_it_sell() 콜. %s, 직전SAR: %s, 최저가 : %s, 현재가 : %s" % (self.profit_dribble_tick[0],main_chart.candles.체결시간[main_chart.index+1], para.SARS[-1], para.EP, price))
                            order_info = self.is_it_sell(subject_code, price)
                        elif len(self.sonjul_tick) > 0 and 최고가대비손절틱 >= self.sonjul_tick[0][0] * subject.info[subject_code[:2]][단위]:
                            # 손절틱
                            self.log.debug("손절틱(%s) 이상 떨어져 is_it_sell() 콜, 시간:%s" % (self.sonjul_tick[0][0],main_chart.candles.체결시간[main_chart.index+1]))
                            order_info = self.is_it_sell(subject_code, price)

                        if order_info is not None: break

            # 맞틀 리스트 별 승률, 수익 계산
            if order_info is not None:
                key = ''
                contract = self.contracts[order_info[종목코드]][0]
                체결가 = order_info[가격] - subject.info[contract.종목코드[:2]][단위]\
                    if order_info[매도수구분] is 신규매도\
                    else order_info[가격] + subject.info[contract.종목코드[:2]][단위]  # 슬리피지

                profit = (contract.체결표시가격 - 체결가) / subject.info[order_info[종목코드][:2]][단위] * subject.info[order_info[종목코드][:2]][틱가치]\
                    if contract.매도수구분 is 신규매도\
                    else (체결가 - contract.체결표시가격) / subject.info[order_info[종목코드][:2]][단위] * subject.info[order_info[종목코드][:2]][틱가치]

                for i in range(-1, -6, -1):
                    key = ('맞' if para.맞틀리스트[i] else '틀') + key
                    if key not in self.stats_true_false_list:
                        self.stats_true_false_list[key] = {}
                        self.stats_true_false_list[key]['수익'] = 0
                        self.stats_true_false_list[key]['승'] = 0
                        self.stats_true_false_list[key]['패'] = 0

                    self.stats_true_false_list[key]['수익'] += profit
                    if profit > 0:
                        self.stats_true_false_list[key]['승'] += 1
                    else:
                        self.stats_true_false_list[key]['패'] += 1

        # 계약이 없을 때
        else:
            if main_chart.candles.영업일[main_chart.index + 1] != main_chart.candles.영업일[main_chart.index]:
                return order_info

            if para.FLOW is 상향:
                if main_chart.candles.저가[main_chart.index + 1] < para.SAR:
                    for price in main_chart.candles.가격들[main_chart.index + 1]:
                        if price < para.SAR:
                            # 하향 반전
                            current_price = math.floor(para.SAR * (1 / subject.info[subject_code[:2]][단위])) / ( 1 / subject.info[subject_code[:2]][단위])
                            self.log.debug('하향 반전, SAR : %s, current_price : %s' % (para.SAR, current_price))
                            #current_price = current_price - subject.info[subject_code[:2]][단위]
                            order_info = self.is_it_ok(subject_code, current_price)
                            break

            elif para.FLOW is 하향:
                if para.SAR < main_chart.candles.고가[main_chart.index + 1]:
                    for price in main_chart.candles.가격들[main_chart.index + 1]:
                        if para.SAR < price:
                            # 상향 반전
                            current_price = math.ceil(para.SAR * (1 / subject.info[subject_code[:2]][단위])) / (1 / subject.info[subject_code[:2]][단위])
                            self.log.debug('상향 반전, SAR : %s, current_price : %s' % (para.SAR, current_price))
                            #current_price = current_price + subject.info[subject_code[:2]][단위]
                            order_info = self.is_it_ok(subject_code, current_price)
                            break

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
            직전플로우수익 = (current_price-파라.SARS[-1]) / subject.info[subject_code[:2]][단위]
            log.debug("하향 반전, 현재가 : %s, 직전플로우수익 : %s(pid = %s) 시간:%s" % (current_price, 직전플로우수익, self.pid, 메인차트.candles.체결시간[메인차트.index+1]))

            _매도수구분 = 신규매도
            # if ma.Calc.is_sorted(메인차트.indicators[MA]) == 하락세:
            #     _매도수구분 = 신규매도
            # else:
            #     log.debug("이동평균선이 맞지 않아 매도 포기.(pid = %s)" % self.pid)

        elif 현재플로우 == 하향 and current_price > 파라.SAR:
            # 상향 반전
            직전플로우수익 = (파라.SARS[-1] - current_price) / subject.info[subject_code[:2]][단위]
            log.debug("상향 반전, 현재가 : %s, 직전플로우수익 : %s(pid = %s) 시간:%s" % (current_price, 직전플로우수익, self.pid, 메인차트.candles.체결시간[메인차트.index+1]))

            _매도수구분 = 신규매수
            # if ma.Calc.is_sorted(메인차트.indicators[MA]) == 상승세:
            #     _매도수구분 = 신규매수
            # else:
            #     log.debug("이동평균선이 맞지 않아 매도 포기.(pid = %s)" % self.pid)

        if _매도수구분 is None:
            return None

        # # 매매시간 확인
        # 매매시간 = int(메인차트.candles.체결시간[메인차트.index + 1].strftime("%H%M"))
        # if subject_code == 'GCG18' or subject_code == 'GCJ18':
        #     if 2200 < 매매시간 < 2330:
        #         log.debug("22:00 ~ 23:30 사이라 매매 포기.")
        #         return None
        # else:
        #     if 2100 < 매매시간 < 2230:
        #         log.debug("21:00 ~ 22:30 사이라 매매 포기.")
        #         return None


        # 매매진입
        self.order_contents = {
            신규주문: True,
            종목코드: subject_code,
            매도수구분: _매도수구분,
            매매전략: 풀파라,
            수량: 2,
            가격: current_price
        }
        log.info("FullPara.is_it_ok(): %s, %s 진입.(pid = %s)" % (메인차트.candles.체결시간[메인차트.index+1], self.order_contents, self.pid))
        # 익절, 손절틱 복사
        self.profit_tick = self.strategy_var[익절틱][:]
        self.sonjul_tick = self.strategy_var[손절틱][:]
        self.profit_dribble_tick = self.strategy_var[수익드리블틱][:]
        self.sonjul_dribble_tick = self.strategy_var[손절드리블틱][:]

        return self.order_contents

    def is_it_sell(self, subject_code: str, current_price: float):
        log = self.log

        # 변수 선언
        현재플로우 = self.para.FLOW
        보유계약 = FullPara.get_contracts(subject_code, self.contracts, 풀파라)
        para = self.para
        main_chart = self.main_chart

        if 현재플로우 == 상향:
            최고가대비손절틱 = para.EP - current_price
            log.info("최고가대비손절틱:"+str(최고가대비손절틱))
            log.info("EP:"+str(para.EP))
            log.info("현재가:"+str(current_price))
            if len(self.sonjul_tick) > 0 and 최고가대비손절틱 >= self.sonjul_tick[0][0] * subject.info[subject_code[:2]][단위]:
                log.info("손절가가 되어 매수계약(%s계약) 청산 요청, 체결시간 : %s, 현재가 : %s(pid = %s)" % (int(len(보유계약) * self.sonjul_tick[0][1]),main_chart.candles.체결시간[main_chart.index+1], current_price, self.pid))
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

            if len(self.profit_tick) > 0 and para.EP - 보유계약[0].체결표시가격 >= self.profit_tick[0][0] * subject.info[subject_code[:2]][단위] and \
                                    para.EP - main_chart.candles.저가[main_chart.index + 1] >= self.profit_dribble_tick[0] * subject.info[subject_code[:2]][단위]:
                log.info("익절드리블 후(%s틱) 손절가가 되어 매수계약(%s계약) 청산 요청, 체결시간 : %s, 현재가 : %s(pid = %s)" % ((current_price - math.ceil(para.SARS[-1] / subject.info[subject_code[:2]][단위]) * subject.info[subject_code[:2]][단위]) / subject.info[subject_code[:2]][단위], int(len(보유계약) * self.profit_tick[0][1]), main_chart.candles.체결시간[main_chart.index+1], current_price, self.pid))

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

            if current_price < para.SAR:
                log.info("하향 반전으로 모든 매수계약 청산 요청, 체결시간 : %s, 현재가 : %s(pid = %s)" % (main_chart.candles.체결시간[main_chart.index+1], current_price, self.pid))
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
            최고가대비손절틱 = current_price - para.EP

            log.info("최고가대비손절틱:"+str(최고가대비손절틱))
            log.info("EP:"+str(para.EP))
            log.info("현재가:"+str(current_price))

            if len(self.sonjul_tick) > 0 and 최고가대비손절틱 >= self.sonjul_tick[0][0] * subject.info[subject_code[:2]][단위]:
                log.info("손절가가 되어 매도계약(%s계약) 청산 요청, 체결시간 : %s, 현재가 : %s(pid = %s)" % (int(len(보유계약) * self.sonjul_tick[0][1]),main_chart.candles.체결시간[main_chart.index+1], current_price, self.pid))
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

            if len(self.profit_tick) > 0 and 보유계약[0].체결표시가격 - para.EP >= self.profit_tick[0][0] * subject.info[subject_code[:2]][단위] and \
                                    main_chart.candles.고가[main_chart.index + 1] - para.EP >= self.profit_dribble_tick[0] * \
                            subject.info[subject_code[:2]][단위]:
                log.info("익절드리블 후(%s틱) 손절가가 되어 매도계약(%s계약) 청산 요청, 체결시간 : %s, 현재가 : %s(pid = %s)" % ((math.floor(para.SARS[-1] / subject.info[subject_code[:2]][단위]) * subject.info[subject_code[:2]][단위] - current_price) / subject.info[subject_code[:2]][단위], main_chart.candles.체결시간[main_chart.index+1], int(len(보유계약) * self.profit_tick[0][1]),current_price, self.pid))
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

            if current_price > para.SAR:
                log.info("상향 반전으로 모든 매도계약 청산 요청, 체결시간 : %s, 현재가 : %s(pid = %s)" % (main_chart.candles.체결시간[main_chart.index+1], current_price, self.pid))
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

    def post_trade(self, report: Report):
        report.맞틀리스트 = self.stats_true_false_list

    @staticmethod
    def calc_reports(reports_list: list):

        모든맞틀수익 = {}
        for reports in reports_list:
            reports.맞틀수익 = {}

            # reports_list 안에 있는 reports 안에 있는 월물 list[Report]들의 수익 합을 계산
            for report in reports.월물:
                for key in report.맞틀리스트:
                    if key not in reports.맞틀수익:
                        reports.맞틀수익[key] = {}
                        reports.맞틀수익[key][수익] = 0
                        reports.맞틀수익[key][승] = 0
                        reports.맞틀수익[key][패] = 0

                    reports.맞틀수익[key][수익] += report.맞틀리스트[key][수익]
                    reports.맞틀수익[key][승] += report.맞틀리스트[key][승]
                    reports.맞틀수익[key][패] += report.맞틀리스트[key][패]

            # reports_list(각 프로세스 결과들)의 맞틀수익을 비교하여 같은 key(ex: '맞틀틀') 중 최적의 수익을 갖는 익절, 손절을 뽑음
            for key in reports.맞틀수익:
                if key not in 모든맞틀수익:
                    모든맞틀수익[key] = []

                params = {
                    수익: round(reports.맞틀수익[key][수익]),
                    승: reports.맞틀수익[key][승],
                    패: reports.맞틀수익[key][패],
                    익절틱: reports.전략변수[STRATEGY][익손절별수익계산][익절틱],
                    손절틱: reports.전략변수[STRATEGY][익손절별수익계산][손절틱],
                    승률 : round(reports.맞틀수익[key][승] / (reports.맞틀수익[key][승] + reports.맞틀수익[key][패]) * 100)
                }
                is_pushed = False
                for i in range(len(모든맞틀수익[key])):
                    if reports.맞틀수익[key][수익] > 모든맞틀수익[key][i][수익]:
                        모든맞틀수익[key].insert(i, params)
                        is_pushed = True

                if not is_pushed:
                    모든맞틀수익[key].append(params)

        from pprint import pprint
        pprint(모든맞틀수익)
