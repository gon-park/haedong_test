# -*- coding: utf-8 -*-

from manager.chart_manager import ChartManger
from manager.contract_manager import ContractManager
from variable.constant import *
from strategy import full_para
from datetime import datetime
from pprint import pprint


class Trader():

    def __init__(self, main_chart: str, subject_code: str, strategy_var: dict, common_candles: dict):
        self.charts = {}  # key 값은 chart_id(GCZ17_tick_60)로 되어있음
        self.strategy = []
        self.contracts = {}
        self.result = {}
        self.subject_code = subject_code
        self.state = '매매가능'
        self.main_chart = main_chart
        self.contract_manager = ContractManager(self)
        # 차트 생성
        self.charts = ChartManger.create_charts(subject_code, strategy_var, common_candles)

        # 매매 전략 설정
        for strategy_name in strategy_var[STRATEGY]:
            if strategy_name == 풀파라:
                self.strategy.append(full_para.FullPara(self.charts, self.subject_code, self.main_chart, strategy_var[STRATEGY][strategy_name], self.contracts))
            else:
                raise NotImplementedError

    def run(self):
        # print('trader : %s run()' % 종목코드)
        self.result[self.subject_code] = 0  # 수익

        # 한개 월물씩 테스트
        while True:
            _체결시간 = datetime(2099, 1, 1)
            체결차트 = None
            for chart_id in self.charts:
                subject_code, type, time_unit = chart_id.split('_')
                if self.subject_code != subject_code: continue

                chart = self.charts[chart_id]
                candles = chart.candles

                if (chart.index + 1) < len(candles.현재가) and \
                    (chart.candles.체결시간[chart.index + 1] < _체결시간):
                    _체결시간 = chart.candles.체결시간[chart.index + 1]
                    # 체결시간은 차트 다음캔들의 체결시간으로 비교해야함. 체결시간은 끝시간이 아니고 시작시간이기 때문에
                    체결차트 = chart

            if _체결시간 == datetime(2099, 1, 1):
                # 모든 차트 테스트 종료
                break

            for strategy in self.strategy:
                order = strategy.check_contract_in_candle(subject_code)
                if order is not None:
                    self.contract_manager.send_order(order)

            ChartManger.candle_push(체결차트, 체결차트.index + 1)

    def get_result(self):
        return self.result
