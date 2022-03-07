import sqlite3
import DataBases
import os
import time

class Supplier:

    #needs input validation
    def AddSupplier():
        '''method to add a supplier, will ask to input data'''

        #fields
        sid     = Supplier.SupplierIdGenerator()
        name    = str(input('Name     :'))
        email   = str(input('email    :'))
        address = str(input('address  :'))
        phone   = str(input('phone no.:'))

        Supplier.AddSupplierToDataBase(sid,name,email,address,phone)

    def SupplierIdGenerator():
        '''generates a new id based on prevoius supplier id'''

        #connects to database
        conn = sqlite3.connect(DataBases.DataBases.DataBaseName)
        print("Opened database Successfully")
        c = conn.cursor()

        try:
            #generate new id based on latest id
            data = conn.execute('''SELECT MAX(SID) FROM SUPPLIERS;''').fetchall()
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

    def AddSupplierToDataBase(sid,name,email,address,phone):
        """adds the data of supplier to database \nParameters: \n sid\n name\n email\n address\n phone"""

        #converting data to a list
        DataList = (sid,name,email,address,phone)

        #connects to database
        conn = sqlite3.connect(DataBases.DataBases.DataBaseName)
        print("Opened database Successfully")
        c = conn.cursor()
        try:
            #adds the supplier to database
            conn.execute('''INSERT INTO SUPPLIERS (SID,NAME,EMAIL,ADDRESS,PHONE) VALUES (?,?,?,?,?);''', DataList)
        except:
            print('exception encountered')
        finally:
            #after everything commiting and closing the tables    
            print('supplier table saved')
            conn.commit()
            conn.close()

    def ViewRecentSuppliers(NumberOfSuppliers = True):
        '''Shows Suppleiers \nParameters \n True = recent 5 \n False= all'''
        
        #connects to database
        conn = sqlite3.connect(DataBases.DataBases.DataBaseName)
        print("Opened database Successfully")
        c = conn.cursor()
        
        try:
            #checks if parameter is entered or not and return table
            
            if(NumberOfSuppliers):
                data = conn.execute('''SELECT * FROM SUPPLIERS ORDER BY SID DESC LIMIT 5 ;''').fetchall()
                return data
            else:
                data = conn.execute('''SELECT * FROM SUPPLIERS;''').fetchall()
                return data
        except:
            print('exception encountered')
            return [(None,)]
        finally:
            #after everything commiting and closing the tables    
            print('suppliers selected')
            conn.commit()
            conn.close()

    def SearchSupplierById(sid = 0):
        '''searches suppliers based on given id\nParameters:\tsid\nReturns:empty list or list of tuples/rows'''

        if(sid==0):
            print('sid not given')
            return []
        else:
            #connects to database
            conn = sqlite3.connect(DataBases.DataBases.DataBaseName)
            print("Opened database Successfully")
            c = conn.cursor()

            #adds the supplier to database
            data = conn.execute('''SELECT * from SUPPLIERS WHERE SID = ?;''', (sid,)).fetchall()

            #after everything commiting and closing the tables    
            conn.commit()
            conn.close()
            print('database closed')
            return data

    def EditSupplier():
        '''edits the details of the supplier (full function page)'''

        choice = '-1'
        while(choice!='0'):
            
            os.system('cls')
            choice = str(input('1.to view sullpiers and edit\n0.to go back\n'))
            if(choice == '1'):
                data = Supplier.ViewRecentSuppliers(False)
                for c in data: print(c)

                #in case user gives wrong input or updating fails using exception handling
                try: 
                    sid = int(input('Enter sid to be edited or 0 to go back :'))
                    if(Supplier.SearchSupplierById(sid) != []):

                        #fields
                        name    = str(input('New Name     :'))
                        email   = str(input('New email    :'))
                        address = str(input('New address  :'))
                        phone   = str(input('New phone no.:'))

                        #connects to database
                        conn = sqlite3.connect(DataBases.DataBases.DataBaseName)
                        print("Opened database Successfully")
                        c = conn.cursor()

                        #edit data in table
                        conn.execute("""UPDATE SUPPLIERS SET 
                                        NAME='"""+    name    +"""',
                                        EMAIL='"""+   email   +"""',
                                        ADDRESS='"""+ address +"""',
                                        PHONE='"""+   phone   +"""'
                                        WHERE SID="""+str(sid)+"""; """)

                        #after everything commiting and closing the tables    
                        print('Supplier Updated')
                        conn.commit()
                        conn.close()
                    else:
                        input('Supplier Dose Not Exist\nPress anything to continue:')
                except:
                    print('try again')
                    time.sleep(1)

    def RemoveSupplier():
        '''Removes supplier after checking for foreign keys'''
        choice = '-1'
        while(choice!='0'):
            
            os.system('cls')
            choice = str(input('1.to view sullpiers and remove\n0.to go back\n'))
            if(choice == '1'):
                data = Supplier.ViewRecentSuppliers(False)
                for c in data: print(c)

                #in case user gives wrong input or updating fails using exception handling
                try: 
                    sid = int(input('Enter sid to be removed or 0 to go back :'))
                    if(Supplier.SearchSupplierById(sid) != [] ):

                        #connects to database
                        conn = sqlite3.connect(DataBases.DataBases.DataBaseName)
                        print("Opened database Successfully")
                        c = conn.cursor()

                        #check for foreign keys in tables
                        data = conn.execute(''' SELECT * FROM MEDICINES WHERE SID ='''+str(sid)+';').fetchall()
                        if(len(data) != 0):
                            header = ['MID','Name','ppu','MinRequirement','SID']
                            print('this supplier supplies following medicines, delete medicines or update' +
                                  'their supplier if you want to delete the supplier')  
                            for c in data:
                                print(header[0],' = ',c[0])
                                print(header[1],' = ',c[1])
                            input('press anything to continue: ')
                            continue
                        
                        #remove data from table
                        conn.execute('''DELETE FROM SUPPLIERS WHERE SID='''+str(sid)+';')

                        #after everything commiting and closing the tables    
                        print('Supplier deleted')
                        conn.commit()
                        conn.close()
                except:
                    print('try again')
                    time.sleep(1)

    def ShowMedsBySuppliers():
        #connects to database
        conn = sqlite3.connect(DataBases.DataBases.DataBaseName)
        print("Opened database Successfully")
        c = conn.cursor()

        try:
            #check for foreign keys in tables
            data = conn.execute('''SELECT SUPPLIERS.SID,SUPPLIERS.NAME,MEDICINES.MID,MEDICINES.NAME
                                   FROM SUPPLIERS,MEDICINES 
                                   WHERE SUPPLIERS.SID = MEDICINES.SID; ''').fetchall()
            header = ['SID','SupplierName','MID','MedicineName']
            for c in data:
                print(header[0],' = ',c[0],'\t',header[1],' = ',c[1],'\t',header[2],' = ',c[2],'\t',header[3],' = ',c[3])
            input('press anything to continue: ')
            
        except:
            print('error occured please try again')
            time.sleep(1)
        finally:
            #after everything commiting and closing the tables    
            print('Supplier Meds Showed')
            conn.commit()
            conn.close()