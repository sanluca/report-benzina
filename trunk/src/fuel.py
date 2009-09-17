#data

import appuifw, time, os, sys, e32db
from time import strftime
from string import replace
#from db import db

databasepath = u'E:\\Python\\src\\test.db'
db=e32db.Dbms()
dbv=e32db.Db_view()
#db.open(u'e:\\data\\python\\test.db')

class Fuel( object ):
    
    ## The constructor.
    def __init__( self ):
        db.open(databasepath)
        try: sql_create = db.execute(u"CREATE TABLE fuel (id COUNTER, date VARCHAR, priceLiter FLOAT, euro FLOAT, paid VARCHAR, who VARCHAR, km FLOAT, another VARCHAR)")
        except: pass #gia creato
        self.list_fuel = [u'Insert', u'View', u'Config']
        self.res_fuel = appuifw.selection_list(self.list_fuel)
        
        if self.res_fuel == 0:
            self.insert()
            
        elif self.res_fuel == 1:
            self.view()
    
        elif self.res_fuel == 2:
            appuifw.note(u'Be done!', 'info')
    
        ## Bool
        self._iIsSaved = False
        
    def setActive( self ):
 
        # list of payment types
        self._payments = [u'Cash', u'Bancomat', u'Credit card', u'Check', u'Payable']
        
        # elenco fornitori 
        self._suppliers=[u'Esso', u'Agip', u'Shell']

        # creazione Form
        self._iFields = [( u'Date', 'date', time.time()),
                         ( u'Price for liter', 'float'),
                         ( u'Euro', 'float'),
                         ( u'Paid', 'combo', ( self._payments, 0 ) ),
                         ( u'Who', 'combo', ( self._suppliers, 0 ) ),
                         ( u'Km', 'number'),
                         ( u'Another item', 'text')]
                         
 
 
    ## Mostro il form.
    #def setActive( self ):
        self._iIsSaved = False
        self._iForm = appuifw.Form(self._iFields, appuifw.FFormEditModeOnly)
        self._iForm.save_hook = self._markSaved
        self._iForm.execute( )
 
 
    ## save_hook send True if the form has been saved.
    def _markSaved( self, aBool ):
        self._iIsSaved = aBool
 
                
    ## _iIsSaved getter.
    def isSaved( self ):
        return self._iIsSaved
    
    def getDate(self):
        da = time.gmtime(self._iForm[0][2])
        di = strftime("%d/%m/%Y", da)
        return di
    
    def getPriceLiter(self):
        return self._iForm[1][2]
  
    ## ritorna la spesa in euro.
    def getEuro( self ):
        # deve essere una stringa
        datoStringa = "%s" % self._iForm[2][2]
        # devo sostituire il punto con la virgola
        # euro = replace(datoStringa,'.',',')
        euro = float(datoStringa)
        return euro

    ## ritorna il tipo di Pagamento
    def getPaid( self ):
        return self._payments[self._iForm[3][2][1]].encode( "utf-8" )

    ## ritorno chi  stato pagato
    def getWho( self ):
        return self._suppliers[self._iForm[4][2][1]].encode( "utf-8" )
    
    def getKm( self ):
        return self._iForm[5][2]

    def getAnother( self ):
        return self._iForm[6][2]

    ## Return date field value.
    def getDay( self ):
        return strftime("%d/%m/%Y")
    
    def insert(self):
        appuifw.app.title = u'Fuel Log'
        #mioForm = Benzina( )
        self.setActive()
        if self.isSaved():
            #estraggo i dati che mi servono
            date = self.getDate()
            priceLiter = self.getPriceLiter()
            euro = self.getEuro()
            paid = self.getPaid()
            who = self.getWho()
            km = self.getKm()
            another = self.getAnother()
            # scrivo i dati in una stringa
            string = "%s;%s;%s;%s;%s;%s;%s\n" % (date, priceLiter, euro, paid, who, km, another)
            # scrivo la stringa su un file txt
            f=open('E:\\Python\\src\\spesa.txt', 'a')
            f.write(string)
            f.close()
            appuifw.note(u"Save to file txt.","info")
            db.open(databasepath)
            db.execute(u"INSERT INTO fuel (date, priceLiter, euro, paid, who, km, another) VALUES ('%s',%f,%f,'%s','%s',%d,'%s')" %( date, priceLiter, euro, paid, who, km, another ))
            appuifw.note(u"Save to database.","info")
	
    
    def view(self):
        #to fetch the whole dataset
        sql_string = u'SELECT * FROM fuel ORDER BY date DESC'
        try: dbv.prepare(db,sql_string)
        except:
		    db.open(databasepath)
		    dbv.prepare(db,sql_string)

        for i in range(1,dbv.count_line()+1): #1 to number of rows
            dbv.get_line() #grabs the current row
            for l in range(1,dbv.col_count()+1):
                print unicode( dbv.col(l) ) #prints each column data
            dbv.next_line() #move to the next rowset
        appuifw.Text() 
	
	
	
	
