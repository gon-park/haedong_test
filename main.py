# -*- coding: utf-8 -*-

import itertools
from random import random, randint

from manager import db_manager, log_manager
from manager.strategy_var_manager import StrategyVarManager
from config import json_reader
from util.util import print_proc_time
from variable.constant import *
import multiprocessing as mp
from pprint import *
from simulate import simulator
import time

# TEST_MAIN_LOG = False
from variable.reports import Reports

TEST_MAIN_LOG = True

simulation_report = []
total_count = 0
current_count = 0

start_time = None

def end_simulate(reports: Reports):
    global current_count, total_count, start_time
    # 총 수익 계산
    for report in reports.월물:
        reports.총수익 += report.수익

    if len(simulation_report) == 0:
        simulation_report.append(reports)
        print("새로운 수익 갱신 : %s" % reports.__dict__)
    else:
        if reports.총수익 > simulation_report[0].총수익:
            print("새로운 수익 갱신 : %s" % reports.__dict__)

        for i in range(0, 10):
            if i > len(simulation_report) - 1:
                simulation_report.append(reports)
                break

            if reports.총수익 > simulation_report[i].총수익:
                simulation_report.insert(i, reports)
                break

    current_count += 1
    current_time = time.time()
    running_time = current_time - start_time
    seconds = round(running_time * float(total_count - current_count) / float(current_count))
    days = int(seconds / 86400)

    remain_time = time.strftime('%H:%M:%S', time.gmtime(seconds))
    if days > 0: remain_time = '%s일 %s' % (days, remain_time)
    print('[End] Simulate process(pid=%d) %s/%s (%s%%), 남은시간 : %s' % (reports.pid, current_count, total_count, round(float(current_count) * 100 / float(total_count)), remain_time))
    pass


