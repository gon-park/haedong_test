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

    def send_order(self, info: dict, 체결시간: str):
        if info[종목코드] not in self.contracts:
            self.contracts[info[종목코드]] = []

        # 청산
        idx = 0
        while idx < len(self.contracts[info[종목코드]]):
            if info[수량] <= 0:
                break

            contract = self.contracts[info[종목코드]][idx]
            if contract.매도수구분 != info[매도수구분]:
                self.log.info("넘어온 info : %s" % info)
                체결가 = info[가격] - subject.info[contract.종목코드[:2]][단위] if info[매도수구분] is 신규매도 else info[가격] + subject.info[contract.종목코드[:2]][단위] # 슬리피지
                profit = (contract.체결표시가격 - 체결가) / subject.info[info[종목코드][:2]][단위] * subject.info[info[종목코드][:2]][틱가치] if contract.매도수구분 is 신규매도 else (체결가 - contract.체결표시가격) / subject.info[info[종목코드][:2]][단위] * subject.info[info[종목코드][:2]][틱가치]
                profit = round(profit)
                info[수량] -= 1
                del self.contracts[info[종목코드]][idx]

                self.trader.result.수익 += (profit - (수수료)) # 수익계산
                if (profit - (수수료)) > 0: self.trader.result.승 += 1
                else: self.trader.result.패 += 1

                self.log.info("[%s] 청산 체결 : %s" % (체결시간, 체결가))
                self.log.info("누적수익[%s] : %s" % (info[종목코드], self.trader.result.수익))
            else: idx += 1

        # 신규
        for i in range(0, info[수량]):
            contract = Contract()
            contract.매도수구분 = info[매도수구분]
            contract.수량 = 1
            contract.종목코드 = info[종목코드]
            contract.체결표시가격 = info[가격] - subject.info[contract.종목코드[:2]][단위] if contract.매도수구분 is 신규매도 else info[가격] + subject.info[contract.종목코드[:2]][단위]
            contract.체결표시가격 = round(contract.체결표시가격, subject.info[contract.종목코드[:2]][자릿수])
            contract.매매전략 = info[매매전략]
            contract.체결시간 = 체결시간
            self.contracts[info[종목코드]].append(contract)
            self.log.info("[%s] 신규 체결 : %s" % (체결시간, contract.__dict__))


    def get_name(self):
        return str(self.__class__.__name__)

    def print_status(self):
        print(self.__getattribute__())
