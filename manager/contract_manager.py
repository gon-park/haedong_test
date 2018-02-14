# -*- coding: utf-8 -*-
from variable.constant import *
from manager import __manager


class ContractManager(__manager.ManagerClass):
    def __init__(self):
        self.contracts = {}

    def order(self, info):
        if info[종목코드] not in self.contracts:
            self.contracts[종목코드] = []



    def get_name(self):
        return str(self.__class__.__name__)

    def print_status(self):
        print(self.__getattribute__())
