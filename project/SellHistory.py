import sqlite3
import DataBases
import Medicine
import Stock
import os
import time
import copy

class SellHistory:
    """description of class"""

    #add it to buy history class
    def AddMedsToSellHistoryInDataBase(mid,amount,cphone,cname):
        """adds the data of supplier to database \nParameters: \n bid\n mid\n amount"""
        
        try:
            #connects to database
            conn = sqlite3.connect(DataBases.DataBases.DataBaseName)
            print("Opened database Successfully")
            c = conn.cursor()

            #adds the supplier to database
            conn.execute('''INSERT INTO SELLHISTORY (TID,MID,AMOUNT,SDATE,CPHONE,CNAME) VALUES (
                              '''+str(SellHistory.SellTransactionIdGenerator())+''',
                              '''+str(mid)+''',
                              '''+str(amount)+''',
                              DATE('now'),
                              \''''+str(cphone)+'''\',
                              \''''+str(cname)+'''\'
                            ); ''')
        except:
            print('exception encountered in AddMedsToBuyHistoryInDataBase')

        finally:
            #after everything commiting and closing the tables    
            print('Database Closed from AddMedsToBuyHistoryInDataBase')
            conn.commit()
            conn.close()

    def ViewMonthSellHistory():
        try:
            #connects to database
            conn = sqlite3.connect(DataBases.DataBases.DataBaseName)
            print("Opened database Successfully from ValidateStock")
            c = conn.cursor()

            #checks if parameter is entered or not and return table            
            data = conn.execute('''SELECT * FROM SELLHISTORY WHERE SDATE < DATE('now','+1 month')''').fetchall()
            print('Validated stock')
            return data
        except:
            print('exception encountered in ValidateStock')
            return []

        finally:
            #after everything commiting and closing the tables    
            print('database closed from ValidateStock')
            conn.commit()
            conn.close()

    def ViewCompleteSellHistory():
        try:
            #connects to database
            conn = sqlite3.connect(DataBases.DataBases.DataBaseName)
            print("Opened database Successfully from ValidateStock")
            c = conn.cursor()

            #checks if parameter is entered or not and return table            
            data = conn.execute('''SELECT * FROM SELLHISTORY''').fetchall()
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

    def SellTransactionIdGenerator():
        '''generates a new id based on prevoius Buytransaction id'''

        #connects to database
        conn = sqlite3.connect(DataBases.DataBases.DataBaseName)
        print("Opened database Successfully")
        c = conn.cursor()

        try:
            #generate new id based on latest id
            data = conn.execute('''SELECT MAX(TID) FROM SELLHISTORY;''').fetchall()
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

    def SellMeds():
        '''method to add/buy a new batch of Stock, will ask to input data'''
        
        choice = '-1'
        while(choice!='0'):
            
            #part1
            os.system('cls')
            choice = str(input('1.to view Med Types and Sell\n0.to go back\n'))#replace with input validation
            if(choice == '1'):
                data = Medicine.Medicine.ViewMedicine()
                print("MID,Name,Price,Minimum Req., Supplier ID")
                for c in data: print(c)
                
                try:                     
                    #part2
                    #fields
                    bid     = Stock.Stocks.BatchIdGenerator()
                    mid     = int(input('Mid    :'))#input validation needed

                    awailable = DataBases.DataBases.ExecuteQuery('''SELECT SUM(INSTOCK) FROM STOCKS WHERE MID = '''+str(mid)+';')[0][0]
                    print("Awailable amount is :" + str(awailable))

                    amount  = int(input('Amount :'))#input validation needed
                    cphone  = str(input('Customer Phone no.:'))
                    cname   = str(input('Customer name:'))
                    data = Medicine.Medicine.SearchMedicineById(mid)
                    if(input('''Total Price :'''+str(data[0][2]*amount)+
                             '''\nPress (y) to confirm order or anything else to reject :''') == 'y'):
                        if(amount > 0 and amount < DataBases.DataBases.ExecuteQuery('''SELECT SUM(INSTOCK) FROM STOCKS WHERE MID = '''+str(mid)+';')[0][0]):
                            temp = copy.copy(amount)
                            while(temp > 0):
                                DataBases.DataBases.ExecuteQuery('''UPDATE STOCKS SET 
                                        INSTOCK=(INSTOCK-'''+str(temp)+''')
                                        WHERE BID=(SELECT BID FROM STOCKS WHERE MID='''+str(mid)+''' ORDER BY EDATE ASC LIMIT 1);''')
                                temp = -DataBases.DataBases.ExecuteQuery('''SELECT INSTOCK FROM STOCKS WHERE MID='''+str(mid)+''' ORDER BY EDATE ASC LIMIT 1''')[0][0]
                                Stock.Stocks.ValidateStock()
                            SellHistory.AddMedsToSellHistoryInDataBase(mid,amount,cphone,cname)
                        else:
                            input("not valid amount in stock please try again \npress anything to continue")                       
                    else:
                        pass
                except:
                    print('try again')
                    time.sleep(1)
