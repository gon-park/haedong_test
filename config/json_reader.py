# -*- coding: utf-8 -*-

import json

from manager import log_manager
from variable.constant import *
from pprint import pprint
from util import util
import collections


class Reader():

    def __init__(self):
        pass

    @staticmethod
    def read_strategy_config():
        data = json.load(open(os.path.join('config', 'strategy.json')))
        return data

    @staticmethod
    def read_test_config():
        data = json.load(open(os.path.join('config', 'test.json')))
        return data[START_DATE], data[END_DATE]

    @staticmethod
    def read_data(chart_id: str):
        data = json.load(open(os.path.join('cached_candles', chart_id)))
        return data

    @staticmethod
    def dump_data(data: dict, chart_id: str):
        dump_file = open(os.path.join('cached_candles', chart_id), 'w')
        json.dump(data, dump_file)
        dump_file.close()