if __name__ == '__main__':
    # log, res, err_log = log_manager.LogManager.__call__().get_logger()
    step = itertools.count(1, 1)

    ''' 해당 종목 코드, 테스트 날짜 읽어옴 '''
    if TEST_MAIN_LOG:
        print('#%d.\t\t 테스트 변수 (strategy.json, test.json) 읽어오는 중 ...' % step.__next__())

    strategy_var = json_reader.Reader.read_strategy_config()
    start_date, end_date = json_reader.Reader.read_test_config()

    subject_symbol = strategy_var[SUBJECT_SYMBOL]

    ''' 해당 종목 테이블 읽어옴 '''
    if TEST_MAIN_LOG:
        print('#%d.\t\t DB 데이터 (종목 & 캔들) 로딩 중...' % step.__next__())

    dbm = db_manager.DBManager()
    temp_tables = dbm.get_table_list(subject_symbol)
    tables = []
    for table_name in temp_tables:
        # print(table_name[0], start_date, end_date)
        if '_' not in table_name[0] and dbm.is_matched_table(table_name[0], start_date, end_date):
            tables.append(table_name[0])

    chart_candles = {}
    '''주거래 차트, charts 의 0번째 인덱스에 있는 차트로 선택'''
    main_chart = None
    for chart in strategy_var[CHARTS]:
        if main_chart is None:
            main_chart = '%s_%s' % (chart[TYPE], chart[TIME_UNIT])

        for subject_code in tables:
            chart_id = '%s_%s_%s' % (subject_code, chart[TYPE], chart[TIME_UNIT])

            if chart[TYPE] == TICK:
                chart_candles[chart_id] = dbm.request_tick_candle(subject_code, chart[TIME_UNIT], start_date, end_date)
                if TEST_MAIN_LOG:
                    print('\t\t [%s] 로딩 된 캔들 : %s개' % (subject_code, len(chart_candles[chart_id])))

            else:
                # TODO
                print("TODO")
                exit(-1)

    '''차트 기본 데이터(캔들) 만들기'''
    if TEST_MAIN_LOG:
        print('#%d.\t\t 데이터 캔들 형식 변환...' % step.__next__())

    tmp_candles = {}
    # chart_candles 변환
    for chart_id in chart_candles.keys():
        tmp_candles[chart_id] = {}
        tmp_candles[chart_id][시가] = []
        tmp_candles[chart_id][현재가] = []
        tmp_candles[chart_id][고가] = []
        tmp_candles[chart_id][저가] = []
        tmp_candles[chart_id][체결시간] = []
        tmp_candles[chart_id][거래량] = []

        for candle in chart_candles[chart_id]:
            tmp_candles[chart_id][시가].append(candle[시가])
            tmp_candles[chart_id][현재가].append(candle[현재가])
            tmp_candles[chart_id][고가].append(candle[고가])
            tmp_candles[chart_id][저가].append(candle[저가])
            tmp_candles[chart_id][체결시간].append(candle[체결시간])
            tmp_candles[chart_id][거래량].append(candle[거래량])

    '''상단까지가 우리가 입력한 날짜에 맞는 테이블을 Tick_60 으로만 가져오는 코드'''

    start_time = time.time()
    with mp.Manager() as manager:
        common_candles = manager.dict(tmp_candles)
        # result = manager.list()

        max_array, cur_array = StrategyVarManager.get_strategy_var_array()  # 전략변수 횟수 테이블 계산
        total_count = 1
        for cnt in max_array:
            total_count *= (cnt + 1)

        s = time.time()
        procs_results = []

        if TEST_MAIN_LOG:
            print('#%d.\t\t 병렬 테스트 수행 (Core 수=%d, 횟수=%d)' % (step.__next__(), (mp.cpu_count() - 1), total_count))

        pool = mp.Pool(processes=mp.cpu_count())
        # pool = mp.Pool(1)

        while True:
            config = StrategyVarManager.get_speific_startegy_var(cur_array)

            ''' 해당 부분에서 Multiprocessing 으로 테스트 시작 '''
            procs_results.append(pool.apply_async(func=simulator.simulate, args=(main_chart, config, common_candles,),
                                                  callback=end_simulate))

            if StrategyVarManager.increase_the_number_of_digits(max_array, cur_array) is False:
                break

        pool.close()
        pool.join()

        e = time.time()

        ''' 이 부분에 result 를 수익별로 sorting '''
        ''' 상위 N개의 결과 보여 줌 '''

        if TEST_MAIN_LOG:
            print('#Fin\t 시뮬레이션 종료 처리시간 : %s s' % (e - s))

        if TEST_MAIN_LOG:
            for procs_result in procs_results:
                if not procs_result.successful():
                    print(procs_result.get())
        #
        # # 정렬
        # for i in range(0, len(simulation_report)):
        #     for j in range(i + 1, len(simulation_report)):
        #         if simulation_report[i].총수익 < simulation_report[j].총수익:
        #             simulation_report[i], simulation_report[j] = simulation_report[j], simulation_report[i]

        for i in range(0, min(len(simulation_report), 10)):
            # TODO
            # if TEST_MAIN_LOG:
            print('\t\t #%d 테스트 결과 : %s' % (i, simulation_report[i].__dict__))  # 더 디테일하게 변경
            for report in simulation_report[i].월물:
                print('\t\t %s: %s' % (report.종목코드, report.수익))
            # log.info("해당 코드의 Git Hash : %s" % label)
            # while True:
            #     log.info("Database에 넣을 결과 Index를 입력해주세요.(종료 : -1)")
            #     idx = input()
            #     if idx == '-1': break
            #     log.info("저장하신 결과에 대한 코드를 나중에 확인하시기 위해선, 코드를 변경하시기 전에 Commit을 해야 합니다.")
            #
            #     ''' 해당 index의 결과를 stv를 정렬해서, 결과 DB에 저장. '''
            #
            # log.info("Config를 변경하여 계속 테스트 하시려면 아무키나 눌러주세요.(종료 : exit)")
            # cmd = input()
            # if cmd == 'exit': break
            #
            # log.info('테스트 종료.')
