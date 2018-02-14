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

    pprint("테스트 월물%s" % subject_codes)

    for subject_code in subject_codes:
        # 한개 월물씩 테스트
        trader = Trader(subject_code, strategy_var, common_candles)
        result.append(trader.run(subject_code))

        print(trader.charts['GCJ17_tick_60'].indicators[PARA][0].SARS)
    print(result)


if __name__ == '__main__':
    log, res, err_log = log_manager.LogManager.__call__().get_logger()

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
        if '_' not in table_name[0] and dbm.is_matched_table(table_name[0], start_date, end_date):
            tables.append(table_name[0])

    pprint(tables)

    chart_candles = {}
    for chart in strategy_var[CHARTS]:
        for subject_code in tables:
            chart_id = '%s_%s_%s' % (subject_code, chart[TYPE], chart[TIME_UNIT])
            if chart[TYPE] == TICK:
                chart_candles[chart_id] = dbm.request_tick_candle(subject_code, chart[TIME_UNIT], start_date, end_date)
                print('캔들 수 : %s' % len(chart_candles[chart_id]))
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
            tmp_candles[chart_id][거래량].append(candle[거래량])

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

        import time
        s = time.time()
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

        e = time.time()

        print("처리시간 : %s seconds" % (e-s))
        log.info("[테스트 결과]")

        ''' 이 부분에 result를 수익별로 sorting '''
        ''' 상위 N개의 결과 보여 줌 '''

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

