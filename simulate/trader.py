from manager.chart_manager import ChartManger
from variable.constant import *
from strategy import full_para

class Trader():
    charts = {}     # key값은 chart_id(GCZ17_tick_60)로 되어있음
    strategy = []
    contracts = []
    result = []
    subject_code = ''

    def __init__(self, subject_code, strategy_var, candles):
        self.subject_code = subject_code
        # 차트 생성
        self.charts = ChartManger.create_charts(subject_code, strategy_var, candles)

        # 매매 전략 설정
        for strategy_name in strategy_var[STRATEGY]:
            if strategy_name == 풀파라:
                self.strategy.append(full_para.Full_Para(self.charts))

    def send_order(self, order):
        pass

    def run(self, 종목코드):
        self.result = []

        # 한개 월물씩 테스트
        while True:
            _체결시간 = None
            체결차트 = None
            for chart_id in self.charts:
                subject_code, type, time_unit = chart_id.split('_')
                if 종목코드 != subject_code: continue

                chart = self.charts[chart_id]
                if (chart.index + 1) < len(chart.candles[현재가]) and \
                    (chart.candles[체결시간][chart.index + 1] < 체결시간 or 체결시간 is None):
                    _체결시간 = chart.candles[체결시간][chart.index + 1]
                    체결차트 = chart

            if _체결시간 is None:
                # 모든 차트 테스트 종료
                break

            ChartManger.candle_push(체결차트, 체결차트.index + 1)

            for strategy in self.strategy:
                order = strategy.check_contract_in_candle(subject_code)
                if order is not None:
                    self.send_order(order)


        return self.result
