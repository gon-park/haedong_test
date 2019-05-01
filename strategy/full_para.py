# -*- coding: utf-8 -*-
from variable.constant import *
from strategy import __base_strategy
from indicator import ma
import math
import os
from variable import subject
from variable.report import Report


class FullPara(__base_strategy.BaseStrategy):

    def __init__(self, charts: dict, subject_code: str, main_chart: str, strategy_var: dict, contracts: dict):
        super(FullPara, self).__init__()
        self.strategy_name = "full_para"
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
        self.수익리스트 = []

    def check_contract_in_candle(self, subject_code: str):
        # 메인차트 Index가 부족 할 때 거래 안함
        if self.charts[self.main_chart_id].index < 3500:
            return None

        메인차트 = self.charts[self.main_chart_id]
        main_chart = self.charts[self.main_chart_id]
        para = main_chart.indicators[PARA][0]
        order_info = None

        # 계약이 있을 때
        if subject_code in self.contracts and FullPara.get_contract_count(subject_code, self.contracts, 풀파라) > 0:
            보유계약 = FullPara.get_contracts(subject_code, self.contracts, 풀파라)
            # 계약이 있을 때
            if para.FLOW == 상향:
                if para.SAR > main_chart.candles.저가[main_chart.index + 1] or \
                        (len(self.profit_tick) > 0 and max(para.EP, main_chart.candles.고가[main_chart.index + 1]) - 보유계약[0].체결표시가격 >= self.profit_tick[0][0] * subject.info[subject_code[:2]][단위] and \
                                         max(para.EP, main_chart.candles.고가[main_chart.index + 1]) - main_chart.candles.저가[main_chart.index + 1] >= self.profit_dribble_tick[0] * subject.info[subject_code[:2]][단위]) or \
                        (len(self.sonjul_tick) > 0 and round((para.EP - main_chart.candles.저가[main_chart.index + 1]) / subject.info[subject_code[:2]][단위]) >= self.sonjul_tick[0][0]):

                    for 가격 in main_chart.candles.가격들[main_chart.index + 1]:
                        if para.EP < 가격: para.EP = 가격

                        최고가대비손절틱 = para.EP - 가격
                        최고가대비손절틱 = round(최고가대비손절틱 / subject.info[subject_code[:2]][단위]) * subject.info[subject_code[:2]][단위]

                        if 가격 < para.SAR:
                            # 반전시
                            self.log.debug('하향 반전으로 is_it_sell() 콜, SAR : %s, current_price : %s' % (para.SAR, 가격))
                            order_info = self.is_it_sell(subject_code, 가격)

                        elif len(self.profit_tick) > 0 and para.EP - 보유계약[0].체결표시가격 >= self.profit_tick[0][0] * subject.info[subject_code[:2]][단위] and \
                                                para.EP - 가격 >= self.profit_dribble_tick[0] * subject.info[subject_code[:2]][단위]:
                            # 익절 수익 이후 익절드리블틱 이하로 가격이 떨어졌을 때
                            self.log.debug("익절수익 이후 익절드리블 틱(%s) 이하로 가격이 떨어져 is_it_sell() 콜, %s, 직전SAR: %s, 최고가 : %s, 현재가 : %s" % (self.profit_dribble_tick[0], 메인차트.candles.체결시간[메인차트.index+1], para.SARS[-1], para.EP, 가격))
                            order_info = self.is_it_sell(subject_code, 가격)

                        elif len(self.sonjul_tick) > 0 and 최고가대비손절틱 >= self.sonjul_tick[0][0] * subject.info[subject_code[:2]][단위]:
                            # 손절틱
                            self.log.debug("손절틱(%s) 이상 떨어져 is_it_sell() 콜, 시간:%s" % (self.sonjul_tick[0][0],메인차트.candles.체결시간[메인차트.index+1]))
                            order_info = self.is_it_sell(subject_code, 가격)

                        if order_info is not None: break

            elif para.FLOW == 하향:
                if para.SAR < main_chart.candles.고가[main_chart.index + 1] or \
                        (len(self.profit_tick) > 0 and 보유계약[0].체결표시가격 - min(para.EP, main_chart.candles.저가[main_chart.index + 1]) >= self.profit_tick[0][0] * subject.info[subject_code[:2]][단위] and \
                                         main_chart.candles.고가[main_chart.index + 1] - min(para.EP, main_chart.candles.저가[main_chart.index + 1]) >= self.profit_dribble_tick[0] * subject.info[subject_code[:2]][단위]) or \
                        (len(self.sonjul_tick) > 0 and round((main_chart.candles.고가[main_chart.index + 1] - para.EP) / subject.info[subject_code[:2]][단위]) >= self.sonjul_tick[0][0]):

                    for 가격 in main_chart.candles.가격들[main_chart.index + 1]:
                        if para.EP > 가격: para.EP = 가격

                        최고가대비손절틱 = 가격 - para.EP
                        최고가대비손절틱 = round(최고가대비손절틱 / subject.info[subject_code[:2]][단위]) * subject.info[subject_code[:2]][단위]

                        if 가격 > para.SAR:
                            # 반전시
                            self.log.debug('상향 반전으로 is_it_sell() 콜, SAR : %s, current_price : %s' % (para.SAR, 가격))
                            order_info = self.is_it_sell(subject_code, 가격)

                        elif len(self.profit_tick) > 0 and 보유계약[0].체결표시가격 - para.EP >= self.profit_tick[0][0] * subject.info[subject_code[:2]][단위] and \
                                                가격 - para.EP >= self.profit_dribble_tick[0] * subject.info[subject_code[:2]][단위]:
                            # 익절 수익 이후 익절드리블틱 이하로 가격이 떨어졌을 때
                            self.log.debug("익절수익 이후 익절드리블 틱(%s) 이하로 가격이 떨어져 is_it_sell() 콜. %s, 직전SAR: %s, 최저가 : %s, 현재가 : %s" % (self.profit_dribble_tick[0],메인차트.candles.체결시간[메인차트.index+1], para.SARS[-1], para.EP, 가격))
                            order_info = self.is_it_sell(subject_code, 가격)
                        elif len(self.sonjul_tick) > 0 and 최고가대비손절틱 >= self.sonjul_tick[0][0] * subject.info[subject_code[:2]][단위]:
                            # 손절틱
                            self.log.debug("손절틱(%s) 이상 떨어져 is_it_sell() 콜, 시간:%s" % (self.sonjul_tick[0][0],메인차트.candles.체결시간[메인차트.index+1]))
                            order_info = self.is_it_sell(subject_code, 가격)

                        if order_info is not None: break

        # 계약이 없을 때
        else:
            if para.FLOW is 상향:
                if main_chart.candles.저가[main_chart.index + 1] < para.SAR:
                    for 가격 in main_chart.candles.가격들[main_chart.index + 1]:
                        if 가격 < para.SAR:
                            # 하향 반전
                            #current_price = math.floor(para.SAR * (1 / subject.info[subject_code[:2]][단위])) / ( 1 / subject.info[subject_code[:2]][단위])
                            current_price = 가격
                            self.log.debug('하향 반전, SAR : %s, current_price : %s' % (para.SAR, current_price))
                            #current_price = current_price - subject.info[subject_code[:2]][단위]
                            order_info = self.is_it_ok(subject_code, current_price)
                            break

            elif para.FLOW is 하향:
                if para.SAR < main_chart.candles.고가[main_chart.index + 1]:
                    for 가격 in main_chart.candles.가격들[main_chart.index + 1]:
                        if para.SAR < 가격:
                            # 상향 반전
                            #current_price = math.ceil(para.SAR * (1 / subject.info[subject_code[:2]][단위])) / (1 / subject.info[subject_code[:2]][단위])
                            current_price = 가격
                            self.log.debug('상향 반전, SAR : %s, current_price : %s' % (para.SAR, current_price))
                            #current_price = current_price + subject.info[subject_code[:2]][단위]
                            order_info = self.is_it_ok(subject_code, current_price)
                            break

        if main_chart.candles.영업일[main_chart.index + 1] != main_chart.candles.영업일[main_chart.index]:
            return None

        return order_info

    def check_contract_in_tick(self, subject_code, current_price):
        pass

    def is_it_ok(self, subject_code: str, current_price: float):
        log = self.log

        self.param01 = self.strategy_var["param01"]
        self.param02 = self.strategy_var["param02"]
        self.param03 = self.strategy_var["param03"]
        self.param04 = self.strategy_var["param04"]
        self.param05 = self.strategy_var["param05"]
        self.param06 = self.strategy_var["param06"]
        self.param07 = self.strategy_var["param07"]
        self.param08 = self.strategy_var["param08"]
        self.param09 = self.strategy_var["param09"]
        self.param10 = self.strategy_var["param10"]
        self.param11 = self.strategy_var["param11"]
        self.param12 = self.strategy_var["param12"]
        self.param13 = self.strategy_var["param13"]
        self.param14 = self.strategy_var["param14"]
        self.param15 = self.strategy_var["param15"]
        self.param16 = self.strategy_var["param16"]
        self.param17 = self.strategy_var["param17"]
        self.param18 = self.strategy_var["param18"]
        self.param19 = self.strategy_var["param19"]
        self.param20 = self.strategy_var["param20"]
        self.param21 = self.strategy_var["param21"]
        self.param22 = self.strategy_var["param22"]
        self.param23 = self.strategy_var["param23"]
        self.param24 = self.strategy_var["param24"]
        self.param25 = self.strategy_var["param25"]



        # 변수 선언
        메인차트 = self.charts[self.main_chart_id]
        _매도수구분 = None
        _이동평균선 = True
        _매매시간확인 = True
        직전플로우수익 = 0
        파라 = 메인차트.indicators[PARA][0]
        현재플로우 = 파라.FLOW
        flow_candle_list = []
        flow_candle_list = 파라.flow_candle_count_list[-5:]
        flow_candle_list.append(파라.flow_candle_count)
        flow_ep_candle_list = 파라.flow_ep_candle_count_list[-5:]

        flow_ep_candle_list.append({'flow_ep': 파라.flow_ep, 'flow_ep_candle_count': 파라.flow_ep_candle_count + 1})
        #print(flow_candle_list)

        # 반전 확인
        if 현재플로우 == 상향 and current_price < 파라.SAR:
            # 하향 반전
            직전플로우수익 = (current_price-파라.SARS[-1]) / subject.info[subject_code[:2]][단위]
            log.debug("하향 반전, 현재가 : %s, 직전플로우수익 : %s(pid = %s) 시간:%s" % (current_price, 직전플로우수익, self.pid, 메인차트.candles.체결시간[메인차트.index+1]))
            log.debug("flow_ep_candle_list : %s" % flow_ep_candle_list[-1])

            #_매도수구분 = 신규매도
            if ma.Calc.is_sorted(메인차트.indicators[MA]) == 하락세:
                _매도수구분 = 신규매도
            else:
                #log.debug("이동평균선이 맞지 않아 매도 포기.(pid = %s)" % self.pid)
                _매도수구분 = 신규매도
                _이동평균선 = False
        elif 현재플로우 == 하향 and current_price > 파라.SAR:
            # 상향 반전
            직전플로우수익 = (파라.SARS[-1] - current_price) / subject.info[subject_code[:2]][단위]
            log.debug("상향 반전, 현재가 : %s, 직전플로우수익 : %s(pid = %s) 시간:%s" % (current_price, 직전플로우수익, self.pid, 메인차트.candles.체결시간[메인차트.index+1]))
            log.debug("flow_ep_candle_list : %s" % flow_ep_candle_list[-1])

            #_매도수구분 = 신규매수
            if ma.Calc.is_sorted(메인차트.indicators[MA]) == 상승세:
                _매도수구분 = 신규매수
            else:
                #log.debug("이동평균선이 맞지 않아 매도 포기.(pid = %s)" % self.pid)
                _매도수구분 = 신규매수
                _이동평균선 = False


        if len(파라.SARS) < 5:
            return None

        self.수익리스트.append(직전플로우수익)
        수익리스트 = self.수익리스트
        if len(수익리스트) > 16:
            수익리스트 = 수익리스트[-15:]
        if len(수익리스트) < 4:
            return None

        맞틀리스트 = []
        for i in range(len(수익리스트)):
            if 수익리스트[i] < 0:
                맞틀리스트.append(틀)
            else:
                맞틀리스트.append(맞)

        log.debug("맞틀리스트 : %s" % 맞틀리스트)
        log.debug("수익리스트 : %s" % 수익리스트)


        # # 매매시간 확인

        매매시간 = int(메인차트.candles.체결시간[메인차트.index + 1].strftime("%H%M"))
        if subject_code[:3] == 'GCZ' or subject_code[:3] == 'GCQ':  # 겨울
            if 2100 < 매매시간 < 2230:
                _매매시간확인 = False

        else:
            if 2200 < 매매시간 < 2330:
                _매매시간확인 = False

        if subject_code[:3] == "GCM" or subject_code[:3] == "GCQ" or subject_code[:3] == "GCZ":
            if 558 <= 매매시간 <= 700:

                if 매매시간 == 700:
                    if _매도수구분 == 신규매도:
                        if 메인차트.candles.저가[메인차트.index] - 메인차트.candles.고가[메인차트.index+1] > 10 * subject.info[subject_code[:2]][단위]:
                            return None
                        else:
                            log.debug("장 시작 시간 매매, 체결시간:%s" % 메인차트.candles.체결시간[메인차트.index + 1])
                            pass

                    elif _매도수구분 == 신규매수:
                        if 메인차트.candles.저가[메인차트.index+1] - 메인차트.candles.고가[메인차트.index] > 10 * subject.info[subject_code[:2]][단위]:
                            return None
                        else:
                            log.debug("장 시작 시간 매매, 체결시간:%s" % 메인차트.candles.체결시간[메인차트.index + 1])
                            pass

        elif subject_code[:3] == "GCJ" or subject_code[:3] == "GCG":
            if 658 <= 매매시간 <= 800:
                if 매매시간 == 800:
                    if _매도수구분 == 신규매도:
                        if 메인차트.candles.저가[메인차트.index] - 메인차트.candles.고가[메인차트.index + 1] > 10 * \
                                subject.info[subject_code[:2]][단위]:
                            return None
                        else:
                            log.debug("장 시작 시간 매매, 체결시간:%s" % 메인차트.candles.체결시간[메인차트.index + 1])
                            pass

                    elif _매도수구분 == 신규매수:
                        if 메인차트.candles.저가[메인차트.index + 1] - 메인차트.candles.고가[메인차트.index] > 10 * \
                                subject.info[subject_code[:2]][단위]:
                            return None
                        else:
                            log.debug("장 시작 시간 매매, 체결시간:%s" % 메인차트.candles.체결시간[메인차트.index + 1])
                            pass

        if _매도수구분 is None:
            return None


        self.profit_tick = [[71, 1]]
        self.sonjul_tick = self.strategy_var[손절틱][:]
        self.profit_dribble_tick = self.strategy_var[수익드리블틱][:]
        self.sonjul_dribble_tick = self.strategy_var[손절드리블틱][:]

        if flow_candle_list[-1] < self.param11:
            log.debug("지난 캔들이 %s개 미만으로 진입 포기" % self.param11)
            return None

        elif flow_candle_list[-1] <= self.param09:
            if flow_candle_list[-3] <= self.param19:# and flow_candle_list[-4] <= 190:
                return None
            elif flow_candle_list[-2] > self.param24:
                return None
            log.debug("지난 캔들 %s개 이하로 진입" % self.param09)
            _이동평균선 = True
            if flow_candle_list[-1] <= self.param14 and flow_candle_list[-2] >= self.param15: # 90, 200
                _매매시간확인 = True
            self.profit_tick = [[73, 1]]
            # self.profit_tick = [[self.param20, 1]]

        elif 맞틀리스트[-1] == 틀 and 수익리스트[-1] < self.param08 and flow_candle_list[-2] > self.param21 :
            log.debug("큰 틀 다음으로 매매 진입합니다.")
            _매매시간확인 = True
            self.profit_tick = [[51, 1]]

        #add
        elif 맞틀리스트[-1] == 맞 and flow_candle_list[-1] > self.param16 and flow_candle_list[-1] - flow_ep_candle_list[-1]['flow_ep_candle_count'] < self.param17 and \
                        abs((flow_ep_candle_list[-1]['flow_ep'] - current_price) / subject.info[subject_code[:2]][단위]) > self.param18:
            log.debug("지난 플로우 맞일 때 큰 추세 전환으로 진입")
            self.profit_tick = [[71, 1]]
            #_매매시간확인 = True


        elif 수익리스트[-1] > self.param06:
            log.debug("지난 플로우 수익이 %s틱 이상으로 진입 포기" % self.param06)
            return None

        elif 맞틀리스트[-3:] == [틀, 맞, 틀]:
            if flow_candle_list[-1] <= self.param01:
                log.debug("틀맞틀 로 매매 진입합니다.")
                #self.profit_tick = [[200, 1]]
                self.profit_tick = [[self.param20, 1]]
            else:
                log.info("틀맞틀일때 지난 플로우 캔들 수가 %s(현재 %s) 이상으로 매매 안합니다" % (self.param01, flow_candle_list[-1]))
                return None

        elif 맞틀리스트[-4:] == [맞, 맞, 맞, 틀]:
            if  flow_candle_list[-3] < flow_candle_list[-4] and flow_candle_list[-3] < flow_candle_list[-2] and flow_candle_list[-4] < flow_candle_list[-2] \
                    and flow_candle_list[-1] < self.param23:
                log.debug("맞맞맞틀 로 진입")
            else:
                log.debug("맞맞맞틀 로 매매 포기")
                return None

        elif 맞틀리스트[-2:] == [맞, 틀]:
            log.debug("맞틀 로 매매 포기")
            return None


        elif 맞틀리스트[-5:] == [틀, 틀, 틀, 틀, 틀]:
            log.debug("틀틀틀틀틀 다음으로 %s 진입 안함.(pid = %s)" % ('신규매도' if _매도수구분 == 1 else '신규매수', self.pid))
            return None

        elif 맞틀리스트[-5:] == [맞, 틀, 틀, 틀, 틀]:
            if 수익리스트[-2] < self.param05: #-10
                log.debug("맞틀틀틀틀, 지지난플로우수익 %s틱 미만으로 %s 포기.(pid = %s)" % (self.param05, '신규매도' if _매도수구분 == 1 else '신규매수', self.pid))
                return None
            elif flow_candle_list[-5] > self.param24:
                return None
            else:
                log.debug("맞틀틀틀틀 다음으로 %s 진입.(pid = %s)" % ('신규매도' if _매도수구분 == 1 else '신규매수', self.pid))
                self.profit_tick = [[61, 1]]


        elif 맞틀리스트[-4:] == [틀, 맞, 맞, 맞]:
            if 수익리스트[-1] > self.param12: #10
                log.debug("틀맞맞맞, 직전플로우 수익이 10틱 초과로 %s 포기.(pid = %s)" % ('신규매도' if _매도수구분 == 1 else '신규매수', self.pid))
                return None
            else:
                log.debug("틀맞맞맞 다음으로 %s 진입.(pid = %s)" % ('신규매도' if _매도수구분 == 1 else '신규매수', self.pid))
                self.profit_tick = [[71, 1]]



        elif 맞틀리스트[-4:] == [맞, 틀, 맞, 맞]:
            if 수익리스트[-2] > self.param13:
                log.debug("맞틀맞맞, 직전플로우 수익이 10틱 초과로 %s 포기.(pid = %s)" % ('신규매도' if _매도수구분 == 1 else '신규매수', self.pid))
                return None
            else:
                log.debug("맞틀맞맞 다음으로 %s 진입.(pid = %s)" % ('신규매도' if _매도수구분 == 1 else '신규매수', self.pid))
                self.profit_tick = [[71, 1]]



        elif 맞틀리스트[-4:] == [맞, 틀, 틀, 맞]:
            if 수익리스트[-1] > self.param03: #10
                log.debug("맞틀틀맞, 직전플로우 수익이 10틱 초과로 %s 포기.(pid = %s)" % ('신규매도' if _매도수구분 == 1 else '신규매수', self.pid))
                return None
            else:
                log.debug("맞틀틀맞 다음으로 %s 진입.(pid = %s)" % ('신규매도' if _매도수구분 == 1 else '신규매수', self.pid))
                self.profit_tick = [[73, 1]]
                #self.profit_tick = [[self.param20, 1]]


        elif 맞틀리스트[-4:] == [틀, 틀, 틀, 맞]:
            if 수익리스트[-1] < self.param07:
                log.debug("틀틀틀맞 다음 조건이 맞지 않아 %s 포기.(pid = %s)" % ('신규매도' if _매도수구분 == 1 else '신규매수', self.pid))
                return None
            else:
                log.debug("틀틀틀맞 다음으로 %s 진입.(pid = %s)" % ('신규매도' if _매도수구분 == 1 else '신규매수', self.pid))
                self.profit_tick = [[71, 1]]

        ############################
        elif 맞틀리스트[-4:] == [틀, 틀, 맞, 맞]:
            #if flow_candle_list[-2] > self.param02 and flow_candle_list[-1] < self.param04:
            if flow_candle_list[-2] > self.param02 and flow_candle_list[-1] < self.param04 and flow_candle_list[-1] > flow_candle_list[-2]:
                return None
            elif flow_candle_list[-1] + flow_candle_list[-2] < self.param22:
                return None
            else:
                log.debug("틀틀맞맞 다음으로 %s 진입.(pid = %s)" % ('신규매도' if _매도수구분 == 1 else '신규매수', self.pid))
                self.profit_tick = [[71, 1]]


        elif 맞틀리스트[-4:] == [맞, 맞, 틀, 틀]:
            #if flow_candle_list[-2] > self.param10 or (flow_candle_list[-2] < 100 and flow_candle_list[-1] > 250):
            if flow_candle_list[-2] > self.param10:
                log.debug("맞맞틀틀, 조건이 맞지 않아 %s 포기.(pid = %s)" % ('신규매도' if _매도수구분 == 1 else '신규매수', self.pid))
                return None
            elif flow_candle_list[-3] + flow_candle_list[-1] > self.param25:
                return None
            else:
                log.debug("맞맞틀틀 다음으로 %s 진입.(pid = %s)" % ('신규매도' if _매도수구분 == 1 else '신규매수', self.pid))
                self.profit_tick = [[71, 1]]


        elif 맞틀리스트[-4:] == [맞, 틀, 틀, 틀]:
            if 수익리스트[-2] < self.param05: #-10
                log.debug("맞틀틀틀, 지지난플로우수익 -10틱 미만으로 %s 포기.(pid = %s)" % ('신규매도' if _매도수구분 == 1 else '신규매수', self.pid))
                return None
            else:
                log.debug("맞틀틀틀 다음으로 %s 진입.(pid = %s)" % ('신규매도' if _매도수구분 == 1 else '신규매수', self.pid))
                self.profit_tick = [[151, 1]]

        elif 맞틀리스트[-4:] == [틀, 맞, 틀, 틀]:
            if flow_candle_list[-2] < flow_candle_list[-1]:
                log.debug("틀맞틀틀 일때 조건이 맞지 않아 매매포기")
                return None
            else:
                self.profit_tick = [[71, 1]]
                log.debug("틀맞틀틀 로 진입 %s .(pid = %s)" % ('신규매도' if _매도수구분 == 1 else '신규매수', self.pid))
                pass

        elif 맞틀리스트[-3:] == [맞, 맞, 맞]:
            if flow_candle_list[-4] > flow_candle_list[-3] > flow_candle_list[-2] > flow_candle_list[-1]:
                log.debug("맞맞맞맞 으로 진입 %s .(pid = %s)" % ('신규매도' if _매도수구분 == 1 else '신규매수', self.pid))
                self.profit_tick = [[71, 1]]
            else:
                log.debug("맞맞맞맞 일때 조건이 맞지 않아 매매포기")
                return None


        # elif 맞틀리스트[-4:] == [틀, 틀, 틀, 맞]:
        #     if flow_candle_list[-1] < 450:
        #         return None
        #     else:
        #         pass
        #
        # elif 맞틀리스트[-1] == 틀 and abs(파라.EP - 파라.SARS[-1]) < 0.8 and flow_candle_list[-1] < 200 and flow_candle_list[-2] > 300:
        #         self.profit_tick = [[71, 1]]

        else:
            log.debug("맞틀 조건에 맞지 않아 %s 포기.(pid = %s)" % ('신규매도' if _매도수구분 == 1 else '신규매수', self.pid))
            return None

        if _매매시간확인 == False:
            log.debug("22:00 ~ 23:30 사이라 매매 포기.")
            return None

        if _이동평균선 == False:
            log.debug("이동평균선이 맞지 않아 매도 포기.(pid = %s)" % self.pid)
            return None

        # 매매진입
        self.order_contents = {
            신규주문: True,
            종목코드: subject_code,
            매도수구분: _매도수구분,
            매매전략: 풀파라,
            수량: 1,
            가격: current_price
        }
        log.info("FullPara.is_it_ok(): %s, %s 진입.(pid = %s)" % (메인차트.candles.체결시간[메인차트.index+1], self.order_contents, self.pid))
        # 익절, 손절틱 복사


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
            log.info("최고가대비손절틱:"+str(최고가대비손절틱))
            log.info("EP:"+str(파라.EP))
            log.info("현재가:"+str(current_price))
            if len(self.sonjul_tick) > 0 and 최고가대비손절틱 >= self.sonjul_tick[0][0] * subject.info[subject_code[:2]][단위]:
                log.info("손절가가 되어 매수계약(%s계약) 청산 요청, 체결시간 : %s, 현재가 : %s(pid = %s)" % (int(len(보유계약) * self.sonjul_tick[0][1]),메인차트.candles.체결시간[메인차트.index+1], current_price, self.pid))
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

            if len(self.profit_tick) > 0 and 파라.EP - 보유계약[0].체결표시가격 >= self.profit_tick[0][0] * subject.info[subject_code[:2]][단위] and \
                                    파라.EP - 메인차트.candles.저가[메인차트.index + 1] >= self.profit_dribble_tick[0] * subject.info[subject_code[:2]][단위]:
                log.info("익절드리블 후(%s틱) 손절가가 되어 매수계약(%s계약) 청산 요청, 체결시간 : %s, 현재가 : %s(pid = %s)" % ((current_price - math.ceil(파라.SARS[-1] / subject.info[subject_code[:2]][단위]) * subject.info[subject_code[:2]][단위]) / subject.info[subject_code[:2]][단위], int(len(보유계약) * self.profit_tick[0][1]), 메인차트.candles.체결시간[메인차트.index+1], current_price, self.pid))

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
                log.info("하향 반전으로 모든 매수계약 청산 요청, 체결시간 : %s, 현재가 : %s(pid = %s)" % (메인차트.candles.체결시간[메인차트.index+1], current_price, self.pid))
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

            log.info("최고가대비손절틱:"+str(최고가대비손절틱))
            log.info("EP:"+str(파라.EP))
            log.info("현재가:"+str(current_price))

            if len(self.sonjul_tick) > 0 and 최고가대비손절틱 >= self.sonjul_tick[0][0] * subject.info[subject_code[:2]][단위]:
                log.info("손절가가 되어 매도계약(%s계약) 청산 요청, 체결시간 : %s, 현재가 : %s(pid = %s)" % (int(len(보유계약) * self.sonjul_tick[0][1]),메인차트.candles.체결시간[메인차트.index+1], current_price, self.pid))
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

            if len(self.profit_tick) > 0 and 보유계약[0].체결표시가격 - 파라.EP >= self.profit_tick[0][0] * subject.info[subject_code[:2]][단위] and \
                                    메인차트.candles.고가[메인차트.index + 1] - 파라.EP >= self.profit_dribble_tick[0] * \
                            subject.info[subject_code[:2]][단위]:
                log.info("익절드리블 후(%s틱) 손절가가 되어 매도계약(%s계약) 청산 요청, 체결시간 : %s, 현재가 : %s(pid = %s)" % ((math.floor(파라.SARS[-1] / subject.info[subject_code[:2]][단위]) * subject.info[subject_code[:2]][단위] - current_price) / subject.info[subject_code[:2]][단위], 메인차트.candles.체결시간[메인차트.index+1], int(len(보유계약) * self.profit_tick[0][1]),current_price, self.pid))
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
                log.info("상향 반전으로 모든 매도계약 청산 요청, 체결시간 : %s, 현재가 : %s(pid = %s)" % (메인차트.candles.체결시간[메인차트.index+1], current_price, self.pid))
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
        pass