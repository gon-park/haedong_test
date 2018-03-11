import os
import datetime

if __name__ == "__main__":
    dt1 = '2017-02-21 17:09:45'
    dt2 = '2017-02-21 17:09:45'
    if dt1 >= dt2:
        print(datetime.datetime.strptime('2017-02-21 17:09:45', '%Y-%m-%d %H:%M:%S'))
    else:
        print('aaaa')
