# -*- coding: utf-8 -*-

from ..variable.constant import *
from ..manager import __manager
from ..config.json_reader import Reader
from pprint import pprint
from ..util import util


class StrategyVarManager(__manager.ManagerClass):
    def __init__(self):
        super(StrategyVarManager, self).__init__()

    def get_name(self):
        return str(self.__class__.__name__)

    def print_status(self):
        print(self.__getattribute__())

    @staticmethod
    def get_strategy_var_array():
        max_array = []
        cur_array = []
        # 전략 변수 Config 불러오기
        config = Reader.read_strategy_config()

        for strategy_name in sorted(config[STRATEGY].keys()):
            for strategy_var in sorted(config[STRATEGY][strategy_name].keys()):
                if type(config[STRATEGY][strategy_name][strategy_var]) is list:
                    util.set_strategy_var(max_array, cur_array, config[STRATEGY][strategy_name][strategy_var])

        for chart in config[CHARTS]:
            for indicator_name in sorted(chart[INDICATORS]):
                # print(indicator_name)
                for indicator_vars in chart[INDICATORS][indicator_name]:
                    for indicator_var in sorted(indicator_vars.keys()):
                        # print(indicator_var)
                        if type(indicator_vars[indicator_var]) is list:
                            util.set_strategy_var(max_array, cur_array, indicator_vars[indicator_var])

        return max_array, cur_array

    @staticmethod
    def get_speific_startegy_var(cur_array: list):
        # 전략 변수 Config 불러오기
        config = Reader.read_strategy_config()
        idx = 0
        for strategy_name in sorted(config[STRATEGY].keys()):
            for strategy_var in sorted(config[STRATEGY][strategy_name].keys()):
                if type(config[STRATEGY][strategy_name][strategy_var]) is list:
                    cnt, value = util.get_strategy_var(cur_array, idx, config[STRATEGY][strategy_name][strategy_var])
                    if cnt is not None:
                        idx = idx + cnt
                    if value is not None:
                        config[STRATEGY][strategy_name][strategy_var] = value

        for chart in config[CHARTS]:
            for indicator_name in sorted(chart[INDICATORS]):
                # print(indicator_name)
                for indicator_vars in chart[INDICATORS][indicator_name]:
                    for indicator_var in sorted(indicator_vars.keys()):
                        # print(indicator_var)
                        if type(indicator_vars[indicator_var]) is list:
                            cnt, value = util.get_strategy_var(cur_array, idx, indicator_vars[indicator_var])
                            if cnt is not None:
                                idx = idx + cnt
                            if value is not None:
                                indicator_vars[indicator_var] = value

        return config


    @staticmethod
    def increase_the_number_of_digits(max_array: list, cur_array: list):
        cur_array[-1] += 1
        for i in range(len(cur_array) - 1, -1, -1):
            if cur_array[i] > max_array[i]:
                if i == 0:
                    return False
                cur_array[i] = 0
                cur_array[i - 1] += 1
            else:
                break

        return True