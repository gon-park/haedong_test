# -*- coding: utf-8 -*-

import abc
import inspect

from manager import log_manager
from variable.report import Report


class BaseStrategy(metaclass=abc.ABCMeta):
    log, res, err_log = None, None, None

    def __init__(self):
        super(BaseStrategy, self).__init__()
        self.init_logger()

    @abc.abstractmethod
    def is_it_ok(self, subject_code, current_price):
        raise NotImplementedError(inspect.stack()[0][3] + ' is not implemented.')

    @abc.abstractmethod
    def is_it_sell(self, subject_code, current_price):
        raise NotImplementedError(inspect.stack()[0][3] + ' is not implemented.')

    @abc.abstractmethod
    def check_contract_in_candle(self, subject_code):
        raise NotImplementedError(inspect.stack()[0][3] + ' is not implemented.')

    @abc.abstractmethod
    def check_contract_in_tick(self, subject_code, current_price):
        raise NotImplementedError(inspect.stack()[0][3] + ' is not implemented.')

    @abc.abstractmethod
    def post_trade(self, report: Report):
        raise NotImplementedError(inspect.stack()[0][3] + ' is not implemented.')

    @staticmethod
    def get_contract_count(subject_code, contracts, strategy):
        count = 0
        for contract in contracts[subject_code]:
            if contract.매매전략 == strategy and contract.종목코드 == subject_code:
                count += 1

        return count

    @staticmethod
    def get_contracts(subject_code, contracts, strategy):
        c = []
        for contract in contracts[subject_code]:
            if contract.매매전략 == strategy and contract.종목코드 == subject_code:
                c.append(contract)

        return c

    def init_logger(self):
        self.log, self.res, self.err_log = log_manager.LogManager().get_logger()

