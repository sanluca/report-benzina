import appuifw, time, os, sys, e32db, key_codes, e32
from time import strftime
from string import replace

# this_path = "c:\\data\\Python\\view"
this_path = "E:\\Python\\view"
sys.path.append(this_path) 

db = e32db.Dbms()
dbv = e32db.Db_view()

class Fuel( object ):
	## The constructor.
	def __init__(self, dbpath):
		self.dbpath = dbpath
		self.old_title = appuifw.app.title
		self.old_quit = appuifw.app.exit_key_handler
		self.old_body = appuifw.app.body
		self.old_menu = appuifw.app.menu
		appuifw.app.title = u"Fuel Menu"
		db.open(self.dbpath)
		self.list_fuel = [u"Insert", u"View", u"Config", u"Back"]
		## Bool
		self._iIsSaved = False
		# self.res_fuel = appuifw.selection_list(self.list_fuel)
		self._initialize_fuel()

	def back(self):
		appuifw.app.body = self.old_body
		appuifw.app.menu = self.old_menu
		appuifw.app.exit_key_handler = self.old_quit
		appuifw.app.title = self.old_title
	
	def _initialize_fuel(self):
		appuifw.app.menu = [(u"Select", self.select_fuel), (u"Back", self.back)]
		self.list_box_fuel = appuifw.Listbox(map(lambda x:x, self.list_fuel))
		self.list_box_fuel.bind(key_codes.EKeySelect, self.select_fuel)
		appuifw.app.body = self.list_box_fuel
		appuifw.app.exit_key_handler = self.back

	def select_fuel(self):
		res_fuel = self.list_box_fuel.current()
		if res_fuel == 0:
			self.insert()
		elif res_fuel == 1:
			self.view()
		elif res_fuel == 2:
			appuifw.note(u"Be done!")
		elif res_fuel == 3:
			self.back()

	def insertForm( self ):
		# list of payment types
		self._payments = [u"Cash", u"Bancomat", u"Credit card", u"Check", u"Payable"]
		# elenco fornitori 
		self._suppliers=[u"Esso", u"Agip", u"Shell", u"Q8", u"IP", u"Erg", u"API", u"Tamoil", u"Total"]
		# creazione Form
		self._iFields = [( u"Date", "date", time.time()),
						 ( u"Price for liter", "float", 0),
						 ( u"Euro", "float", 0),
						 ( u"Paid", "combo", ( self._payments, 0 ) ),
						 ( u"Who", "combo", ( self._suppliers, 0 ) ),
						 ( u"Km", "number"),
						 ( u"Another item", "text")]
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

	def getPriceLiter(self):
		return self._iForm[1][2]

	## ritorna la spesa in euro.
	def getEuro( self ):
		# deve essere un float
		datoStringa = "%s" % self._iForm[2][2]
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
		old_title = appuifw.app.title
		appuifw.app.title = u"Add Fuel"
		self.insertForm()
		if self.isSaved():
			# estraggo i dati che mi servono
			date = self.getDate()
			priceLiter = self.getPriceLiter()
			euro = self.getEuro()
			paid = self.getPaid()
			who = self.getWho()
			km = self.getKm()
			another = self.getAnother()
			sql_string = u"INSERT INTO fuel (date, priceLiter, euro, paid, who, km, another) VALUES ('%s', %f, %f, '%s', '%s', %d, '%s')" %( date, priceLiter, euro, paid, who, km, another )
			try:
				db.execute(sql_string)
			except:
				db.open(self.dbpath)
				db.execute(sql_string)
			appuifw.note(u"Save to database.")
			db.close()
		appuifw.app.title = old_title

	def view(self):
		import viewfuel
		viewfuel.View(self.dbpath)
