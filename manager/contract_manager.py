# -*- coding: utf-8 -*-
from variable.constant import *
from manager import __manager
from variable import subject
from variable.contract import Contract


class ContractManager(__manager.ManagerClass):
    def __init__(self, trader):
        super().__init__()
        self.trader = trader
        self.contracts = trader.contracts

    def send_order(self, info: dict):
        if info[종목코드] not in self.contracts:
            self.contracts[info[종목코드]] = []

        # 청산
        idx = 0
        while idx < len(self.contracts[info[종목코드]]):
            if info[수량] <= 0:
                break

            contract = self.contracts[info[종목코드]][idx]
            if contract.매도수구분 != info[매도수구분]:
                profit = (contract.체결표시가격 - info[가격]) / subject.info[info[종목코드][:2]][단위] * subject.info[info[종목코드][:2]][틱가치] if contract.매도수구분 is 신규매도 else (info[가격] - contract.체결표시가격) / subject.info[info[종목코드][:2]][단위] * subject.info[info[종목코드][:2]][틱가치]
                profit = round(profit)
                info[수량] -= 1
                del self.contracts[info[종목코드]][idx]

                self.trader.result[info[종목코드]] += (profit - (2 * 수수료)) # 수익계산
                self.log.info("누적수익[%s] : %s" % (info[종목코드], self.trader.result[info[종목코드]]))
            else: idx += 1

        # 신규
        for i in range(0, info[수량]):
            contract = Contract()
            contract.매도수구분 = info[매도수구분]
            contract.수량 = 1
            contract.종목코드 = info[종목코드]
            contract.체결표시가격 = info[가격] + subject.info[contract.종목코드[:2]][단위] if contract.매도수구분 is 신규매수 else info[가격] - subject.info[contract.종목코드[:2]][단위]
            contract.체결표시가격 = round(contract.체결표시가격, subject.info[contract.종목코드[:2]][자릿수])
            contract.매매전략 = info[매매전략]
            self.contracts[info[종목코드]].append(contract)

    def get_name(self):
        return str(self.__class__.__name__)

    def print_status(self):
        print(self.__getattribute__())
