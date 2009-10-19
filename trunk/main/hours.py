import appuifw, time, os, sys, e32db, key_codes, e32
from time import strftime
from string import replace

# view_path = "c:\\data\\Python\\view"
# view_path = "E:\\Python\\view"
# sys.path.append(view_path)

db = e32db.Dbms()
dbv = e32db.Db_view()

class Hours( object ):
	## The constructor.
	def __init__(self, dbpath):
		self.dbpath = dbpath
		self.sqlpath = "%s.hours.sql" % self.dbpath
		self.old_title = appuifw.app.title
		self.old_quit = appuifw.app.exit_key_handler
		self.old_body = appuifw.app.body
		self.old_menu = appuifw.app.menu
		appuifw.app.title = u"Hours Menu"
		db.open(self.dbpath)
		self.list_hours = [u"Insert", u"View", u"Export", u"Back"]
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
			self.view()
		elif res_hours == 2:
			self.export()
		elif res_hours == 3:
			self.back()

	def export( self ):
		sql_string = u"INSERT INTO hours (id, date, hourstart, hourend, lunch, another) VALUES (%d, %d, %d, %d, %f,'%s');\n"
		db.open(self.dbpath)
		if os.path.exists(self.sqlpath):
			os.remove(self.sqlpath)
		file = open(self.sqlpath, 'a')
		file.write(unicode("DROP TABLE IF EXISTS hours;\nCREATE TABLE IF NOT EXISTS hours (id INT, date DOUBLE, hourstart INT, hourend INT, lunch FLOAT, another VARCHAR(255), PRIMARY KEY (id));\n"))
		dbv.prepare(db, unicode("SELECT * FROM hours"))
		for i in range(1, dbv.count_line()+1):
			dbv.get_line()
			file.write(sql_string % ( dbv.col(1), dbv.col(2), dbv.col(3), dbv.col(4), dbv.col(5), dbv.col(6) ))
			dbv.next_line()
		file.close()
		db.close()
		appuifw.note(u"Saved in %s" % self.sqlpath, "conf")

	def setActive( self ):
		# create Form
		self._iFields = [( u"Date", "date", time.time()),
						 ( u"Start Time", "time", time.time()),
						 ( u"End Time", "time", time.time()),
						 ( u"Lunch (min)", "float", 0.0),
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

	def getStartTime(self):
		return self._iForm[1][2]

	def getEndTime( self ):
		return self._iForm[2][2]

	def getLunch( self ):
		return self._iForm[3][2]

	def getAnother( self ):
		return self._iForm[4][2]

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
			hourstart = self.getStartTime()
			hourend = self.getEndTime()
			lunch = self.getLunch()
			another = self.getAnother()
			sql_string = u"INSERT INTO hours (date, hourstart, hourend, lunch, another) VALUES (%d, %d, %d, %f,'%s')" % ( date, hourstart, hourend, lunch, another )
			try:
				db.execute(sql_string)
			except:
				db.open(self.dbpath)
				db.execute(sql_string)
			appuifw.note(u"Saved", "conf")
			db.close()
		appuifw.app.title = old_title

	def view(self):
		import viewhours
		viewhours.View(self.dbpath)
