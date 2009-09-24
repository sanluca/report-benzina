#data

import appuifw, time, os, sys
from time import strftime
from string import replace

class Hours( object ):
    
    ## The constructor.
    def __init__( self ):
        
        
        self.list_hours = [u'Insert', u'View', u'Config']
        self.res_hours = appuifw.selection_list(self.list_hours)
        
        if self.res_hours == 0:
            self.insert()
            
        elif self.res_hours == 1:
            appuifw.note(u"Be done!", 'info')
       
        elif self.res_hours == 2:
            appuifw.note(u'Be done!', 'info')
    
        ## Bool
        self._iIsSaved = False
        
    def setActive( self ):
 
        # list cities
        self._place = [u'Home', u'Pordenone', u'Udine', u'Trieste', u'Milano', u'Padova']

        # create Form
        self._iFields = [( u'Date', 'date', time.time()),
                         ( u'Place of departure', 'combo', (self._place, 0)),
                         ( u'Km departure', 'float'),
                         ( u'Hour departure', 'time'),
                         ( u'Hour arrival', 'time'),
                         ( u'Place arrival', 'combo', (self._place, 0)),
                         ( u'Km arrival', 'float'),
                         ( u'Another item', 'text')]
                         
 
 
    ## Mostro il form.
    #def setActive( self ):
        self._iIsSaved = False
        self._iForm = appuifw.Form(self._iFields, appuifw.FFormDoubleSpaced+appuifw.FFormEditModeOnly)
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
    
    def getPlaceDeparture(self):
        return self._place[self._iForm[1][2][1]].encode("utf-8")
  
    def getKmDeparture( self ):
        return self._iForm[2][2]
        
    def getHourDeparture( self ):
        return self._iForm[3][2]

    def getHourArrival( self ):
        return self._iForm[4][2]
    
    def getPlaceArrival(self):
        return self._place[self._iForm[5][2][1]].encode("utf-8")
    
    def getKmArrival( self ):
        return self._iForm[6][2]

    def getAnotherItem( self ):
        return self._iForm[7][2]

    ## Return date field value.
    def getDay( self ):
        return strftime("%d/%m/%Y")
    
    def insert(self):
        
       appuifw.app.title = u'Hours Log'
       #mioForm = Benzina( )
       self.setActive( )
       if self.isSaved( ):
           # estraggo i dati che mi servono
           date = self.getDate()
           placeDeparture = self.getPlaceDeparture()
           kmDeparture = self.getKmDeparture()
           hourDeparture = self.getHourDeparture()
           hourArrival = self.getHourArrival()
           placeArrival = self.getPlaceArrival()
           kmArrival = self.getKmArrival()
           another = self.getAnotherItem()
           # scrivo i dati in una stringa
           string = "%s;%s;%s;%s;%s;%s;%s;%s\n" % (date, placeDeparture, kmDeparture, hourDeparture, hourArrival, placeArrival, kmArrival, another)
           # scrivo la stringa su un file txt
           f=open('E:\\Python\\src\\spesa.txt', 'a')
           f.write(string)
           f.close()
           appuifw.note(u"Save to file txt.","info")
    
           #scrivo nel db
           #mydb.query("create table benzina (id counter, data date, prezzolitro float, euro float, pagato text, achi text, km float, altra text)")
          # directory = "e:\\Python\\src\\"
          # dbname = "report"
         #  mydb = db(directory+dbname+'.db')
           #self.mydb.query("insert into Progetti (progetto, importo,durata) VALUES ('%s',%f,%d)" % (nome,importo,0))
          # mydb.query("insert into benzina (data, prezzolitro , euro , pagato , achi , km , altra) values('%s','%f','%f','%s','%s','%f','%s')" % (data, prezzolitro, euro, pagato, aChi, km, altra))
           appuifw.note(u"Save to database. Be done","info")
    
    
    
    
    
