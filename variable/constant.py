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
드리블틱 = "drible_tick"
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

#
INFINITY = 99999999
ZERO = 0
