

class Chart :
    subject_code = None
    type = None
    time_unit = 0
    candles = {}

    def __init__(self):
        pass

    def __str__(self) -> str:
        return "subject_code=" + str(self.subject_code) + " type=" + str(self.type) + " time_unit=" + str(self.time_unit) + " candles=" + str(self.candles)


