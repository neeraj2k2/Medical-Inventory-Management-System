import sqlite3
import DataBases
import Medicine
import os
import time
'''WORKING NOW'''
#need to test for bugs
class BuyHistory:
    """description of class"""

    #add it to buy history class
    def AddMedsToBuyHistoryInDataBase(bid,mid,amount):
        """adds the data of supplier to database \nParameters: \n bid\n mid\n amount"""
        
        try:
            #connects to database
            conn = sqlite3.connect(DataBases.DataBases.DataBaseName)
            print("Opened database Successfully")
            c = conn.cursor()

            #adds the supplier to database
            conn.execute('''INSERT INTO BUYHISTORY (TID,BID,MID,AMOUNT,BDATE,EDATE,TPRICE) VALUES (
                              '''+str(BuyHistory.BuyTransactionIdGenerator())+''',
                              '''+str(bid)+''',
                              '''+str(mid)+''',
                              '''+str(amount)+''',
                              DATE('now'),
                              (SELECT date('now',\''''+Medicine.Medicine.DefaultExpiryTime+'''\')),
                              '''+str(amount)+'''*(SELECT PRICE FROM MEDICINES WHERE MID = '''+str(mid)+''')
                            ); ''')
                              
        except:
            print('exception encountered in AddMedsToBuyHistoryInDataBase')

        finally:
            #after everything commiting and closing the tables    
            print('Database Closed from AddMedsToBuyHistoryInDataBase')
            conn.commit()
            conn.close()

    def ViewMonthBuyHistory():
        try:
            #connects to database
            conn = sqlite3.connect(DataBases.DataBases.DataBaseName)
            print("Opened database Successfully from ValidateStock")
            c = conn.cursor()

            #checks if parameter is entered or not and return table            
            data = conn.execute('''SELECT * FROM BUYHISTORY WHERE BDATE < (SELECT DATE('now','+1 month'))''').fetchall()
            return data
            print('Validated stock')
        except:
            print('exception encountered in ValidateStock')
            return []
        finally:
            #after everything commiting and closing the tables    
            print('database closed from ValidateStock')
            conn.commit()
            conn.close()

    def ViewCompleteBuyHistory():
        try:
            #connects to database
            conn = sqlite3.connect(DataBases.DataBases.DataBaseName)
            print("Opened database Successfully from ValidateStock")
            c = conn.cursor()

            #checks if parameter is entered or not and return table            
            data = conn.execute('''SELECT * FROM BUYHISTORY''').fetchall()
            print('Got history')
            return data

        except:
            print('exception encountered in ValidateStock')
            return []

        finally:
            #after everything commiting and closing the tables    
            print('database closed from ValidateStock')
            conn.commit()
            conn.close()

    def BuyTransactionIdGenerator():
        '''generates a new id based on prevoius Buytransaction id'''

        #connects to database
        conn = sqlite3.connect(DataBases.DataBases.DataBaseName)
        print("Opened database Successfully")
        c = conn.cursor()

        try:
            #generate new id based on latest id
            data = conn.execute('''SELECT MAX(TID) FROM BUYHISTORY;''').fetchall()
            if( data[0][0] == None ):
                return 1
            else:
                return data[0][0]+1
        except:
            print('exception encountered')
        finally:
            #after everything commiting and closing the tables    
            print('Supplier id generated db closed')
            conn.commit()
            conn.close()


