import re
import pymssql
import pandas as pd
from sqlalchemy import create_engine
import sqlite3
from app.database.config import user, server, database_name, password
import hashlib
# engine = create_engine(f'mssql+pymssql://{user}:{password}@{server}/{database}')

def get_news():
    engine = create_engine(f'mssql+pymssql://{user}:{password}@{server}/{database_name}')
    pdf=pd.read_sql_query('select * from [dbo].[news]', con =engine, index_col='ID',
                          parse_dates='NDate')
    return pdf

def _get_items(table: str = '', top: int = 0, sortby: str = 'NDate'):
    assert len(table) > 0
    with pymssql.connect(host=server, user=user,
                         password=password, database=database_name) as conn:
        cursor = conn.cursor()
        strSQL = f'''SELECT top {top} * 
FROM [dbo].[{table}] 
WHERE ([dbo].[{table}].[IsVisible] <> 0) order by [{sortby}] DESC'''
        cursor.execute(strSQL)
        return [n for n in cursor]



if __name__ == '__main__':
    print(hashlib.sha1(b'cmasf 1310 news').hexdigest())
    # con3=sqlite3.connect(database='news.sqlite3')
    # pdf = get_news()
    # pdf.to_sql('news', con=con3)
    # print(pdf.tail(10))
    print('fone for dbserv')