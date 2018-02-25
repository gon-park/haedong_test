# -*- coding: utf-8 -*-

from variable.candles import CandleList
from variable.constant import *
from variable import subject


class Variable():

    def __init__(self, candles: CandleList, indicator_info: dict):
        self.candles = candles
        self.INIT_AF = indicator_info[INIT_AF]
        self.MAX_AF = indicator_info[MAX_AF]
        self.SAR = 0.0
        self.SARS = []  # 반전되었을 시 SAR 값들을 저장, candle index와 SARS index 일치하지 않음
        self.SAR_TIMES = []
        self.FLOWS = []
        self.EP = 0.0
        self.AF = 0.0
        self.INDEX = 0
        self.맞틀리스트 = [] # 지난 플로우들의 맞틀리스트, candle index와 맞틀리스트 index 일치하지 않음
        self.FLOW = 알수없음


class Calc():

    @staticmethod
    def calc(var: Variable, index: int):
        if index < 5:
            var.FLOWS.append(None)
        elif index == 5:
            Calc.init_sar(var, index)
        else:
            Calc.calc_sar(var, index)

        var.INDEX = index

    @staticmethod
    def init_sar(var: Variable, index: int):
        ep = var.EP
        af = var.AF

        temp_high_price_list = []
        temp_low_price_list = []

        for i in range(index):
            temp_high_price_list.append(var.candles.고가[i])
            temp_low_price_list.append(var.candles.저가[i])

        score = 0

        for i in range(len(temp_high_price_list) - 1):
            if temp_high_price_list[i] < temp_high_price_list[i + 1]:
                score = score + 1
            else:
                score = score - 1

        if score >= 1:
            init_sar = min(temp_low_price_list)
            temp_flow = 상향
            ep = max(temp_high_price_list)
        if score < 1:
            init_sar = max(temp_high_price_list)
            ep = min(temp_low_price_list)
            temp_flow = 하향

        sar = ((ep - init_sar) * af) + init_sar

        var.SAR = sar
        var.SARS.append(sar)
        var.EP = ep
        var.AF = af
        var.FLOW = temp_flow
        var.FLOWS.append(temp_flow)
        Calc.calc_sar(var, index)

    @staticmethod
    def calc_sar(var: Variable, index: int):
        af = var.AF
        init_af = var.INIT_AF
        max_af = var.MAX_AF
        ep = var.EP
        temp_flow = var.FLOW
        next_sar = var.SAR

        the_highest_price = 0
        the_lowest_price = 0

        if temp_flow == 상향:
            the_highest_price = ep
        if temp_flow == 하향:
            the_lowest_price = ep

        if temp_flow == 상향:
            if var.candles.저가[index] >= next_sar:  # 상승추세에서 저가가 내일의 SAR보다 높으면 하락이 유효
                today_sar = next_sar
                temp_flow = 상향
                the_lowest_price = 0

                if var.candles.고가[index] > ep:  # 신고가 발생
                    the_highest_price = var.candles.고가[index]
                    ep = var.candles.고가[index]
                    af = af + init_af
                    if af > max_af:
                        af = max_af

            elif var.candles.저가[index] < next_sar:  # 상승추세에서 저가가 내일의 SAR보다 낮으면 하향 반전
                temp_flow = 하향
                af = init_af
                today_sar = ep
                the_highest_price = 0
                the_lowest_price = var.candles.저가[index]

                ep = the_lowest_price

                var.SARS.append(next_sar)
                var.SAR_TIMES.append(var.candles.체결시간[index])

                if var.SARS[-2] - next_sar > 0:
                    var.맞틀리스트.append(틀)
                else:
                    var.맞틀리스트.append(맞)
                #print("하향 반전, 수익 = %s, %s" % ((var.SARS[-1] - var.SARS[-2]), var.candles.체결시간[index]))
                    
        elif temp_flow == 하향:
            if var.candles.고가[index] <= next_sar:  # 하락추세에서 고가가 내일의 SAR보다 낮으면 하락이 유효
                today_sar = next_sar
                temp_flow = 하향
                the_highest_price = 0
                if var.candles.저가[index] < ep:  # 신저가 발생
                    the_lowest_price = var.candles.저가[index]
                    ep = var.candles.저가[index]
                    af = af + init_af
                    if af > max_af:
                        af = max_af

            elif var.candles.고가[index] > next_sar:  # 하락추세에서 고가가 내일의 SAR보다 높으면 상향 반전
                temp_flow = 상향
                af = init_af
                today_sar = ep
                the_lowest_price = 0
                the_highest_price = var.candles.고가[index]

                ep = the_highest_price

                var.SARS.append(next_sar)
                var.SAR_TIMES.append(var.candles.체결시간[index])

                if var.SARS[-2] - next_sar > 0:
                    var.맞틀리스트.append(맞)
                else:
                    var.맞틀리스트.append(틀)
                #print("상향 반전, 수익 = %s, %s" % ((var.SARS[-2] - var.SARS[-1]), var.candles.체결시간[index]))

        next_sar = today_sar + af * (max(the_highest_price, the_lowest_price) - today_sar)

        var.SAR = next_sar
        #print('%s, %s, %s' % (index, var.candles.체결시간[index], round(var.SAR, 2)))
        var.EP = ep
        var.AF = af
        var.FLOW = temp_flow
        var.FLOWS.append(temp_flow)
