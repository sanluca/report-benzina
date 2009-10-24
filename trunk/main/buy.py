import appuifw, time, os, sys, e32db, key_codes, e32
from time import strftime
from string import replace

# view_path = "c:\\data\\Python\\view"
# view_path = "E:\\Python\\view"
# sys.path.append(view_path)

db = e32db.Dbms()
dbv = e32db.Db_view()

class Buy( object ):
	## The constructor.
	def __init__(self, dbpath):
		self.dbpath = dbpath
		self.sqlpath = "%s.buy.sql" % self.dbpath
		self.old_title = appuifw.app.title
		self.old_quit = appuifw.app.exit_key_handler
		self.old_body = appuifw.app.body
		self.old_menu = appuifw.app.menu
		appuifw.app.title = u"Buy Menu"
		db.open(self.dbpath)
		self.list_buy = [u"Insert", u"View", u"Export", u"Back"]
		## Bool
		self._iIsSaved = False
		# self.res_fuel = appuifw.selection_list(self.list_fuel)
		self._initialize_buy()

	def back(self):
		appuifw.app.body = self.old_body
		appuifw.app.menu = self.old_menu
		appuifw.app.exit_key_handler = self.old_quit
		appuifw.app.title = self.old_title
	
	def _initialize_buy(self):
		appuifw.app.menu = [(u"Select", self.select_fuel), (u"Back", self.back)]
		self.list_box_buy = appuifw.Listbox(map(lambda x:x, self.list_buy))
		self.list_box_buy.bind(key_codes.EKeySelect, self.select_buy)
		appuifw.app.body = self.list_box_buy
		appuifw.app.exit_key_handler = self.back

	def select_buy(self):
		res_buy = self.list_box_buy.current()
		if res_buy == 0:
			self.insert()
		elif res_buy == 1:
			self.view()
		elif res_buy == 2:
			self.export()
		elif res_buy == 3:
			self.back()

	def export( self ):#INSERT INTO buy (date, shop, type, paid, price, another) VALUES (%d, '%s', '%s', '%s', %f, '%s')" %( date, shop, type, paid, price, another 
		sql_string = u"INSERT INTO buy (id, date, shop, type, paid, price, another) VALUES (%d, '%s', '%s', '%s', %f, '%s');\n"
		db.open(self.dbpath)
		if os.path.exists(self.sqlpath):
			os.remove(self.sqlpath)
		file = open(self.sqlpath, 'a')
		file.write(unicode("DROP TABLE IF EXISTS buy;\nCREATE TABLE IF NOT EXISTS buy (id INT, date DOUBLE, shop VARCHAR(255), type VARCHAR(255), paid VARCHAR(255), price FLOAT, another VARCHAR(255), PRIMARY KEY (id));\n"))
		dbv.prepare(db, unicode("SELECT * FROM buy"))
		for i in range(1, dbv.count_line()+1):
			dbv.get_line()
			file.write(sql_string % ( dbv.col(1), dbv.col(2), dbv.col(3), dbv.col(4), dbv.col(5), dbv.col(6), dbv.col(7), dbv.col(8) ))
			dbv.next_line()
		file.close()
		db.close()
		appuifw.note(u"Saved in %s" % self.sqlpath, "conf")

	def insertForm( self ):
		# list of payment types
		self._payments = [u"Cash", u"Bancomat", u"Credit card", u"Check", u"Payable"]
		# elenco fornitori 
		self._suppliers=[u"Market", u"Despar", u"Coop", u"Visotto", u"Pam"]
		# creazione Form
		self._iFields = [( u"Date", "date", time.time()),
						 ( u"Shop", "combo", (self._suppliers, 0)),
						 ( u"Type", "text"),
						 ( u"Paid", "combo", ( self._payments, 0 ) ),
						 ( u"Price", "float", 0.0),
						 ( u"Another", "text")]
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

	def getShop(self):
		return self._suppliers[self._iForm[1][2][1]].encode( "utf-8" )

	## 
	def getType( self ):
		return self._iForm[2][2]

	## 
	def getPaid( self ):
		return self._payments[self._iForm[3][2][1]].encode( "utf-8" )

	## 
	def getPrice( self ):
		return self._iForm[4][2]
	def getAnother(self):
		return self._iForm[5][2]

	def insert(self):
		old_title = appuifw.app.title
		appuifw.app.title = u"Add Buy"
		self.insertForm()
		if self.isSaved():
			# estraggo i dati che mi servono
			date = self.getDate()
			shop = self.getShop()
			type = self.getType()
			paid = self.getPaid()
			price = self.getPrice()
			another = self.getAnother()
			sql_string = u"INSERT INTO buy (date, shop, type, paid, price, another) VALUES (%d, '%s', '%s', '%s', %f, '%s')" %( date, shop, type, paid, price, another )
			try:
				db.execute(sql_string)
			except:
				db.open(self.dbpath)
				db.execute(sql_string)
			appuifw.note(u"Saved", "conf")
			db.close()
		appuifw.app.title = old_title

	def view(self):
		import viewbuy
		viewbuy.View(self.dbpath)
