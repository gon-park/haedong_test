# -*- coding: utf-8 -*-

from variable.constant import *
from strategy import __base_strategy
import math
from variable import subject


class FullPara(__base_strategy.BaseStrategy):
    trader = None
    chart = None
    main_chart_id = None

    def __init__(self, trader_obj):
        super(FullPara, self).__init__()
        self.trader = trader_obj
        self.charts = self.trader.charts
        type, time_unit = self.trader.main_chart.split('_')
        subject_code = self.trader.subject_code
        self.main_chart_id = subject_code + '_' + type + '_' + time_unit

    def check_contract_in_candle(self, subject_code):
        # 메인차트 Index가 부족 할 때 거래 안함
        if self.charts[self.main_chart_id].index < 3000:
            return None

        main_chart = self.charts[self.main_chart_id]
        para = main_chart.indicators[PARA][0]
        order_info = None
        if subject_code in self.trader.contracts and len(self.trader.contracts[self.trader.subject_code]) > 0:
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
                    print('하향 반전, SAR : %s, current_price : %s' % (para.SAR, current_price))
            elif para.FLOW is 하향:
                if para.SAR < main_chart.candles.고가[main_chart.index + 1]:
                    # 상향 반전
                    current_price = math.ceil(para.SAR * (1 / subject.info[subject_code[:2]][단위])) / (1 / subject.info[subject_code[:2]][단위])
                    order_info = self.is_it_ok(subject_code, current_price)
                    print('상향 반전, SAR : %s, current_price : %s' % (para.SAR, current_price))

        return order_info

    def check_contract_in_tick(self, subject_code, current_price):
        pass

    def is_it_ok(self, subject_code, current_price):
        log = self.log

        main_chart = self.charts[self.main_chart_id]
        #
        # start_price = subject.info[subject_code]['시가']
        # profit = 0
        # profit_tick = subject.info[subject_code]['익절틱']
        # sonjal_tick = subject.info[subject_code]['손절틱']
        # mesu_medo_type = None
        # false = {'신규주문': False}
        # ma_line_is_true = True
        # reverse_tic = subject.info[subject_code]['반대매매틱']
        #
        # # 300캔들이 없으면 매매 안함
        # if calc.data[subject_code]['idx'] < 300:
        #     return false
        #
        # if subject.info[subject_code]['상태'] == '매수중' or subject.info[subject_code]['상태'] == '매도중' or \
        #                 subject.info[subject_code]['상태'] == '청산시도중' or subject.info[subject_code]['상태'] == '매매시도중':
        #     log.debug('신규 주문 가능상태가 아니므로 매매 불가. 상태 : ' + subject.info[subject_code]['상태'])
        #     return false
        #
        # # log.debug("종목코드(" + subject_code + ")  현재 Flow : " + subject.info[subject_code]['flow'] + " / SAR : " + str(subject.info[subject_code]['sar']) + " / 추세 : " + my_util.is_sorted(subject_code))
        # # 여기서 상향/하향계산은 2개로 나뉨 1. 캐들만들고 있을때~! 2. 캔들 완성시!!
        # # calc를 통해서 calc.push -> calc를 통해 여러가지 계산을 하는데 이때 flow를 저장 즉, 실데이터가 딱 들어오면 바로 계산끝
        # if subject.info[subject_code]['flow'] == '상향':
        #     if current_price < subject.info[subject_code]['sar']:
        #         # 여기에 들어온건 상향일때 현재가격이 sar보다 작아져 하향반전을 이룰때
        #         log.debug("종목코드(" + subject_code + ") 하향 반전.")
        #         profit = current_price - calc.data[subject_code]['이전반전시SAR값'][-1]
        #         if len(calc.data[subject_code]['SAR반전시간']) > 0 and calc.data[subject_code]['SAR반전시간'][-1] == \
        #                 calc.data[subject_code]['체결시간'][-1]:  # 반전 후 SAR로 갱신되었다면
        #             profit = current_price - calc.data[subject_code]['이전반전시SAR값'][-2]
        #
        #         if my_util.is_sorted(subject_code) == '하락세':
        #             mesu_medo_type = '신규매도'
        #         else:
        #             res.info("이동평균선이 맞지 않아 매수 포기합니다.")
        #             ma_line_is_true = False
        #             mesu_medo_type = '신규매도'
        #             # return false
        #
        #     elif calc.data[subject_code]['플로우'][-2] == '하향':
        #         # 하향으로 진행하던 플로가 상향으로 상향 반전될때! ex)리스트[-1]은 리스트의 가장 마지막 항목이다
        #         log.debug("종목코드(" + subject_code + ") 상향 반전.")
        #         profit = calc.data[subject_code]['이전반전시SAR값'][-1] - current_price
        #         if len(calc.data[subject_code]['SAR반전시간']) > 0 and calc.data[subject_code]['SAR반전시간'][-1] == \
        #                 calc.data[subject_code]['체결시간'][-1]:  # 반전 후 SAR로 갱신되었다면
        #             profit = calc.data[subject_code]['이전반전시SAR값'][-2] - current_price
        #
        #         if my_util.is_sorted(subject_code) == '상승세':
        #             mesu_medo_type = '신규매수'
        #
        #         else:
        #             res.info("이동평균선이 맞지 않아 매수 포기합니다.")
        #             ma_line_is_true = False
        #             mesu_medo_type = '신규매수'
        #             # return false
        #     else:
        #         return false
        #
        # elif subject.info[subject_code]['flow'] == '하향':
        #     if current_price > subject.info[subject_code]['sar']:
        #         log.debug("종목코드(" + subject_code + ") 상향 반전.")
        #         profit = calc.data[subject_code]['이전반전시SAR값'][-1] - current_price
        #         if len(calc.data[subject_code]['SAR반전시간']) > 0 and calc.data[subject_code]['SAR반전시간'][-1] == \
        #                 calc.data[subject_code]['체결시간'][-1]:  # 반전 후 SAR로 갱신되었다면
        #             profit = calc.data[subject_code]['이전반전시SAR값'][-2] - current_price
        #
        #         if my_util.is_sorted(subject_code) == '상승세':
        #             mesu_medo_type = '신규매수'
        #
        #         else:
        #             res.info("이동평균선이 맞지 않아 매수 포기합니다.")
        #             ma_line_is_true = False
        #             mesu_medo_type = '신규매수'
        #             # return false
        #
        #     elif calc.data[subject_code]['플로우'][-2] == '상향':
        #         log.debug("종목코드(" + subject_code + ") 하향 반전.")
        #         profit = current_price - calc.data[subject_code]['이전반전시SAR값'][-1]
        #         if len(calc.data[subject_code]['SAR반전시간']) > 0 and calc.data[subject_code]['SAR반전시간'][-1] == \
        #                 calc.data[subject_code]['체결시간'][-1]:  # 반전 후 SAR로 갱신되었다면
        #             profit = current_price - calc.data[subject_code]['이전반전시SAR값'][-2]
        #
        #         if my_util.is_sorted(subject_code) == '하락세':
        #             mesu_medo_type = '신규매도'
        #
        #         else:
        #             res.info("이동평균선이 맞지 않아 매수 포기합니다.")
        #             ma_line_is_true = False
        #             mesu_medo_type = '신규매도'
        #             # return false
        #     else:
        #         return false
        # else:
        #     return false
        #
        # profit = profit / subject.info[subject_code]['단위']
        #
        # if len(subject.info[subject_code]['맞틀리스트']) < 5:
        #     return false
        #
        # if subject.info[subject_code]['반대매매'] == True:
        #     subject.info[subject_code]['반대매매'] = False
        #     log.info("반대대대 False로 변경.")
        #
        # if len(calc.data[subject_code]['SAR반전시간']) > 0 and calc.data[subject_code]['SAR반전시간'][-1] == \
        #         calc.data[subject_code]['체결시간'][-1]:  # 반전 후 SAR로 갱신되었다면
        #
        #     if subject.info[subject_code]['맞틀리스트'][-2] == '맞' and subject.info[subject_code]['맞틀리스트'][-1] == '틀':
        #         if subject.info[subject_code]['수익리스트'][-2] > 70:
        #             log.info("지지난 플로우가 70이상 수익으로 진입안합니다.")
        #             return false
        #         else:
        #             pass
        #
        #     if subject.info[subject_code]['수익리스트'][-1] > 160:
        #         if mesu_medo_type == '신규매도':
        #             mesu_medo_type = '신규매수'
        #         elif mesu_medo_type == '신규매수':
        #             mesu_medo_type = '신규매도'
        #         log.info("[%s] 반대매매 조건이 맞아 반대 매매 진입합니다.(전 플로우 160틱 이상 수익)(1)" % mesu_medo_type)
        #         ma_line_is_true = True
        #         subject.info[subject_code]['반대매매'] = True
        #
        #     elif subject.info[subject_code]['맞틀리스트'][-4:] == ['틀', '틀', '틀', '틀']:
        #         if subject.info[subject_code]['수익리스트'][-2] < subject.info[subject_code]['수익리스트'][-1] and \
        #                         subject.info[subject_code]['수익리스트'][-2] < -15:
        #             log.info("틀틀틀틀일때 조건이 맞지 않아 진입 안합니다.")
        #             return false
        #         else:
        #             log.info("틀틀틀틀 다음으로 매매 진입합니다.")
        #             pass
        #
        #     elif subject.info[subject_code]['맞틀리스트'][-4:] == ['틀', '맞', '맞', '틀']:
        #         log.info("틀맞맞틀 다음으로 매매 진입합니다.")
        #         pass
        #
        #     elif subject.info[subject_code]['맞틀리스트'][-4:] == ['틀', '맞', '틀', '틀']:
        #         log.info("틀맞틀틀 다음으로 매매 진입합니다.")
        #         pass
        #
        #     elif subject.info[subject_code]['맞틀리스트'][-4:] == ['맞', '틀', '틀', '맞']:
        #         if subject.info[subject_code]['수익리스트'][-1] > 10:
        #             log.info("이전 플로우 수익이 10틱 이상으로 매매 진입 안합니다.")
        #             return false
        #         else:
        #             log.info("맞틀틀맞 다음으로 매매 진입합니다.")
        #             pass
        #
        #     elif subject.info[subject_code]['맞틀리스트'][-4:] == ['틀', '틀', '틀', '맞']:
        #         if subject.info[subject_code]['수익리스트'][-3] < -10:
        #             log.info("이전 플로우 수익이 10틱 이하로 매매 진입 안합니다.")
        #             return false
        #         else:
        #             log.info("틀틀틀맞 다음으로 매매 진입합니다.")
        #             pass
        #
        #     elif subject.info[subject_code]['맞틀리스트'][-4:] == ['맞', '맞', '맞', '틀']:
        #         log.info("맞맞맞틀 다음으로 매매 진입합니다.")
        #         pass
        #
        #     elif subject.info[subject_code]['맞틀리스트'][-4:] == ['틀', '틀', '맞', '맞']:
        #         log.info("틀틀맞맞 다음으로 매매 진입합니다.")
        #         pass
        #
        #     elif subject.info[subject_code]['맞틀리스트'][-4:] == ['맞', '맞', '틀', '틀']:
        #         if subject.info[subject_code]['수익리스트'][-4] < subject.info[subject_code]['수익리스트'][-3]:
        #             log.info("맞맞틀틀일때 조건이 맞지 않아 진입 안합니다.")
        #             return false
        #         else:
        #             log.info("맞맞틀틀 다음으로 매매 진입합니다.")
        #             pass
        #
        #     elif subject.info[subject_code]['맞틀리스트'][-4:] == ['맞', '틀', '틀', '틀']:
        #         if subject.info[subject_code]['수익리스트'][-2] < -10:
        #             log.info("맞틀틀틀일때 조건이 맞지 않아 진입 안합니다.")
        #             return false
        #         else:
        #             log.info("맞틀틀틀 다음으로 매매 진입합니다.")
        #             pass
        #
        #     elif subject.info[subject_code]['맞틀리스트'][-3:] == ['틀', '맞', '틀']:
        #         if subject.info[subject_code]['수익리스트'][-2] > 70:
        #             log.info("지지난 플로우가 70이상 수익으로 진입안합니다.")
        #             return false
        #         else:
        #             log.info("틀맞틀 다음으로 매매 진입합니다.")
        #             pass
        #
        #     elif subject.info[subject_code]['맞틀리스트'][-3:] == ['맞', '틀', '맞'] and profit > reverse_tic:
        #         if mesu_medo_type == '신규매도':
        #             mesu_medo_type = '신규매수'
        #         elif mesu_medo_type == '신규매수':
        #             mesu_medo_type = '신규매도'
        #         log.info("[%s] 반대매매 조건이 맞아 반대 매매 진입합니다." % mesu_medo_type)
        #         ma_line_is_true = True
        #         subject.info[subject_code]['반대매매'] = True
        #
        #     else:
        #         log.info("맞틀 조건이 맞지 않아 매매 포기합니다.")
        #         return false
        #
        # else:
        #
        #     if subject.info[subject_code]['맞틀리스트'][-1] == '맞' and profit < 0:
        #         if subject.info[subject_code]['수익리스트'][-1] > 70:
        #             log.info("지지난 플로우가 70이상 수익으로 진입안합니다.")
        #             return false
        #         else:
        #             pass
        #
        #     if profit > 160:
        #         if mesu_medo_type == '신규매도':
        #             mesu_medo_type = '신규매수'
        #         elif mesu_medo_type == '신규매수':
        #             mesu_medo_type = '신규매도'
        #         log.info("[%s] 반대매매 조건이 맞아 반대 매매 진입합니다.(전 플로우 160틱 이상 수익)4" % mesu_medo_type)
        #         ma_line_is_true = True
        #         subject.info[subject_code]['반대매매'] = True
        #
        #     elif subject.info[subject_code]['맞틀리스트'][-3:] == ['틀', '틀', '틀'] and profit < 0:
        #         if subject.info[subject_code]['수익리스트'][-1] < profit and subject.info[subject_code]['수익리스트'][-1] < -15:
        #             log.info("틀틀틀틀일때 조건이 맞지 않아 진입 안합니다.")
        #             return false
        #         else:
        #             log.info("틀틀틀틀 다음으로 매매 진입합니다.")
        #             pass
        #
        #     elif subject.info[subject_code]['맞틀리스트'][-3:] == ['틀', '맞', '맞'] and profit < 0:
        #         log.info("틀맞맞틀 다음으로 매매 진입합니다.")
        #         pass
        #
        #     elif subject.info[subject_code]['맞틀리스트'][-3:] == ['틀', '맞', '틀'] and profit < 0:
        #         log.info("틀맞틀틀 다음으로 매매 진입합니다.")
        #         pass
        #
        #     elif subject.info[subject_code]['맞틀리스트'][-3:] == ['맞', '틀', '틀'] and profit > 0:
        #         if profit > 10:
        #             log.info("이전 플로우 수익이 10틱 이상으로 매매 진입 안합니다.")
        #             return false
        #         else:
        #             log.info("맞틀틀맞 다음으로 매매 진입합니다.")
        #             pass
        #
        #     elif subject.info[subject_code]['맞틀리스트'][-3:] == ['틀', '틀', '틀'] and profit > 0:
        #         if subject.info[subject_code]['수익리스트'][-2] < -10:
        #             log.info("이전 플로우 수익이 10틱 이하로 매매 진입 안합니다.")
        #             return false
        #         else:
        #             log.info("틀틀틀맞 다음으로 매매 진입합니다.")
        #             pass
        #
        #
        #     elif subject.info[subject_code]['맞틀리스트'][-3:] == ['맞', '맞', '맞'] and profit < 0:
        #         log.info("맞맞맞틀 다음으로 매매 진입합니다.")
        #         pass
        #
        #     elif subject.info[subject_code]['맞틀리스트'][-3:] == ['틀', '틀', '맞'] and profit > 0:
        #         log.info("틀틀맞맞 다음으로 매매 진입합니다.")
        #         pass
        #
        #     elif subject.info[subject_code]['맞틀리스트'][-3:] == ['맞', '맞', '틀'] and profit < 0:
        #         if subject.info[subject_code]['수익리스트'][-3] < subject.info[subject_code]['수익리스트'][-2]:
        #             log.info("맞맞틀틀일때 조건이 맞지 않아 진입 안합니다.")
        #             return false
        #         else:
        #             log.info("맞맞틀틀 다음으로 매매 진입합니다.")
        #             pass
        #
        #     elif subject.info[subject_code]['맞틀리스트'][-3:] == ['맞', '틀', '틀'] and profit < 0:
        #         if subject.info[subject_code]['수익리스트'][-1] < -10:
        #             log.info("맞틀틀틀일때 조건이 맞지 않아 진입 안합니다.")
        #             return false
        #         else:
        #             log.info("맞틀틀틀 다음으로 매매 진입합니다.")
        #             pass
        #
        #     elif subject.info[subject_code]['맞틀리스트'][-2:] == ['틀', '맞'] and profit < 0:
        #         if subject.info[subject_code]['수익리스트'][-1] > 70:
        #             log.info("지지난 플로우가 70이상 수익으로 진입안합니다.")
        #             return false
        #         else:
        #             log.info("틀맞틀 다음으로 매매 진입합니다.")
        #             pass
        #
        #
        #     elif subject.info[subject_code]['맞틀리스트'][-2:] == ['맞', '틀'] and profit > reverse_tic:
        #         if mesu_medo_type == '신규매도':
        #             mesu_medo_type = '신규매수'
        #         elif mesu_medo_type == '신규매수':
        #             mesu_medo_type = '신규매도'
        #         log.info("[%s] 반대매매 조건이 맞아 반대 매매 진입합니다." % mesu_medo_type)
        #         ma_line_is_true = True
        #         subject.info[subject_code]['반대매매'] = True
        #
        #
        #     else:
        #         log.info("맞틀 조건이 맞지 않아 매매 포기합니다.")
        #         return false
        #
        # if ma_line_is_true == False: return false
        #
        # # if get_time(0, subject_code) > 2100 and get_time(0, subject_code) < 2230 and subject.info[subject_code][
        # #    '반대매매'] == False:
        # #    log.info("21:00~22:30 시 사이라 매매 포기 합니다.")
        # #    return false
        # if d.get_mode() == d.REAL:  # 실제 투자 할때
        #     if get_time(0, subject_code) > 2200 and get_time(0, subject_code) < 2330 and subject.info[subject_code][
        #         '반대매매'] == False:
        #         log.info("21:00~22:30 시 사이라 매매 포기 합니다.")
        #         return false
        #     elif get_time(0, subject_code) == int(subject.info[subject_code]['시작시간']) or get_time(0,
        #                                                                                           subject_code) == int(
        #             subject.info[subject_code]['마감시간']):
        #         log.info("장 시작 시간, 마감 시간 정각에 매매하지 않습니다. 매매금지")
        #         return false
        # else:
        #     if subject_code == "GCG18":
        #         if get_time(0, subject_code) > 2200 and get_time(0, subject_code) < 2330 and subject.info[subject_code][
        #             '반대매매'] == False:
        #             log.info("21:00~22:30 시 사이라 매매 포기 합니다.")
        #             return false
        #     else:
        #         if get_time(0, subject_code) > 2100 and get_time(0, subject_code) < 2230 and subject.info[subject_code][
        #             '반대매매'] == False:
        #             log.info("21:00~22:30 시 사이라 매매 포기 합니다.")
        #             return false
        #     if get_time(0, subject_code) == int(subject.info[subject_code]['시작시간']) or get_time(0, subject_code) == int(
        #             subject.info[subject_code]['마감시간']):
        #         log.info("장 시작 시간, 마감 시간 정각에 매매하지 않습니다. 매매금지")
        #         return false
        #
        # if d.get_mode() == d.REAL:  # 실제 투자 할때
        #     possible_contract_cnt = int(contract.my_deposit / subject.info[subject_code]['위탁증거금'])
        #     log.info("possible_contract_cnt %s개 입니다." % possible_contract_cnt)
        #     contract_cnt = int(contract.my_deposit / 1.2 / subject.info[subject_code]['위탁증거금'])
        #     log.info("contract_cnt %s개 입니다." % contract_cnt)
        #     if contract.recent_trade_cnt == possible_contract_cnt:
        #         contract_cnt = possible_contract_cnt
        #     log.info("매매 예정 수량은 %s개 입니다." % contract_cnt)
        #     if contract_cnt == 0:
        #         contract_cnt = 2
        #     #
        #     contract_cnt = 2
        #
        #
        # else:
        #     contract_cnt = 2  # 테스트 돌릴때
        #
        # if contract_cnt > 1:
        #     subject.info[subject_code]['신규매매수량'] = contract_cnt
        # elif contract_cnt == 1:
        #     subject.info[subject_code]['신규매매수량'] = 2
        #
        # # heejun add `17.8.16
        # number_of_current_contract = int(contract.get_contract_count(subject_code))
        # if number_of_current_contract > 0 and subject.info[subject_code]['반대매매'] == False:
        #     return false  # 계약을 가지고 있으면서 반대매매가 아니면 추가매매 금지
        #
        # if subject.info[subject_code]['반대매매'] == True:  # 만약 1계약이 1차 청산되고 1계약만 드리블 중 반전되었다면 나머지 한계약만 추가 리버스파라 매매 진입
        #     contract_cnt = contract_cnt - number_of_current_contract
        #     log.debug("반대매매 True 로 계약수 조정, 계약수: %s개" % contract_cnt)
        # ######################
        #
        # log.debug("종목코드(" + subject_code + ") 신규 매매 계약 수 " + str(contract_cnt))
        #
        # ######
        # # contract_cnt = 0
        # if contract_cnt == 0: return false
        #
        # order_contents = {'신규주문': True, '매도수구분': mesu_medo_type, '익절틱': profit_tick, '손절틱': sonjal_tick,
        #                   '수량': contract_cnt}
        # subject.info[subject_code]['주문내용'] = order_contents
        # log.debug('para.is_it_OK() : 모든 구매조건 통과.')
        # log.debug(order_contents)
        # return order_contents

    def is_it_sell(self, subject_code, current_price):
        return None