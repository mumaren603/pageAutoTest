import cx_Oracle as Oracle
from DBUtils.PooledDB import PooledDB

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
    password='DJPT',
    dsn = Oracle.makedsn('192.168.1.10',1521,'sqdj')
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
    user='CGKCSS',
    password='CGKCSS',
    dsn = Oracle.makedsn('192.168.1.251',1521,'orcl')
)
