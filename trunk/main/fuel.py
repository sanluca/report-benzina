import appuifw, time, os, sys, e32db, key_codes, e32
from time import strftime
from string import replace

# view_path = "c:\\data\\Python\\view"
# view_path = "E:\\Python\\view"
# sys.path.append(view_path)

db = e32db.Dbms()
dbv = e32db.Db_view()

class Fuel( object ):
	## The constructor.
	def __init__(self, dbpath):
		self.dbpath = dbpath
		self.sqlpath = "%s.fuel.sql" % self.dbpath
		self.old_title = appuifw.app.title
		self.old_quit = appuifw.app.exit_key_handler
		self.old_body = appuifw.app.body
		self.old_menu = appuifw.app.menu
		appuifw.app.title = u"Fuel Menu"
		db.open(self.dbpath)
		self.list_fuel = [u"Insert", u"View", u"Export", u"Back"]
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
			self.export()
		elif res_fuel == 3:
			self.back()

	def export( self ):
		sql_string = u"INSERT INTO fuel (date, auto, priceLiter, euro, paid, who, km, another) VALUES (%d, '%s', %f, %f, '%s', '%s', %d, '%s');\n"
		db.open(self.dbpath)
		if os.path.exists(self.sqlpath):
			os.remove(self.sqlpath)
		file = open(self.sqlpath, 'a')
		file.write(unicode("DROP TABLE IF EXISTS fuel;\nCREATE TABLE IF NOT EXISTS fuel (id INT, date DOUBLE, auto VARCHAR(255), priceLiter FLOAT, euro FLOAT, paid VARCHAR(255), who VARCHAR(255), km FLOAT, another VARCHAR(255), PRIMARY KEY (id));\n"))
		dbv.prepare(db, unicode("SELECT * FROM fuel"))
		for i in range(1, dbv.count_line()+1):
			dbv.get_line()
			file.write(sql_string % ( dbv.col(2), dbv.col(3), dbv.col(4), dbv.col(5), dbv.col(6), dbv.col(7), dbv.col(8), dbv.col(9) ))
			dbv.next_line()
		file.close()
		db.close()
		appuifw.note(u"Saved in %s" % self.sqlpath, "conf")
		
	def __getAuto(self):
		self.list_config = []
		self.result = []
		sql_string = u"SELECT * FROM config"
		try: 
			dbv.prepare(db, sql_string)
		except:
			db.open(self.dbpath)
			dbv.prepare(db,sql_string)
		for i in range(1,dbv.count_line()+1):
			dbv.get_line()
			for l in range(1,dbv.col_count()+1):
				try:
					self.result.append(dbv.col(l))
					self.list_config.append(self.result[l][0])
				except:
					self.result.append(None)
			# self.list_fuel.append((result[0], unicode(strftime("%d/%m/%Y", time.localtime(result[1])))))
			# self.list_config.append((result[0], unicode("[%s]" % (result[1]))))#, strftime("%d/%m/%Y", time.localtime(result[1]))))))
			dbv.next_line()
		db.close()
		return self.list_config

	def insertForm( self ):
		# list of payment types
		self._payments = [u"Euroshell", u"Cash", u"Bancomat", u"Credit card", u"Check", u"Payable", u"Card"]
		# elenco fornitori 
		self._suppliers=[u"Esso", u"Agip", u"Shell", u"Q8", u"IP", u"Erg", u"API", u"Tamoil", u"Total"]
		#elenco auto
		#self._auto=__getAuto()
		# creazione Form
		print u'%s' % self.__getAuto()
		self._iFields = [( u"Date", "date", time.time()),
						 ( u"Auto", "combo", (self.__getAuto(), 0) ),
						 ( u"Price for liter", "float", 0.0),
						 ( u"Euro", "float", 0.0),
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
		# return strftime("%d/%m/%Y", time.localtime(self._iForm[0][2]))
		return self._iForm[0][2]

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
			sql_string = u"INSERT INTO fuel (date, auto, priceLiter, euro, paid, who, km, another) VALUES (%d, '%s', %f, %f, '%s', '%s', %d, '%s')" %( date, priceLiter, euro, paid, who, km, another )
			try:
				db.execute(sql_string)
			except:
				db.open(self.dbpath)
				db.execute(sql_string)
			appuifw.note(u"Saved", "conf")
			db.close()
		appuifw.app.title = old_title

	def view(self):
		import viewfuel
		viewfuel.View(self.dbpath)
