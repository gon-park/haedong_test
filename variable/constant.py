# -*- coding: utf-8 -*-

import os

MAIN_DIR = os.path.dirname(os.path.abspath(__file__))[:-9]
CONFIG_PATH = MAIN_DIR + '/config'

# DB
DB_SERVER_ADDR = "211.253.10.91"
DB_USER_ID = "root"
DB_USER_PWD = "goehddl"
DB_NAME = "haedong4"
DB_CHARSET = "utf8"
FETCH_ONE = 0
FETCH_ALL = 1
FETCH_MANY = 2
CURSOR_TUPLE = 0
CURSOR_DICT = 1

# CHART TYPE
TICK = "tick"
MIN = "min"
HOUR = "hour"
DAY = "day"

# STRATEGY CONFIG
SUBJECT_SYMBOL = "subject_symbol"
CHARTS = "charts"
풀파라 = "full_para"
익손절별수익계산 = "full_para_"
숏컷 = "short_cut"
수익드리블틱 = "profit_dribble_tick"
손절드리블틱 = "sonjul_dribble_tick"
TYPE = "type"
TIME_UNIT = "time_unit"
INDICATORS = "indicators"
MA = "ma"
LENGTH = "length"
PARA = "para"
INIT_AF = "init_af"
MAX_AF = "max_af"
STRATEGY = "strategy"

# TEST CONFIG
START_DATE = "start_date"
END_DATE = "end_date"

# CANDLE KEY
시가 = "open"
현재가 = "close"
고가 = "high"
저가 = "low"
체결시간 = "date"
거래량 = "volume"
영업일 = "working_day"
가격들 = "price_list"

# 숫자
INFINITY = 99999999
ZERO = 0

# 계약
신규주문 = "신규주문"
익절틱 = "profit_tick"
손절틱 = "sonjul_tick"
신규매수 = 2
신규매도 = 1
시장가 = 1
지정가 = 2
스탑 = 3
주문번호 = "주문번호"
원주문번호 = "원주문번호"
주문유형 = "주문유형"
체결표시가격 = "체결표시가격"
종목코드 = "종목코드"
신규수량 = "신규수량"
체결수량 = "체결수량"
청산수량 = "청산수량"
매도수구분 = "매도수구분"
수수료 = 15
가격 = "가격"
수량 = "수량"
매매전략 = "매매전략"

# 지표
상향 = "상향"
하향 = "하향"
알수없음 = "알수없음"
맞 = True
틀 = False
상승세 = "상승세"
하락세 = "하락세"

# 종목정보
단위 = "단위"
틱가치 = "틱가치"
자릿수 = "자릿수"

# 파라
반대매매틱 = "reverse_tick"
갱신손절틱 = "update_sonjul_tick"

# 결과
TOTAL = "TOTAL"
전략변수 = "전략변수"
수익 = "수익"
승 = "승"
패 = "패"
승률 = "승률"