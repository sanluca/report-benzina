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

class Tickets( object ):
    ## The constructor.
    def __init__(self, dbpath):
        self.dbpath = dbpath
        self.old_title = appuifw.app.title
        self.old_quit = appuifw.app.exit_key_handler
        self.old_body = appuifw.app.body
        self.old_menu = appuifw.app.menu
        appuifw.app.title = u"Tickets Menu"
        db.open(self.dbpath)
        self.list_cabins = [u"Inserisci Ticket" ,u"View Ticket" , u"Back"]
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
            self.insert_tickets()
        elif res_cabins == 1:
            appuifw.note(u"Be done!")
        elif res_cabins == 2:
            self.back()

    def setActive( self ):#interventi
        # create Form
        self._iFields = [( u"Date", "date", time.time()),
                         ( u"Cabina", "text"), 
                         ( u"Strumento", "text"), 
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
    
    def getDateInterventi(self):
        return self._iForm[0][2]
    
    def getCabinaInterventi(self):
        return self._iForm[1][2]
    
    def getStrumentoInterventi(self):
        return self._iForm[2][2]
    
    def getNoteInterventi(self):
        return self._iForm[2][2]

    def insert_interventi(self):
        old_title = appuifw.app.title
        appuifw.app.title = u"Add Interventi"
        self.setActive()
        if self.isSaved():
            # estraggo i dati che mi servono
            date = self.getDateInterventi()
            cabina = self.getCabinaInterventi()
            strumento = self.getStrumentoInterventi()
            note = self.getNoteInterventi()
            sql_string = u"INSERT INTO tickets (date, cabina, strumento, note) VALUES (%d, '%s', '%s', '%s')" % (date, cabina, strumento, note)
            try:
                db.execute(sql_string)
            except:
                db.open(self.dbpath)
                db.execute(sql_string)
            appuifw.note(u"Saved", "conf")
            db.close()
        appuifw.app.title = old_title

    def view(self):
        import viewtickets
        viewtickets.View(self.dbpath)

