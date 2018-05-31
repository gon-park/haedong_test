# -*- coding: utf-8 -*-

import itertools
from datetime import datetime
from idlelib import paragraph
from random import random, randint
from strategy import full_para_

from pip.cmdoptions import cache_dir

import os
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
output = None


def end_simulate(reports: Reports):
    global current_count, total_count, start_time
    try:
        # 총 수익 계산
        for report in reports.월물:
            reports.총수익 += report.수익
            reports.승 += report.승
            reports.패 += report.패

        reports.승률 = float(reports.승) / float(reports.승 + reports.패)

        if len(simulation_report) == 0:
            simulation_report.append(reports)
            print("\r새로운 수익 갱신 : %s, %s" % (reports.총수익, reports.승률))
            fprint("새로운 수익 갱신 : %s, %s" % (reports.총수익, reports.승률))
            fprint(reports.__dict__)
        else:
            #if reports.총수익 > simulation_report[0].총수익:
            print("\r새로운 수익 갱신 : %s, %s" % (reports.총수익, reports.승률))
            print("reports : %s" % reports.전략변수)
            fprint("새로운 수익 갱신 : %s, %s" % (reports.총수익, reports.승률))
            fprint(reports.__dict__)

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
        print('\r', '[End] Simulate process(pid=%d) %s/%s (%s%%), 남은시간 : %s' % (
            reports.pid, current_count, total_count, round(float(current_count) * 100 / float(total_count)),
            remain_time),
              end='', flush=True)
    except Exception as err:
        print(err)


def fprint(params):
    output = open('output.txt', 'a+')
    print(params, file=output)
    output.close()


if __name__ == '__main__':
    # log, res, err_log = log_manager.LogManager.__call__().get_logger()
    step = itertools.count(1, 1)

    ''' 해당 종목 코드, 테스트 날짜 읽어옴 '''
    if TEST_MAIN_LOG:
        print('#%d.\t\t 테스트 변수 (strategy.json, test.json) 읽어오는 중 ...' % step.__next__())

    strategy_var = json_reader.Reader.read_strategy_config()
    start_date, end_date = json_reader.Reader.read_test_config()
    real_start_date = "20990101"
    real_end_date = "20000101"

    subject_symbol = strategy_var[SUBJECT_SYMBOL]

    _max_array, _cur_array = StrategyVarManager.get_strategy_var_array()  # 전략변수 횟수 테이블 계산
    tc = 1
    for cnt in _max_array:
        tc *= (cnt + 1)
    print('\t\t 총 TestCase : %s회' % tc)

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

    if not os.path.exists(os.path.join(os.path.curdir, 'cached_candles')):
        os.mkdir(os.path.join(os.path.curdir, 'cached_candles'))

    ''' 캐시 디렉토리 셋업 '''
    try :
        cache_dir = os.listdir('%s/%s' % (os.path.curdir, '/cached_candles'))
    except FileNotFoundError as err:
        print("Not exist 'cached_candles directory', Create the directory")
        os.makedirs('%s/%s' % (os.path.curdir, '/cached_candles'))

    ''' 기간(하루)이 지난 캐시 데이터 삭제 '''


    for file_name in cache_dir:
        file_path = '%s/%s/%s' % (os.path.curdir, '/cached_candles', file_name)
        file_datetime = datetime.strptime(time.ctime(os.path.getctime(file_path)), "%a %b %d %H:%M:%S %Y")
        if file_datetime.day is not datetime.now().day:
            os.remove(file_path)
            print('Remove Cached File(%s)' % file_name)

    for chart in strategy_var[CHARTS]:
        if main_chart is None:
            main_chart = '%s_%s' % (chart[TYPE], chart[TIME_UNIT])

        for subject_code in tables:
            # 파일이 있는지 체크하고 파일이 있으면 파일로 없으면 디비에서 틱 캔들 정보 가져오기
            chart_id = '%s_%s_%s' % (subject_code, chart[TYPE], chart[TIME_UNIT])
            if chart_id in cache_dir:
                chart_candles[chart_id] = json_reader.Reader.read_data(chart_id)
                print('         LOAD 월물별 CANDLE DATA [%s] : %s개' % (chart_id, len(chart_candles[chart_id])))

            else:
                if chart[TYPE] == TICK:
                    chart_candles[chart_id] = dbm.request_tick_candle(subject_code, chart[TIME_UNIT], start_date,
                                                                      end_date)
                    #pprint(chart_candles[chart_id])
                    if TEST_MAIN_LOG:
                        print('\t\t [%s] 로딩 된 캔들 : %s개' % (subject_code, len(chart_candles[chart_id])))

                    # save cached dir
                    json_reader.Reader.dump_data(chart_candles[chart_id], chart_id)
                    print('         DUMP 월물별 CANDLE DATA [%s] : %s개' % (chart_id, len(chart_candles[chart_id])))

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
        tmp_candles[chart_id][영업일] = []
        tmp_candles[chart_id][가격들] = []

        for candle in chart_candles[chart_id]:
            if not start_date <= candle[영업일] <= end_date:
                continue

            real_start_date = min(real_start_date, candle[영업일])
            real_end_date = max(real_end_date, candle[영업일])

            tmp_candles[chart_id][시가].append(candle[시가])
            tmp_candles[chart_id][현재가].append(candle[현재가])
            tmp_candles[chart_id][고가].append(candle[고가])
            tmp_candles[chart_id][저가].append(candle[저가])
            tmp_candles[chart_id][체결시간].append(datetime.strptime(candle[체결시간], '%Y-%m-%d %H:%M:%S'))
            tmp_candles[chart_id][거래량].append(candle[거래량])
            tmp_candles[chart_id][영업일].append(candle[영업일])
            tmp_candles[chart_id][가격들].append([float(price) for price in candle[가격들].split(',')])

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

        pool = mp.Pool(processes=mp.cpu_count() - 1)
        #pool = mp.Pool(processes=mp.cpu_count() * 2)
        # pool = mp.Pool(1)

        while True:
            config = StrategyVarManager.get_speific_startegy_var(cur_array)
            #pprint(config)
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

    for i in range(0, min(len(simulation_report), 5)):

        if TEST_MAIN_LOG:
            print('\t\t #%d 테스트 결과 : %s' % (i, simulation_report[i].__dict__))  # 더 디테일하게 변경
            fprint('\t\t #%d 테스트 결과 : %s' % (i, simulation_report[i].__dict__))

        for report in simulation_report[i].월물:
            if TEST_MAIN_LOG:
                win = report.승
                lose = report.패
                try:
                    win_lose = round((win / (win + lose) * 100),3)
                except ZeroDivisionError:
                    win_lose = 0

                print('\t\t %s: %s   승률:%s,   승:%s, 패:%s' % (report.종목코드, report.수익, win_lose, report.승, report.패 ))
                fprint('\t\t %s: %s   승률:%s,   승:%s, 패:%s' % (report.종목코드, report.수익, win_lose, report.승, report.패))

    #full_para_.FullPara.calc_reports(simulation_report)


    print("DataBase에 최고 수익의 테스트 결과가 기록됩니다. \n기록을 원치 않을 때 'N'입력하세요.")
    idx = input()
    if idx == 'N' or idx == 'n':
        exit(0)

    print("DB에 저장!!!!!")
    print('test_start_date=%s \t real_start_date=%s' % (start_date, real_start_date))
    print('test_end_date=%s \t real_end_date=%s' % (end_date, real_end_date))
    dbm.insert_test_result(simulation_report[0], real_start_date, real_end_date)


