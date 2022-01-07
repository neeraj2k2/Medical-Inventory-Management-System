import sqlite3
class DataBases:
    
    #Database attributes
    DataBaseName = "initialization.db"

    #initialise database
    def start():
        print('initialisation started')
        DataBases.CheckSuppliersTable()
        DataBases.CheckMedicinesTable()
        DataBases.CheckStocksTable()
        DataBases.CheckBuyHistoryTable()
        DataBases.CheckSellHistoryTable()
        print('tables initialised')

    #check existance of suppliers table
    def CheckSuppliersTable():

        #connects to database
        conn = sqlite3.connect(DataBases.DataBaseName)
        print("Opened database Successfully")
        c = conn.cursor()

        #checks if suppliers table is present
        c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='SUPPLIERS' ''')
        if c.fetchone()[0] == 1:
            print('supplier table exists')
        else:
            c.execute('''CREATE TABLE SUPPLIERS
                       (SID     INT          PRIMARY KEY NOT NULL,
                        NAME    TEXT                     NOT NULL,
                        EMAIL   VARCHAR(30)              NOT NULL,
                        ADDRESS VARCHAR(30)              NOT NULL,
                        PHONE   VARCHAR(30)              NOT NULL
                       );''')
            print('supplier table created')

        #after everything commiting and closing the tables    
        print('supplier table initialised')
        conn.commit()
        conn.close()

    #check existance of medicines table
    def CheckMedicinesTable():

        #connects to database
        conn = sqlite3.connect(DataBases.DataBaseName)
        print("Opened database Successfully")
        c = conn.cursor()

        #check if medicines table is present
        c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='MEDICINES' ''')
        if c.fetchone()[0] == 1:
            print('medicines table exists')
        else:
            c.execute('''CREATE TABLE MEDICINES
                       (MID     INT         PRIMARY KEY NOT NULL,
                        NAME    VARCHAR(20)             NOT NULL,
                        PRICE   INT                     NOT NULL,
                        MINREQ  INT                     NOT NULL,
                        SID     INT                     NOT NULL,
                        FOREIGN KEY(SID)
                        	REFERENCES SUPPLIERS(SID)
                       );''')
            print('medicines table created')

        #after everything commiting and closing the tables    
        print('medicines table initialised')
        conn.commit()
        conn.close()

    #check existance of stocks table
    def CheckStocksTable():

        #connects to database
        conn = sqlite3.connect(DataBases.DataBaseName)
        print("Opened database Successfully")
        c = conn.cursor()

        #check if stocks table is present
        c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='STOCKS' ''')
        if c.fetchone()[0] == 1:
            print('stocks table exists')
        else:
            c.execute('''CREATE TABLE STOCKS
					    (BID     INT PRIMARY KEY NOT NULL,
                         MID     INT             NOT NULL,
                         EDATE   DATE            NOT NULL,
                         INSTOCK INT             NOT NULL,
                         FOREIGN KEY(MID)
                     	     REFERENCES MEDICINES(MID)
                        );''')
            print('stocks table created')

        #after everything commiting and closing the tables    
        print('stocks table initialised')
        conn.commit()
        conn.close()

    #check existance of buyhistory table
    def CheckBuyHistoryTable():

        #connects to database
        conn = sqlite3.connect(DataBases.DataBaseName)
        print("Opened database Successfully")
        c = conn.cursor()

        #check if buyhistory table is present
        c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='BUYHISTORY' ''')
        if c.fetchone()[0] == 1:
            print('buyhistory table exists')
        else:
            c.execute('''CREATE TABLE BUYHISTORY
						(TID INT PRIMARY KEY NOT NULL,
                         BID INT             NOT NULL,
                         MID INT             NOT NULL,
                         AMOUNT INT          NOT NULL,
                         BDATE DATE          NOT NULL,
                         EDATE DATE          NOT NULL,
                         TPRICE FLOAT        NOT NULL,
                         FOREIGN KEY(MID)
                         	REFERENCES MEDICINES(MID)
                        );''')
            print('buyhistory table created')

        #after everything commiting and closing the tables    
        print('buyhistory table initialised')
        conn.commit()
        conn.close()

    #check existance of sellhistory table
    def CheckSellHistoryTable():

        #connects to database
        conn = sqlite3.connect(DataBases.DataBaseName)
        print("Opened database Successfully")
        c = conn.cursor()

        #check if SELLHISTORY table is present
        c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='SELLHISTORY' ''')
        if c.fetchone()[0] == 1:
            print('sellhistory table exists')
        else:
            c.execute('''CREATE TABLE SELLHISTORY
						(TID    INT PRIMARY KEY NOT NULL,
                         MID    INT             NOT NULL,
                         AMOUNT INT             NOT NULL,
                         SDATE  DATE            NOT NULL,
                         CPHONE VARCHAR(20)     NOT NULL,
                         CNAME  TEXT                    ,
                         FOREIGN KEY(MID)
                         	REFERENCES MEDICINES(MID)
                        );''')
            print('sellhistory table created')

        #after everything commiting and closing the tables    
        print('sellhistory table initialised')
        conn.commit()
        conn.close()

    def ExecuteQuery(query):
        '''executes SQLite3 queries'''
        try:
            #connects to database
            conn = sqlite3.connect(DataBases.DataBaseName)
            print("Opened database Successfully")
            c = conn.cursor()
                        
            #executes query
            data = conn.execute(query).fetchall()
            return data
        except:
            print('exception')
            return []

        finally:
            #after everything commiting and closing the tables    
            print('Database closed')
            conn.commit()
            conn.close()

