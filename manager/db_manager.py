# -*- coding: utf-8 -*-
import pymysql
from variable.constant import *
from manager import __manager
from variable.report import Report
from variable.reports import Reports
import subprocess


class DBManager(__manager.ManagerClass):
    curs = None
    conn = None
    is_connected = False

    def __init__(self):
        super(DBManager, self).__init__()

    def connect(self):
        self.conn = pymysql.connect(host=DB_SERVER_ADDR, user=DB_USER_ID, password=DB_USER_PWD, db=DB_NAME,
                                    charset=DB_CHARSET)
        self.curs = self.conn.cursor()
        self.is_connected = True

    def disconnect(self):
        self.conn.close()

    def exec_query(self, query, fetch_type=None, fetch_count=None, cursor_type=CURSOR_TUPLE):
        if not self.is_connected:
            self.connect()

        if cursor_type == CURSOR_DICT:
            self.curs = self.conn.cursor(pymysql.cursors.DictCursor)
        elif cursor_type == CURSOR_TUPLE:
            self.curs = self.conn.cursor()

        result = self.curs.execute(query)
        self.conn.commit()

        if fetch_type == FETCH_ONE:
            return self.curs.fetchone()
        elif fetch_type == FETCH_ALL:
            return self.curs.fetchall()
        elif fetch_type == FETCH_MANY:
            return self.curs.fetchmany(fetch_count)
        else:
            return result

    def exist_table(self, table_name):
        query = "show tables in haedong4 like '%s'" % table_name

        row = self.exec_query(query, FETCH_ONE)

        if row is None:
            return False

        return True

    def drop_table(self, table_name):
        query = "drop table %s" % table_name
        return self.exec_query(query)

    def create_table(self, table_name):
        query = 'create table %s select * from root_table' % table_name
        return self.exec_query(query)

    def get_table(self, table_name, start_date=None, end_date=None):
        if start_date is not None:
            query = 'select date, price, working_day from %s' % table_name
        else:
            query = "select date, price, working_day from %s where date >= timestamp('%s') and date = timestamp('%s')" % (
            table_name, start_date, end_date)

        return self.exec_query(query, FETCH_ALL)

    def get_table_list(self, subject_symbol):
        query = '''
        SELECT 
         table_name
        FROM 
         information_schema.tables
        WHERE 
         table_schema = DATABASE()
         and
         substr(table_name, 1, %s) = '%s'
        ''' % (len(subject_symbol), subject_symbol)
        return list(self.exec_query(query, FETCH_ALL))

    def get_name(self):
        return str(self.__class__.__name__)

    def request_tick_candle(self, subject_code, tick_unit, start_date='20170101', end_date='20201231'):
        # if self.exist_table(subject_code + '_tick_10') and tick_unit % 10 == 0:
        #     tick_unit /= 10
        #     subject_code = subject_code + '_tick_10'
        #     query = '''
        #     select t1.id
        #             , date_format(t1.date, '%%Y-%%m-%%d %%H:%%i:%%s') as date
        #             , t2.open as open
        #             , t1.high
        #             , t1.low
        #             , t3.close as close
        #             , cast(t1.volume as int) as volume
        #             , date_format(t1.working_day, '%%Y%%m%%d') as working_day
        #      from (
        #            select Floor((result.row-1) / %s) + 1 as id
        #                 , date
        #                 , max(result.id) as max_id
        #                 , min(result.id) as min_id
        #                 , max(result.high) as high
        #                 , min(result.low) as low
        #                 , sum(result.volume) as volume
        #                 , working_day
        #              from (
        #                        select @rownum:=if(@working_day = s1.working_day, @rownum+1, if(@rownum=1, 1, ((truncate((@rownum-1) / %s, 0) + 1) * %s + 1))) as row,
        #                             @working_day:= s1.working_day,
        #                               s1.*
        #
        #                          from %s s1
        #                         inner join (
        #                                    select @rownum:=1, @working_day:=Date('2000-01-01')
        #                                      from dual
        #                                    ) s2
        #                   ) result
        #             group by working_day, Floor((result.row-1) / %s)
        #           ) t1
        #     inner join %s t2
        #        on t1.min_id = t2.id
        #     inner join %s t3
        #        on t1.max_id = t3.id
        #     ''' % (tick_unit, tick_unit, tick_unit, subject_code, tick_unit, subject_code, subject_code)
        # else:
        #     query = '''
        #     select t1.id
        #             , date_format(t1.date, '%%Y-%%m-%%d %%H:%%i:%%s') as date
        #             , t2.price as open
        #             , t1.high
        #             , t1.low
        #             , t3.price as close
        #             , cast(t1.volume as int) as volume
        #             , date_format(t1.working_day, '%%Y%%m%%d') as working_day
        #      from (
        #            select Floor((result.row-1) / %s) + 1 as id
        #                 , date
        #                 , max(result.id) as max_id
        #                 , min(result.id) as min_id
        #                 , max(result.price) as high
        #                 , min(result.price) as low
        #                 , sum(result.volume) as volume
        #                 , working_day
        #              from (
        #                        select @rownum:=if(@working_day = s1.working_day, @rownum+1, if(@rownum=1, 1, ((truncate((@rownum-1) / %s, 0) + 1) * %s + 1))) as row,
        #                             @working_day:= s1.working_day,
        #                               s1.*
        #
        #                          from %s s1
        #                         inner join (
        #                                    select @rownum:=1, @working_day:=Date('2000-01-01')
        #                                      from dual
        #                                    ) s2
        #                   ) result
        #             group by working_day, Floor((result.row-1) / %s)
        #           ) t1
        #     inner join %s t2
        #        on t1.min_id = t2.id
        #     inner join %s t3
        #        on t1.max_id = t3.id
        #     ;
        #     ''' % (tick_unit, tick_unit, tick_unit, subject_code, tick_unit, subject_code, subject_code)

        # print(query)
        query = '''
        select t1.id
                , date_format(t1.date, '%%Y-%%m-%%d %%H:%%i:%%s') as date
                , t2.price as open
                , t1.high
                , t1.low
                , t3.price as close
                , cast(t1.volume as int) as volume
                , date_format(t1.working_day, '%%Y%%m%%d') as working_day
                , t1.price_list
         from (
               select Floor((result.row-1) / %s) + 1 as id
                    , min(result.date) as date
                    , max(result.id) as max_id
                    , min(result.id) as min_id
                    , max(result.price) as high
                    , min(result.price) as low
                    , sum(result.volume) as volume
                    , working_day
                    , group_concat(result.price order by row) as price_list
                 from (
                            select	
                                row,
                                id,
                                date,
                                price,
                                volume,
                                working_day							
                            from		(
                                   select @rownum:=if(@working_day = s1.working_day, @rownum+1, if(@rownum=1, 1, ((truncate((@rownum-1) / %s, 0) + 1) * %s + 1))) as row,
                                        @working_day:= s1.working_day,        
                                        if( @lastPrice = s1.price, 0, 1 ) as NotEqual,                            
                                        @lastPrice := s1.price,
                                          s1.*

                                     from %s s1
                                    inner join (
                                               select @rownum:=1, @working_day:=Date('2000-01-01'), @lastPrice := 0
                                                 from dual
                                               ) s2     
                              ) result
                            where	 NotEqual = 1 or mod((row-1), %s) = 0 or mod(row, %s) = 0
                      )	result                   
                group by working_day, Floor((result.row-1) / %s)
              ) t1
        inner join %s t2
           on t1.min_id = t2.id
        inner join %s t3
           on t1.max_id = t3.id
        ;
        ''' % (tick_unit, tick_unit, tick_unit, subject_code, tick_unit, tick_unit, tick_unit, subject_code, subject_code)

        return self.exec_query(query, fetch_type=FETCH_ALL, cursor_type=CURSOR_DICT)

    def request_hour_candle(self, subject_code, time_unit, start_date='20170101', end_date='20201231'):
        return self.request_min_candle(subject_code, int(time_unit) * 60, start_date='20170101', end_date='20201231')

    def request_min_candle(self, subject_code, time_unit, start_date='20170101', end_date='20201231'):
        sec = int(time_unit) * 60
        query = '''
        SELECT 
            date_format(T1.date, '%%Y-%%m-%%d %%H:%%i:%%s') as date,
            T2.price as open,
            T1.high,
            T1.low,
            T3.price as close,
            cast(T1.volume as int) as volume,
            date_format(T1.working_day, '%%Y-%%m-%%d') as working_day
        FROM
            (
            SELECT
                from_unixtime(FLOOR(UNIX_TIMESTAMP(date) / %s) * %s) AS date,
                MIN(id) as open_id,
                MAX(price) AS high,
                MIN(price) AS low,
                MAX(id) as close_id,
                SUM(volume) AS volume,
                working_day
            FROM %s
            WHERE working_day between '%s' and '%s'
            GROUP BY FLOOR(UNIX_TIMESTAMP(date)/%s)
            ORDER BY date
            ) T1
            INNER JOIN
            %s T2
            ON T1.open_id = T2.id
            INNER JOIN
            %s T3
            ON T1.close_id = T3.id            
        ''' % (sec, sec, subject_code, start_date, end_date, sec, subject_code, subject_code)

        print(query)
        return self.exec_query(query, fetch_type=FETCH_ALL, cursor_type=CURSOR_DICT)

    def request_day_candle(self, subject_symbol, start_date='20000101', end_date='21000101'):
        query = '''
        SELECT  
            date_format(date, '%%Y-%%m-%%d 07:%%i:%%s') as date,
            open,
            high,
            low,
            close,
            volume
        FROM    %s_day
        ''' % (subject_symbol)

        print(query)
        return self.exec_query(query, fetch_type=FETCH_ALL, cursor_type=CURSOR_DICT)

    def request_week_candle(self, subject_symbol, start_date='20000101', end_date='21000101'):
        query = '''
        SELECT  
            date_format(date, '%%Y-%%m-%%d 07:%%i:%%s') as date,
            open,
            high,
            low,
            close,
            volume
        FROM    %s_week
        ''' % (subject_symbol)

        return self.exec_query(query, fetch_type=FETCH_ALL, cursor_type=CURSOR_DICT)

    def print_status(self):
        print(self.__getattribute__())

    def is_matched_table(self, table_name, c, d):
        query = '''
        select
            *
        from
            (select date(date) as s from %s order by date asc limit 1) R1
        inner join
            (select date(date) as e from %s order by date desc limit 1) R2
        ''' % (table_name, table_name)

        try:
            select_result = self.exec_query(query, fetch_type=FETCH_ONE, cursor_type=CURSOR_DICT)

            c = c[:4] + '-' + c[4:6] + '-' + c[6:]
            d = d[:4] + '-' + d[4:6] + '-' + d[6:]
            a = str(select_result['s'])
            b = str(select_result['e'])

        except Exception as err:
            print(err)

        if c <= a <= d <= b or c <= a <= b <= d or a <= c <= d <= b or a <= c <= b <= d:
            return True
        return False

    def insert_test_result(self, report_obj: Reports, start_date: str, end_date: str):
        print(type(report_obj))
        print(report_obj.__dict__)

        label = subprocess.check_output(["git", "describe", "--always"])  # current git hash
        print('git Hash tag : %s' % (label))

        query = '''
        insert
            into 
        TEST_RESULT (subject_symbol, total_profit, start_date, end_date, git_hash, strategy, result)
        values ('%s', %d, date('%s'), date('%s'), "%s", "%s", "%s")
        ;
        ''' % (report_obj.전략변수[SUBJECT_SYMBOL], report_obj.총수익, start_date, end_date, label, str(report_obj.전략변수),
               str(report_obj.__dict__))

        try:
            result = self.exec_query(query, cursor_type=CURSOR_DICT)
            print(result)
        except Exception as err:
            print(err)


if __name__ == '__main__':
    dbm = DBManager()
    result = dbm.request_tick_candle('GCJ17', 60)
    for rs in result:
        print(rs)