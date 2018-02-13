from manager import db_manager, log_manager
from manager.strategy_var_manager import StrategyVarManager
from config import json_reader
from variable.constant import *
import multiprocessing as mp
from pprint import *
from simulate.trader import Trader

def simulate(strategy_var, common_candles, result):

    #try:
    print("%s common candles id : %s" % (os.getpid(), id(common_candles)))
    print("%s result id : %s" % (os.getpid(), id(result)))

    # print(common_data)
    # print(stv.info)
    print('%s simulate start.' % os.getpid())
    # print('common_data keys() : %s' % common_data.keys())

    subject_codes = []
    for chart_id in common_candles.keys():
        subject_code, type, time_unit = chart_id.split('_')
        print(subject_code)
        if subject_code not in subject_codes:
            subject_codes.append(subject_code)

    pprint("테스트 월물[%s]" % subject_codes)

    for subject_code in subject_codes:
        # 한개 월물씩 테스트
        trader = Trader(subject_code, strategy_var, common_candles)
        result.append(trader.run(subject_code))

#     profit = 0
#
#     tester = kiwoom_tester.KiwoomTester(stv, common_data)
#
#     for subject_code in common_data.keys():
#         log = tester.log
#         log.info("pid : %s 시작" % os.getpid())
#         stv_info = tester.stv.info
#         sbv_info = tester.sbv.info
#         log.info("pid : %s, stv : %s" %(os.getpid(), stv_info))
#         chart_type = stv_info[subject_code][sbv_info[subject_code][전략]][차트][0][0]
#         time_unit = stv_info[subject_code][sbv_info[subject_code][전략]][차트][0][1]
#
#         log.info('pid : %s, 차트타입 : %s, 시간단위 : %s' % (os.getpid(), chart_type, time_unit))
#         tester.run(subject_code, chart_type, time_unit)
        # log = kiwoom_tester.log
        # kiwoom_tester.chart.init_data(subject_code, common_data)
        #
        # stv_info = kiwoom_tester.stv.info
        # sbv_info = kiwoom_tester.sbv.info
        # chart_type = stv_info[subject_code][sbv_info[subject_code]][차트][0][0]
        # time_unit = stv_info[subject_code][sbv_info[subject_code]][차트][0][1]
        # for i in range(0, len(common_data[subject_code][chart_type][time_unit])):
        #     kiwoom_tester.chart.calc(subject_code, chart_type, 60)
        #     kiwoom_tester.chart.data[subject_code][chart_type][time_unit]['인덱스'] += 1
        #     print('process id : %s, candle index : %s' % (os.getpid(), i))
        #     order_info = kiwoom_tester.check_contract_in_candle(subject_code, chart_type, time_unit)
        #
        #     if order_info[신규매매]:
        #         kiwoom_tester.send_order(order_info[매도수구분], subject_code, order_info[수량])
        #
        # profit = profit + kiwoom_tester.누적수익

    print(result)

    #except Exception as err:
    #    log.error(err)


if __name__ == '__main__':
    log, res, err_log = log_manager.LogManager.__call__().get_logger()
    # read config
    ## test.json
    ## strategy.json (범위)

    # strategy_config = {}
    # strategy_config = read_config();

    # tick36, 60, 90 read (candle) data from DB
    # 캔들을 가진 charts를 만듬

    # while
    ## tester_var 읽고 Loop
    ## tester_var 경우의 수 만큼 charts 를 만들고
    ## charts의 candle을 위에 chart.candle 에서 copy해서 사용
    ## simulate() 시작

    ''' 해당 종목 코드, 테스트 날짜 읽어옴 '''
    strategy_var = json_reader.Reader.read_strategy_config()
    start_date, end_date = json_reader.Reader.read_test_config()
    # pprint(strategy_var)

    subject_symbol = strategy_var[SUBJECT_SYMBOL]

    ''' 해당 종목 테이블 읽어옴 '''
    dbm = db_manager.DBManager()
    temp_tables = dbm.get_table_list(subject_symbol)
    tables = []
    for table_name in temp_tables:
        # print(table_name[0], start_date, end_date)
        if dbm.is_matched_table(table_name[0], start_date, end_date):
            tables.append(table_name[0])

    # pprint(tables)

    chart_candles = {}
    for chart in strategy_var[CHARTS]:
        for subject_code in tables:
            chart_id = '%s_%s_%s' % (subject_code, chart[TYPE], chart[TIME_UNIT])
            if chart[TYPE] == TICK:
                chart_candles[chart_id] = dbm.request_tick_candle(subject_code, chart[TIME_UNIT], start_date, end_date)
            else :
                err_log("TODO")
                exit()

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
            #tmp_candles[chart_id][거래량].append(candle[거래량])

    '''
    상단까지가 우리가 입력한 날짜에 맞는 테이블을 틱_60으로만 가져오는 코드
    '''

    with mp.Manager() as manager:
        common_candles = manager.dict(tmp_candles)
        result = manager.list()

        max_array, cur_array = StrategyVarManager.get_strategy_var_array()  # 전략변수 횟수 테이블 계산
        total_count = 1
        for cnt in max_array:
            total_count *= (cnt + 1)
        log.info("총 테스트 횟수: " + str(total_count))
        # pprint(max_array)
        # pprint(cur_array)

        procs = []
        cnt = 0
        while True:
            config = StrategyVarManager.get_speific_startegy_var(cur_array)
            # pprint(config)

            ''' 해당 부분에서 Multiprocessing으로 테스트 시작 '''
            process = mp.Process(target=simulate, args=(config, common_candles, result,))
            procs.append(process)

            process.start()
            cnt = cnt + 1

            break

            if StrategyVarManager.increase_the_number_of_digits(max_array, cur_array) == False: break

        for process in procs:
            process.join()

        log.info("[테스트 결과]")

        ''' 이 부분에 result를 수익별로 sorting '''
        ''' 상위 N개의 결과 보여 줌 '''

        print(len(result))
        for i in range(0, min(len(result), 10)):
            log.info(result[i])  # 더 디테일하게 변경


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

