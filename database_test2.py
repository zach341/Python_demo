import os
from random import randrange as rand

COLSIZ = 10
FIELDS = ('login', 'userid', 'projid')
RDBMSs= {'s': 'sqlite','m': 'mysql','g': 'gadfly'}
DBNAME = 'test_zach'
DBUSER = 'root'
DB_EXC = None
NAMELEN = 16

tformat = lambda s: str(s).title().ljust(COLSIZ)
rformat = lambda s: s.upper().ljust(COLSIZ)

def setup():
    return RDBMSs[input('''
    Choose a database system:

    (M)ySQL
    (S)QLite
    
    Enter choice: ''').strip().lower()[0]]

def connect(db):
    global DB_EXC
    dbDir = "%s_%s"%(db, DBNAME)
    
    if db == 'sqlite':
        try:
            import sqlite3
        except ImportError:
            return None
        DB_EXC = sqlite3
        if not os.path.isdir(dbDir):
            os.mkdir(dbDir)
        cxn = sqlite3.connect(os.path.join(dbDir, DBNAME))

    elif db == 'mysql':
        try:
            import MySQLdb
            import _mysql_exceptions as DB_EXC
        
        except ImportError:
            return None

        try:
            cxn = MySQLdb.connect(db = DBNAME)
        except DB_EXC.OperationError:
            try:
                cxn = MySQLdb.connect(user = DBUSER)
                cxn.query('CREATE DATABASE %s' % DBNAME)
                cxn.commit()
                cxn.close()
                cxn = MySQLdb.connect(db = DBNAME)
            except DB_EXC.OperationError:
                return None
    else:
        return None
    return cxn

def create(cur):
    try:
        cur.execute('''
            CREATE TABLE users(
                login VARCHAR(%d),
                userid INTEGER,
                projid INTEGER)
        '''% NAMELEN)
    except DB_EXC.OperationalError:
        drop(cur)
        create(cur)

drop = lambda cur: cur.execute('DROP TABLE users')

