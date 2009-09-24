import appuifw, time, os, sys, e32db, key_codes, e32
from time import strftime
from string import replace

db = e32db.Dbms()
dbv = e32db.Db_view()

class Hours( object ):
	## The constructor.
	def __init__(self, dbpath):
		self.dbpath = dbpath
		self.old_title = appuifw.app.title
		self.old_quit = appuifw.app.exit_key_handler
		self.old_body = appuifw.app.body
		self.old_menu = appuifw.app.menu
		appuifw.app.title = u"Hours Menu"
		db.open(self.dbpath)
		self.list_hours = [u'Insert', u'View', u'Config']
		## Bool
		self._iIsSaved = False
		# self.res_hours = appuifw.selection_list(self.list_hours)
		self._initialize_hours()

	def back(self):
		appuifw.app.body = self.old_body
		appuifw.app.menu = self.old_menu
		appuifw.app.exit_key_handler = self.old_quit
		appuifw.app.title = self.old_title

	def _initialize_hours(self):
		appuifw.app.menu = [(u"Select", self.select_hours), (u"Back", self.back)]
		self.list_box_hours = appuifw.Listbox(map(lambda x:x, self.list_hours))
		self.list_box_hours.bind(key_codes.EKeySelect, self.select_hours)
		appuifw.app.body = self.list_box_hours
		appuifw.app.exit_key_handler = self.back

	def select_hours(self):
		res_hours = self.list_box_hours.current()
		if res_hours == 0:
			self.insert()
		elif res_hours == 1:
			appuifw.note(u"Be done!")
		elif res_hours == 2:
			appuifw.note(u"Be done!")
		elif res_hours == 3:
			self.back()

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
		return strftime("%d/%m/%Y", time.localtime(self._iForm[0][2]))

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
		old_title = appuifw.app.title
		appuifw.app.title = u"Add Hours"
		self.setActive()
		if self.isSaved():
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

			# scrivo nel db
			# mydb.query("create table benzina (id counter, data date, prezzolitro float, euro float, pagato text, achi text, km float, altra text)")
			# directory = "e:\\Python\\src\\"
			# dbname = "report"
			# mydb = db(directory+dbname+'.db')
			# self.mydb.query("insert into Progetti (progetto, importo,durata) VALUES ('%s',%f,%d)" % (nome,importo,0))
			# mydb.query("insert into benzina (data, prezzolitro , euro , pagato , achi , km , altra) values('%s','%f','%f','%s','%s','%f','%s')" % (date, prezzolitro, euro, pagato, aChi, km, altra))
			appuifw.note(u"Save to database. Be done","info")
		appuifw.app.title = old_title
