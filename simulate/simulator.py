from variable.constant import *


def simulate(stv, common_data, result):

    #try:
    print("%s common data id : %s" % (os.getpid(), id(common_data)))
    print("%s result id : %s" % (os.getpid(), id(result)))

    # print(common_data)
    # print(stv.info)
    print('%s simulate start.' % os.getpid())
    # print('common_data keys() : %s' % common_data.keys())
    return result
    record = {}
#     profit = 0

    tester = kiwoom_tester.KiwoomTester(stv, common_data)

    for subject_code in common_data.keys():
        log = tester.log
        log.info("pid : %s 시작" % os.getpid())
        stv_info = tester.stv.info
        sbv_info = tester.sbv.info
        log.info("pid : %s, stv : %s" %(os.getpid(), stv_info))
        chart_type = stv_info[subject_code][sbv_info[subject_code][전략]][차트][0][0]
        time_unit = stv_info[subject_code][sbv_info[subject_code][전략]][차트][0][1]

        log.info('pid : %s, 차트타입 : %s, 시간단위 : %s' % (os.getpid(), chart_type, time_unit))
        tester.run(subject_code, chart_type, time_unit)
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

    record['전략변수'] = tester.stv
    record['누적수익'] = tester.누적수익

    record['전략변수'] = os.getpid()
    record['누적수익'] = os.getpid()

    result.append(record)
    print(result)

    #except Exception as err:
    #    log.error(err)
