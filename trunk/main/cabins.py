#pagina in cui si configura la cabina con il numero degli 
#strumenti al suo interno, selezionando lo strumento all' interno
#della cabina si possono inserire varie manutenzioni o sistemazioni

# view_path = "c:\\data\\Python\\view"
# view_path = "E:\\Python\\view"
# sys.path.append(view_path)

import appuifw, time, os, sys, e32db, key_codes, e32
from time import strftime
from string import replace

db = e32db.Dbms()
dbv = e32db.Db_view()

class Cabins( object ):
    ## The constructor.
    def __init__(self, dbpath):
        self.dbpath = dbpath
        self.old_title = appuifw.app.title
        self.old_quit = appuifw.app.exit_key_handler
        self.old_body = appuifw.app.body
        self.old_menu = appuifw.app.menu
        appuifw.app.title = u"Cabins Menu"
        db.open(self.dbpath)
        self.list_cabins = [u"Inserisci Cabina", u"Inserisci Strumenti", u"Inserisci Interventi" ,u"View Cabine" ,u"View Strumenti" ,u"View Ticket" , u"Back"]
        ## Bool
        self._iIsSaved = False
        # self.res_hours = appuifw.selection_list(self.list_hours)
        self._initialize_cabins()

    def back(self):
        appuifw.app.body = self.old_body
        appuifw.app.menu = self.old_menu
        appuifw.app.exit_key_handler = self.old_quit
        appuifw.app.title = self.old_title

    def _initialize_cabins(self):
        appuifw.app.menu = [(u"Select", self.select_cabins), (u"Back", self.back)]
        self.list_box_cabins = appuifw.Listbox(map(lambda x:x, self.list_cabins))
        self.list_box_cabins.bind(key_codes.EKeySelect, self.select_cabins)
        appuifw.app.body = self.list_box_cabins
        appuifw.app.exit_key_handler = self.back

    def select_cabins(self):
        res_cabins = self.list_box_cabins.current()
        if res_cabins == 0:
            self.insert_cabins()
        elif res_cabins == 1:
            self.insert_strumenti()
        elif res_cabins == 2:
            self.insert_interventi()
        elif res_cabins == 3:
            appuifw.note(u"Be done!")
        elif res_cabins == 4:
            appuifw.note(u"Be done!")
        elif res_cabins == 5:
            appuifw.note(u"Be done!")
        elif res_cabins == 6:
            self.back()

    def setActive( self ):#cabine
        # create Form
        self._iFields = [( u"Nome", "text"),
                         ( u"Regione", "text"),
                         ( u"Provincia", "text"),
                         ( u"Indirizzo", "text"),
                         ( u"Note", "text")]
        ## Mostro il form.
        self._iIsSaved = False
        self._iForm = appuifw.Form(self._iFields, appuifw.FFormDoubleSpaced+appuifw.FFormEditModeOnly)
        self._iForm.save_hook = self._markSaved
        self._iForm.execute( )
        
    def setActive_1( self ):#strumenti
        # create Form
        self._iFields = [( u"Nome", "text"),
                         ( u"Cabina", "text"),#qua dovrebbe produrre una lista delle cabine inserite
                         ( u"Note", "text")]
        ## Mostro il form.
        self._iIsSaved = False
        self._iForm = appuifw.Form(self._iFields, appuifw.FFormDoubleSpaced+appuifw.FFormEditModeOnly)
        self._iForm.save_hook = self._markSaved
        self._iForm.execute( )
    def setActive_2( self ):#interventi
        # create Form
        self._iFields = [( u"Date", "date", time.time()),
                         ( u"Cabina", "text"),#anche qua ci vorrebbe un menù con il nome di tutte le cabine inserite
                         ( u"Strumento", "text"),#idem per gli strumenti
                         ( u"Note", "text")]
        ## Mostro il form.
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

    def getNome(self):
        # return strftime("%d/%m/%Y", time.localtime(self._iForm[0][2]))
        return self._iForm[0][2]

    def getRegione(self):
        return self._iForm[1][2]

    def getProvincia( self ):
        return self._iForm[2][2]

    def getIndirizzo( self ):
        return self._iForm[3][2]

    def getNote(self):
        return self._iForm[4][2]

    ## Return date field value.
    def getDay( self ):
        return strftime("%d/%m/%Y")
    
    def getNomeStrumenti(self):
        return self._iForm[0][2]
    
    def getCabinaStrumenti(self):
        return self._iForm[1][2]
    
    def getNoteStrumenti(self):
        return self._iForm[2][2]
    
    def getDateInterventi(self):
        return self._iForm[0][2]
    
    def getCabinaInterventi(self):
        return self._iForm[1][2]
    
    def getStrumentoInterventi(self):
        return self._iForm[2][2]
    
    def getNoteInterventi(self):
        return self._iForm[2][2]
    
    def insert_cabins(self):
        old_title = appuifw.app.title
        appuifw.app.title = u"Add Cabins"
        self.setActive()
        if self.isSaved():
            # estraggo i dati che mi servono
            nome = self.getNome()
            regione = self.getRegione()
            provincia = self.getProvincia()
            indirizzo = self.getIndirizzo()
          #  strumento = self.getStrumento()
            note = self.getNote()
            #sql_string = u"INSERT INTO hours (date, hourstart, hourend, lunch, another) VALUES (%d, %d, %d, %f,'%s')" % ( date, hourstart, hourend, lunch, another )
            sql_string = u"INSERT INTO cabine (nome, regione, provincia, indirizzo, note) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (nome, regione, provincia, indirizzo, note)
            try:
                db.execute(sql_string)
            except:
                db.open(self.dbpath)
                db.execute(sql_string)
            appuifw.note(u"Saved", "conf")
            db.close()
        appuifw.app.title = old_title
        
        
    def insert_strumenti(self):
        old_title = appuifw.app.title
        appuifw.app.title = u"Add Strumenti"
        self.setActive_1()
        if self.isSaved():
            # estraggo i dati che mi servono
            nome = self.getNomeStrumenti()
            cabina = self.getCabinaStrumenti()
            note = self.getNoteStrumenti()
            sql_string = u"INSERT INTO strumenti (nome, cabina, note) VALUES ('%s', '%s', '%s')" % (nome, cabina, note)
            try:
                db.execute(sql_string)
            except:
                db.open(self.dbpath)
                db.execute(sql_string)
            appuifw.note(u"Saved", "conf")
            db.close()
        appuifw.app.title = old_title
    

    def insert_interventi(self):
        old_title = appuifw.app.title
        appuifw.app.title = u"Add Interventi"
        self.setActive_2()
        if self.isSaved():
            # estraggo i dati che mi servono
            date = self.getDateInterventi()
            cabina = self.getCabinaInterventi()
            strumento = self.getStrumentoInterventi()
            note = self.getNoteInterventi()
            sql_string = u"INSERT INTO interventi (date, cabina, strumento, note) VALUES ('%s', '%s', '%s', '%s')" % (date, cabina, strumento, note)
            try:
                db.execute(sql_string)
            except:
                db.open(self.dbpath)
                db.execute(sql_string)
            appuifw.note(u"Saved", "conf")
            db.close()
        appuifw.app.title = old_title

    def view(self):
        pass
       # import viewhours
      #  viewhours.View(self.dbpath)

