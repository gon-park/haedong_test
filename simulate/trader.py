from manager.chart_manager import ChartManger
from variable.constant import *
from strategy import full_para

class Trader():
    charts = {}     # key값은 chart_id(GCZ17_tick_60)로 되어있음
    strategy = []
    results = [] # 원본 result list 마지막에 한번만 append
    result = [] # 월물별 수익 저장
    contracts = []

    def __init__(self, strategy_var, candles, results):
        # 차트 생성
        self.charts = ChartManger.create_charts(strategy_var, candles)

        # 매매 전략 설정
        for strategy_name in strategy_var[STRATEGY]:
            if strategy_name == 풀파라:
                self.strategy.append(full_para.Full_Para(self.charts))

    def send_order(self, order):
        pass

    def run(self, 종목코드):
        # 한개 월물씩 테스트
        while True:
            체결시간 = None
            체결차트 = None
            for chart_id in self.charts:
                subject_code, type, time_unit = chart_id.split('_')
                if 종목코드 != subject_code: continue

                chart = self.charts[chart_id]
                if (chart.index + 1) < len(chart.candles[현재가]) and \
                    (chart.candles[체결시간][chart.index + 1] < 체결시간 or 체결시간 is None):
                    체결시간 = chart.candles[체결시간][chart.index + 1]
                    체결차트 = chart

            ChartManger.candle_push(체결차트, 체결차트.index + 1)

            for strategy in self.strategy:
                order = strategy.check_contract_in_candle(subject_code)
                if order is not None:
                    self.send_order(order)

            if 체결시간 is None:
                # 모든 차트 테스트 종료
                break
