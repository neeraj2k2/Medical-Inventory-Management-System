import os
import time
import datetime
import sqlite3
import DataBases
import Supplier
import Medicine
import Stock
import BuyHistory
import SellHistory

DataBases.DataBases.start()

choice = ''
while(choice != '0'):
    os.system("cls")
    
    #frontPage
    choice = str(input('\n1.Sell Meds' +
                       '\n2.Buy Meds' +
                       '\n3.View History' +
                       '\n4.Medicines Data CRUD' +
                       '\n5.Suppliers Data CRUD' +
                       '\n6.Stock' +
                       '\n0.Quit' +
                       '\nInput : '))

    if(choice == '1'):
        SellHistory.SellHistory.SellMeds()
    
    elif(choice == '2'):
        Stock.Stocks.BuyMedsInStock()

    elif(choice == '3'):
        choice2 = ''
        while(choice2 != '0'):
            os.system("cls")

            #2ndPage
            choice2 = str(input('\n1.View Mounths sell history' +
                                '\n2.View complete sell History' +
                                '\n3.View Months Buy Histoy' +
                                '\n4.View Complete Buy History' +
                                '\n0.Quit'      +
                                '\nInput : '))
            if(choice2 == '1'):
                data = SellHistory.SellHistory.ViewMonthSellHistory()
                print("TID, MID, Amount, Date, phone, Name")
                for i in data: print(i)
                input("press anything to continue")
            elif(choice2 == '2'):
                data = SellHistory.SellHistory.ViewCompleteSellHistory()
                print("TID, MID, Amount, Date, phone, Name")
                for i in data: print(i)
                input("press anything to continue")
            elif(choice2 == '3'):
                data = BuyHistory.BuyHistory.ViewMonthBuyHistory()
                print("TID, Bid, MID, Amount, Date, Expiry, Price")
                for i in data: print(i)
                input("press anything to continue")
            elif(choice2 == '4'):
                data = BuyHistory.BuyHistory.ViewCompleteBuyHistory()
                print("TID, Bid, MID, Amount, Date, Expiry, Price")
                for i in data: print(i)
                input("press anything to continue")
            else:
                pass

    elif(choice == '4'):
        choice2 = ''
        while(choice2 != '0'):
            os.system("cls")

            #2ndPage
            choice2 = str(input('\n1.Add a new Medicine' +
                                '\n2.Update Old Medicine\'s data' +
                                '\n3.View All Medicines' +
                                '\n0.Quit'      +
                                '\nInput : '))
            if(choice2 == '1'):
                Medicine.Medicine.AddMedicine()
            elif(choice2 == '2'):
                Medicine.Medicine.EditMedicine()
            elif(choice2 == '3'):
                data = Medicine.Medicine.ViewMedicine()
                print("MID,Name,Price,Minimum Req., Supplier ID")
                for i in data : print(i)
                input()
            else:
                pass

    elif(choice == '5'):
        choice2 = ''
        while(choice2 != '0'):
            os.system("cls")

            #2ndPage
            choice2 = str(input('\n1.Add a new Supplier' +
                                '\n2.Remove Old Supplier\'s data' +
                                '\n3.Update Old Supplier\'s data' +
                                '\n4.View All Supplier' +
                                '\n5.Show Meds By Supplier' +
                                '\n0.Quit'      +
                                '\nInput : '))
            if(choice2 == '1'):
                Supplier.Supplier.AddSupplier()
            elif(choice2 == '2'):
                Supplier.Supplier.RemoveSupplier()
            elif(choice2 == '3'):
                Supplier.Supplier.EditSupplier()
            elif(choice2 == '4'):
                data = Supplier.Supplier.ViewRecentSuppliers(False)
                print("SID,Name,EMAIL,Address,Phone")
                for i in data : print(i)
                input()
            elif(choice2 == '5'):
                Supplier.Supplier.ShowMedsBySuppliers()
            else:
                pass

    elif(choice == '6'):
        choice2 = ''
        while(choice2 != '0'):
            os.system("cls")

            #2ndPage
            choice2 = str(input('\n1.View Stock' +
                                '\n2.Refresh Stock' +
                                '\n3.Discard Batch' +
                                '\n4.Edit Batch' +
                                '\n5.Search Med In Stock'
                                '\n0.Quit'      +
                                '\nInput : '))
            if(choice2 == '1'):
                data = Stock.Stocks.ViewStock()
                print("(BID, MID, Name, Expiry, Instock)")
                for i in data: print(i)
                input('press anyting to continue: ')
            elif(choice2 == '2'):
                Stock.Stocks.ValidateStock()
            elif(choice2 == '3'):
                Stock.Stocks.RemoveBatchFromStock()
            elif(choice2 == '4'):
                Stock.Stocks.EditMedsInStock()
            elif(choice2 == '5'):
                Stock.Stocks.ShowCertainMedInStock()

    else:
        pass