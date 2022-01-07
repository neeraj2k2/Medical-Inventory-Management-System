import sqlite3
import DataBases
import Medicine
import BuyHistory
import os
import time

class Stocks:
    '''Stocks Class'''

    def BatchIdGenerator():
        '''generates a new id based on prevoius Batch id'''

        try:
            #connects to database
            conn = sqlite3.connect(DataBases.DataBases.DataBaseName)
            print("Opened database Successfully form BatchIdGenerator")
            c = conn.cursor()

            #generate new id based on latest id
            data = conn.execute('''SELECT MAX(BID) FROM STOCKS;''').fetchall()
            print('batch id generated')
            if( data[0][0] == None ):
                return 1
            else:
                return data[0][0]+1

        except:
            print('exception encountered in BatchIdGenerator')

        finally:
            #after everything commiting and closing the tables    
            print('database closed from BatchIdGenerator')
            conn.commit()
            conn.close()

    def ViewStock():
        '''returns Stock in inventory'''
               
        try:
            #connects to database
            conn = sqlite3.connect(DataBases.DataBases.DataBaseName)
            print("Opened database Successfully from ViewStock")
            c = conn.cursor()

            #checks if parameter is entered or not and return table            
            data = conn.execute('''SELECT BID,STOCKS.MID,MEDICINES.NAME,EDATE,INSTOCK 
	                                FROM STOCKS,MEDICINES 
                                    WHERE STOCKS.MID = MEDICINES.MID ;''').fetchall()
            print('Stocks selected')
            return data

        except:
            print('exception encountered in ViewStock')
            return [(None,)]

        finally:
            #after everything commiting and closing the tables    
            print('DataBase Closed from ViewStock')
            conn.commit()
            conn.close()

    def SearchMedInStockByMid(mid = 0):
        '''searches Stock based on given Mid\nParameters:\tMid\nReturns:empty list or list of tuples/rows'''

        if(mid==0):
            print('Mid not given')
            return []
        else:
            try:
                #connects to database
                conn = sqlite3.connect(DataBases.DataBases.DataBaseName)
                print("Opened database Successfully from SearchMedInStockByMid")
                c = conn.cursor()

                #adds the supplier to database
                data = conn.execute('''SELECT BID,STOCKS.MID,MEDICINES.NAME,EDATE,INSTOCK
	                                    FROM STOCKS,MEDICINES 
                                        where STOCKS.MID = MEDICINES.MID and STOCKS.MID = ?;''', (mid,)).fetchall()
                print('stock selected')

            except:
                print('exception in SearchMedInStockByMid')
                return []

            finally:
                #after everything commiting and closing the tables    
                conn.commit()
                conn.close()
                print('database closed from SearchMedInStockByMid')
                return data

    def SearchMedInStockByBid(bid = 0):
        '''searches Stock based on given Bid\nParameters:\tBid\nReturns:empty list or list of tuples/rows'''

        if(bid==0):
            print('Bid not given')
            return []
        else:
            try:
                #connects to database
                conn = sqlite3.connect(DataBases.DataBases.DataBaseName)
                print("Opened database Successfully from SearchMedInStockByBid")
                c = conn.cursor()

                #adds the supplier to database
                data = conn.execute('''SELECT BID,STOCKS.MID,MEDICINES.NAME,EDATE,INSTOCK
	                                    FROM STOCKS,MEDICINES 
                                        where STOCKS.MID = MEDICINES.MID and STOCKS.BID = ?;''', (bid,)).fetchall()
                print('stock selected')
            
            except:
                print('exception in SearchMedInStockByBid')
                return []

            finally:
                #after everything commiting and closing the tables    
                conn.commit()
                conn.close()
                print('database closed from SearchMedInStockByBid')
                return data

    def ShowCertainMedInStock():
        '''returns cartain medicine's Stock in inventory'''
               
        try:
            #connects to database
            conn = sqlite3.connect(DataBases.DataBases.DataBaseName)
            print("Opened database Successfully from ViewStock")
            c = conn.cursor()

            data = Medicine.Medicine.ViewMedicine()
            print("MID,Name,Price,Minimum Req., Supplier ID")
            for i in data: print(i)

            mid = int(input('enter mid to be Searched or 0 to go back: '))
            if(Medicine.Medicine.SearchMedicineById(mid) != []):

                #cheaking for foreign keys in tables

                #checks if parameter is entered or not and return table            
                data2 = conn.execute('''SELECT BID,STOCKS.MID,MEDICINES.NAME,EDATE,SUM(INSTOCK)
	                                FROM STOCKS,MEDICINES 
                                    WHERE MEDICINES.MID = '''+str(mid)+''' AND STOCKS.MID = MEDICINES.MID
                                    GROUP BY STOCKS.MID;''').fetchall()
                header = ['BID','MID','NAME','EXPIRY','INSTOCK']
                for c in data2:
                    print(header[1],' = ',c[1])
                    print(header[2],' = ',c[2])
                    print(header[3],' = ',c[3])
                    print(header[4],' = ',c[4])  
                    input("press anything to continue:")
            else:
                input("entered mid dosent exist\npress anything to continue:")

        except:
            print('exception encountered in ViewStock')
            time.sleep(1)

        finally:
            #after everything commiting and closing the tables    
            print('DataBase Closed from ViewStock')
            conn.commit()
            conn.close()

    def AddMedsToStockInDataBase(bid,mid,amount):
        """adds the data of supplier to database \nParameters: \n bid\n mid\n amount"""

        try:
            #connects to database
            conn = sqlite3.connect(DataBases.DataBases.DataBaseName)
            print("Opened database Successfully from AddMedsToStockInDataBase")
            c = conn.cursor()

            #adds the supplier to database
            conn.execute('''INSERT INTO STOCKS (BID,MID,EDATE,INSTOCK)
                            VALUES (
                            '''+str(bid)+''',
                            '''+str(mid)+''',
                            (SELECT date('now',\''''+Medicine.Medicine.DefaultExpiryTime+'''\')),
                            '''+str(amount)+'''
                            );''')
            print('stock added to database')

        except:
            print('exception encountered in AddMedsToStockInDataBase')

        finally:
            #after everything commiting and closing the tables    
            print('Data base closed form AddMedsToStockInDataBase')
            conn.commit()
            conn.close()

    def ValidateStock():
        '''removes all expierd meds'''

        try:
            #connects to database
            conn = sqlite3.connect(DataBases.DataBases.DataBaseName)
            print("Opened database Successfully from ValidateStock")
            c = conn.cursor()

            #checks if parameter is entered or not and return table            
            conn.execute('''DELETE FROM STOCKS WHERE EDATE < DATE('now');''')
            conn.execute('''DELETE FROM STOCKS WHERE AMOUNT <= 0;''')
            print('Validated stock')
        except:
            print('exception encountered in ValidateStock')

        finally:
            #after everything commiting and closing the tables    
            print('database closed from ValidateStock')
            conn.commit()
            conn.close()

    def RemoveBatchFromStock():


        try:
            #connects to database
            conn = sqlite3.connect(DataBases.DataBases.DataBaseName)
            print("Opened database Successfully in RemoveBatchFromStock")
            c = conn.cursor()

            
            #printing Stock
            data = Stocks.ViewStock()
            print("(BID, MID, Name, Expiry, Instock)")
            for i in data: print(i)
            bid = int(input("enter the batch id to be discarded: "))

            if(Stocks.SearchMedInStockByBid(bid) != []):         
                #remove data from table
                conn.execute('''DELETE FROM STOCKS WHERE BID='''+str(bid)+';')

            else:
                input("batch dosent exist.\npress anything to continue:")

        except:
            print('Try Again')
            time.sleep(1)

        finally:
            #after everything commiting and closing the tables    
            print('Database closed from RemoveBatchFromStock')
            conn.commit()
            conn.close()

    def BuyMedsInStock():
        '''method to add/buy a new batch of Stock, will ask to input data'''
        
        choice = '-1'
        while(choice!='0'):
            
            #part1
            os.system('cls')
            choice = str(input('1.to view Med Types and Buy\n0.to go back\n'))#replace with input validation
            if(choice == '1'):
                data = Medicine.Medicine.ViewMedicine()
                print("MID, Name, Price, Minimum Req., Supplier ID")
                for c in data: print(c)
                
                try:                     
                    #part2
                    #fields
                    bid     = Stocks.BatchIdGenerator()
                    mid     = int(input('Mid    :'))#input validation needed
                    amount  = int(input('Amount :'))#input validation needed
                    data = Medicine.Medicine.SearchMedicineById(mid)
                    if(data != [] and input('Total Price :'+str(data[0][2]*amount)+'\nPress (y) to confirm order or anything else to reject :') == 'y'):
                        Stocks.AddMedsToStockInDataBase(bid,mid,amount)
                        BuyHistory.BuyHistory.AddMedsToBuyHistoryInDataBase(bid,mid,amount)
                    else:
                        pass
                except:
                    print('try again')
                    time.sleep(1)

    def EditMedsInStock():
        '''method toedit batch of Stock, will ask to input data'''
        
        choice = ''
        while(choice!='0'):
            
            #part1
            os.system('cls')
            choice = str(input('''1.to view stock and edit'''
                               '''\n0.to go back\n'''))#replace with input validation
            if(choice == '1'):
                data = Stocks.ViewStock()
                print("(BID, MID, Name, Expiry, Instock)")
                for c in data: print(c)
                
                try:                     
                    #part2
                    #fields
                    bid     = int(input('bid       :'))#input validation needed
                    amount  = int(input('New Amount:'))#input validation needed

                    if( Stocks.SearchMedInStockByBid(bid) != [] ):
                        try:
                            #connects to database
                            conn = sqlite3.connect(DataBases.DataBases.DataBaseName)
                            print("Opened database Successfully in EditMedsInStock")
                            c = conn.cursor()
                        
                            #remove data from table
                            conn.execute('''UPDATE STOCKS SET 
                                              BID='''     +str(bid)   +''',
                                              INSTOCK=''' +str(amount)+'''
                                             WHERE BID='''+str(bid)   +'''; ''')

                        except:
                            print('exception in EditMedsInStock')

                        finally:
                            #after everything commiting and closing the tables    
                            print('batch edited')
                            conn.commit()
                            conn.close()
                    else:
                        input("Batch dosent exist.\nPress anything to continue")
                except:
                    print('try again')
                    time.sleep(1)

