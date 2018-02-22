# -*- coding: utf-8 -*-
from pywin.mfc.object import Object

from variable.constant import *
from datetime import datetime


class Contract(Object):
    def __init__(self):
        self.주문번호 = 0
        self.원주문번호 = 0
        self.주문유형 = 0
        self.종목코드 = ''
        self.매도수구분 = None
        self.체결표시가격 = 0.0
        self.체결수량 = 0
        self.체결시간 = datetime(2017, 1, 1, 0, 0, 0)
        self.매매전략 = None
