import sqlite3
import DataBases
import Supplier
import os
import time


class Medicine:

    #Medicines attributes
    DefaultExpiryTime = '+6 month'

    def AddMedicine():
        try:
            mid     = Medicine.MIDgenerator()
            name    = str(input('Name               :'))
            price   = int(input('Price              :'))
            minreq  = int(input('Minimum requirement:'))
            data = Supplier.Supplier.ViewRecentSuppliers(False)
            for i in data: print(i)
            sid     = int(input('Supplier ID        :'))
        
            if(Supplier.Supplier.SearchSupplierById(sid) != []):
                #adding medicine to database
                Medicine.AddMedicineToDataBase(mid,name,price,minreq,sid)
            else:
                input("Given Supplier ID Dosent exist\nPress enter to continue:")
        except:
            print("try again")
            time.sleep(1)
    
    def ViewMedicine():
        '''Shows Stock in inventory'''
               
        try:
            #connects to database
            conn = sqlite3.connect(DataBases.DataBases.DataBaseName)
            print("Opened database Successfully")
            c = conn.cursor()

            #checks if parameter is entered or not and return table            
            data = conn.execute('''SELECT * FROM MEDICINES;''').fetchall()
            return data

        except:
            print('exception encountered')
            return [(None,)]

        finally:
            #after everything commiting and closing the tables    
            print('medicines selected')
            conn.commit()
            conn.close()

    def MIDgenerator():
        '''generates a new id based on prevoius Medicine id'''

        #connects to database
        conn = sqlite3.connect(DataBases.DataBases.DataBaseName)
        print("Opened database Successfully")
        c = conn.cursor()

        try:
            #generate new id based on latest id
            data = conn.execute('''SELECT MAX(MID) FROM MEDICINES;''').fetchall()
            if( data[0][0] == None ):
                return 1
            else:
                return data[0][0]+1
        except:
            print('exception encountered')
        finally:
            #after everything commiting and closing the tables    
            print('Medicine id generated db closed')
            conn.commit()
            conn.close()
    
    def AddMedicineToDataBase(mid,name,price,minreq,sid):

        DataList = (mid,name,price,minreq,sid) 

        DataBases.DataBases.CheckMedicinesTable()

        conn = sqlite3.connect(DataBases.DataBases.DataBaseName)
        print('Opened database successfully')
        c=conn.cursor()

        conn.execute('''INSERT INTO MEDICINES (MID,NAME,PRICE,MINREQ,SID) VALUES (?,?,?,?,?);''', DataList)

        print('medicine table saved')
        conn.commit()
        conn.close()
    
    def SearchMedicineById(mid = 0):

        if mid == 0:
            print('mid not given')
            return []
        else:
            conn = sqlite3.connect(DataBases.DataBases.DataBaseName)
            print('Opened database successfully')
            c=conn.cursor()

            data= conn.execute('''SELECT * FROM MEDICINES WHERE MID = ?;''', (mid,)).fetchall()

            if( data == None):
                print('Doesnt exist')
                
            conn.commit()
            conn.close()
            print('database closed')
            return data

    def EditMedicine():

        choice='-1'
        while(choice != '0'):

            os.system('cls')
            choice = str(input('1. to view medicines and edit\n0. to go back'))
            if choice =='1':
                data = Medicine.ViewMedicine()
                print("MID, Name, Price, Minimum Req., Supplier ID")
                for i in data : print(i)

                try:                    
                    conn = sqlite3.connect(DataBases.DataBases.DataBaseName)
                    print('Opened database successfully')
                    c=conn.cursor()

                    mid = int(input('enter mid to be edited or 0 to go back: '))
                    if (Medicine.SearchMedicineById(mid)!= []):

                        name    = str(input('Name               :'))
                        price   = int(input('Price              :'))
                        minreq  = int(input('Minimum requirement:'))
                        data = Supplier.Supplier.ViewRecentSuppliers(False)
                        for c in data: print(c)
                        sid     = int(input('Supplier ID        :'))
                        
                        conn.execute('''UPDATE MEDICINES SET
                                        NAME=\''''+ name + '''\',
                                        PRICE=\''''+ str(price) + '''\',
                                        MINREQ=\''''+ str(minreq)+ '''\',
                                        SID =\''''+ str(sid) +'''\' 
                                        WHERE MID='''+str(mid)+''';''')
                                           
                        print('Medicine updated')

                except:
                    print('try again')
                    time.sleep(1)

                finally:
                    conn.commit()
                    conn.close()
    
    def RemoveMedicine():

        choice=''
        while(choice != '0'):

            os.system('cls')
            choice = str(input('1. to view medicines and delete\n 0. to go back'))
            if(choice =='1'):
                data = Medicine.ViewMedicine()
                print("MID,Name,Price,Minimum Req., Supplier ID")
                for i in data : print(i)

                try:
                    conn = sqlite3.connect(DataBases.DataBases.DataBaseName)
                    print('Opened database successfully')
                    c=conn.cursor()

                    mid = int(input('enter mid to be deleted or 0 to go back'))
                    if (Medicine.SearchMedicineById(mid) != []):

                        #cheaking for foreign keys in tables

                        data2 = conn.execute('''SELECT INSTOCK FROM STOCKS WHERE MID='''+str(mid)+';').fetchall()
                        print(''' There exist ''')
                        print(str(data2[0][0] if(data2 != []) else 0))
                        print(''' amount of given medicine in the store and will be discarded on confirmation''')

                        dell=int(input('Press 1 to conform delete or press 0 to Go back:'))
                        
                        if(Medicine.SearchMedicineById(mid)[0][4] != ''):
                            conn.execute('''DELETE FROM MEDICINE WHERE MID='''+str(mid)+';')
                            print('Medicine table updated')
                        else:
                            input("u can only remove mistakenly entered medicines but not the medicines being supplied")
                        
                except:
                    print('try again')
                    time.sleep(1)

                finally:
                    conn.commit()
                    conn.close()