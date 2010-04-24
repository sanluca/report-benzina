import appuifw, time, os, sys, e32db, key_codes, e32
from time import strftime
from string import replace

# view_path = "c:\\data\\Python\\view"
# view_path = "E:\\Python\\view"
# sys.path.append(view_path)

db = e32db.Dbms()
dbv = e32db.Db_view()

class Config( object ):
	## The constructor.
	def __init__(self, dbpath):
		self.dbpath = dbpath
		self.sqlpath = "%s.config.sql" % self.dbpath
		self.old_title = appuifw.app.title
		self.old_quit = appuifw.app.exit_key_handler
		self.old_body = appuifw.app.body
		self.old_menu = appuifw.app.menu
		appuifw.app.title = u"Config Menu"
		db.open(self.dbpath)
		self.list_config = [u"Insert", u"View", u"Back"]
		## Bool
		self._iIsSaved = False
		# self.res_fuel = appuifw.selection_list(self.list_fuel)
		self._initialize_config()

	def back(self):
		appuifw.app.body = self.old_body
		appuifw.app.menu = self.old_menu
		appuifw.app.exit_key_handler = self.old_quit
		appuifw.app.title = self.old_title
	
	def _initialize_config(self):
		appuifw.app.menu = [(u"Select", self.select_config), (u"Back", self.back)]
		self.list_box_config = appuifw.Listbox(map(lambda x:x, self.list_config))
		self.list_box_config.bind(key_codes.EKeySelect, self.select_config)
		appuifw.app.body = self.list_box_config
		appuifw.app.exit_key_handler = self.back

	def select_config(self):
		res_config = self.list_box_config.current()
		if res_config == 0:
			self.insert()
		elif res_config == 1:
			self.view()
		elif res_config == 2:
			self.back()

	def export( self ):
		sql_string = u"INSERT INTO config (auto, cilindrata, rimborso) VALUES ('%s', %f, %f);\n"
		db.open(self.dbpath)
		if os.path.exists(self.sqlpath):
			os.remove(self.sqlpath)
		file = open(self.sqlpath, 'a')
		file.write(unicode("DROP TABLE IF EXISTS config;\nCREATE TABLE IF NOT EXISTS fuel (id INT, auto VARCHAR(255),cilindrata FLOAT, rimborso FLOAT, PRIMARY KEY (id));\n"))
		dbv.prepare(db, unicode("SELECT * FROM config"))
		for i in range(1, dbv.count_line()+1):
			dbv.get_line()
			file.write(sql_string % ( dbv.col(2), dbv.col(3), dbv.col(4), dbv.col(5), dbv.col(6), dbv.col(7), dbv.col(8) ))
			dbv.next_line()
		file.close()
		db.close()
		appuifw.note(u"Saved in %s" % self.sqlpath, "conf")
		
		
	def insertForm( self ):
		# list of payment types
		#self._payments = [u"Cash", u"Bancomat", u"Credit card", u"Check", u"Payable", u"Card"]
		# elenco fornitori 
		#self._suppliers=[u"Esso", u"Agip", u"Shell", u"Q8", u"IP", u"Erg", u"API", u"Tamoil", u"Total"]
		# creazione Form
		self._iFields = [( u"Auto", "text"),
						 ( u"Cilindrata", "float", 0.0),
						 ( u"Rimborso", "float", 0.0)]
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

	def getAuto(self):
		# return strftime("%d/%m/%Y", time.localtime(self._iForm[0][2]))
		return self._iForm[0][2]

	def getCilindrata(self):
		return self._iForm[1][2]

	def getRimborso( self ):
		# deve essere un float
		return self._iForm[2][2]


	def insert(self):
		old_title = appuifw.app.title
		appuifw.app.title = u"Add Auto"
		self.insertForm()
		if self.isSaved():
			# estraggo i dati che mi servono
			auto = self.getAuto()
			cilindrata = self.getCilindrata()
			rimborso = self.getRimborso()
			sql_string = u"INSERT INTO config (auto, cilindrata, rimborso) VALUES ('%s', %f, %f)" %( auto, cilindrata, rimborso )
			try:
				db.execute(sql_string)
			except:
				db.open(self.dbpath)
				db.execute(sql_string)
			appuifw.note(u"Saved", "conf")
			db.close()
		appuifw.app.title = old_title

	def view(self):
		import viewconfig
		viewconfig.View(self.dbpath)
