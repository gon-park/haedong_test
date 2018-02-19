# -*- coding: utf-8 -*-
from pywin.mfc.object import Object


class CandleList(Object):
    시가 = []
    현재가 = []
    고가 = []
    저가 = []
    체결시간 = []
    거래량 = []

    def __init__(self):
        pass