import json
from manager import log_manager
from variable.constant import *
from pprint import pprint
from util import util
import collections

class Reader :

    def __init__(self):
        pass

    @staticmethod
    def read_strategy_config():
        data = json.load(open('config\\strategy.json'))
        return data

    @staticmethod
    def read_test_config():
        data = json.load(open('config\\test.json'))
        return data[START_DATE], data[END_DATE]
