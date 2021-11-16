import cx_Oracle as Oracle
from DBUtils.PooledDB import PooledDB, SharedDBConnection

# 登记数据池
DJ_POOL = PooledDB(
    creator=Oracle,
    maxconnections=6,
    mincached=2,
    maxcached=5,
    maxshared=3,
    blocking=True,
    maxusage=None,
    setsession=[],
    ping=0,
    user='DJPT',
    password='Djpt2021#',
    dsn = Oracle.makedsn('172.16.17.241',1521,'orcl')
)

# 权籍数据池
QJ_POOL = PooledDB(
    creator=Oracle,
    maxconnections=4,
    mincached=2,
    maxcached=4,
    maxshared=3,
    blocking=True,
    maxusage=None,
    setsession=[],
    ping=0,
    user='CSK',
    password='Cgk2021#',
    dsn = Oracle.makedsn('172.16.17.251',1521,'orcl')
)
