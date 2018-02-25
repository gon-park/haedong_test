# -*- coding: utf-8 -*-
from variable.constant import *
from pprint import pprint
from simulate.trader import Trader
import time

TEST_SIM_LOG = True
# TEST_SIM_LOG = False


# function simulate()
#
# main_chart : 거래를 할지 정하는(?) 차트
# strategy_var : 해당 Simulate 함수에서 테스트 할 전략 변수 (1개)
# common_candles : 모든 chart 에 대한 캔들을 가지고 있는 dictionary
# result : 테스트 결과를 작성할 dictionary


def simulate(main_chart: str, strategy_var: dict, common_candles: dict, results: dict):

    if TEST_SIM_LOG:
        print('[Start] Simulate process(ppid=%d, pid=%d) ' % (os.getppid(), os.getpid()))

    '''월물 List 뽑기'''
    subject_code_list_in_common_candles = []
    for chart_id in common_candles.keys():
        subject_code, type, time_unit = chart_id.split('_')
        if subject_code not in subject_code_list_in_common_candles:
            subject_code_list_in_common_candles.append(subject_code)

    # if TEST_SIM_LOG:
    #     print("월물 List : %s" % subject_code_list_in_common_candles)

    result = []
    for _월물 in subject_code_list_in_common_candles:
        '''한개 월물씩 테스트'''
        trader = Trader(main_chart, _월물, strategy_var, common_candles)
        trader.run()
        result.append(trader.get_result())

    results.append(result)

    if TEST_SIM_LOG:
        print('[End] Simulate process(pid=%d)' % os.getpid())

    return "test"
    pass