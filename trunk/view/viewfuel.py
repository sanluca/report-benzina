import appuifw, time, os, sys, e32db, key_codes, e32
from time import strftime
from string import replace

db = e32db.Dbms()
dbv = e32db.Db_view()

class View( object ):
	## The constructor.
	def __init__(self, dbpath):
		self.dbpath = dbpath
		self.old_title = appuifw.app.title
		self.old_quit = appuifw.app.exit_key_handler
		self.old_body = appuifw.app.body
		self.old_menu = appuifw.app.menu
		appuifw.app.title = u"Fuel View"
		db.open(self.dbpath)
		self.list_fuel = []
		## Bool
		# self._iIsSaved = False
		self._initialize_fuel()

	def back(self):
		appuifw.app.body = self.old_body
		appuifw.app.menu = self.old_menu
		appuifw.app.exit_key_handler = self.old_quit
		appuifw.app.title = self.old_title
	
	def _initialize_fuel(self):
		appuifw.app.menu = [(u"Select", self._select_fuel), (u"Back", self.back)]
		self.__create_list()
		self.list_box_fuel = appuifw.Listbox(map(lambda x:x[1], self.list_fuel))
		self.list_box_fuel.bind(key_codes.EKeySelect, self._select_fuel)
		appuifw.app.body = self.list_box_fuel
		appuifw.app.exit_key_handler = self.back

	def _select_fuel(self):
		id = self.list_box_fuel.current()
		# appuifw.note(u"ID: %s\nData: %s" % (self.list_fuel[id][0], self.list_fuel[id][1]) )
		self.__get_info(self.list_fuel[id][0])
		self.__show_form(self.info_selection)

	def __show_form(self, lista):
		old_title = appuifw.app.title
		appuifw.app.title = u"Add Fuel"
		self._iFields = [( u"Date", "text", lista[1]),
						 ( u"Price for liter", "float", lista[2]),
						 ( u"Euro", "float", lista[3]),
						 ( u"Paid", "text", lista[4] ),
						 ( u"Who", "text", lista[5] ),
						 ( u"Km", "number", lista[6] ),
						 ( u"Another item", "text", lista[7])]
		## Mostro il form.
		self._iForm = appuifw.Form(self._iFields, appuifw.FFormDoubleSpaced+appuifw.FFormViewModeOnly)
		self._iForm.execute()
		appuifw.app.title = old_title

	def __get_info(self, id):
		import globalui
		sql_string = u"SELECT * FROM fuel WHERE id=%d" % int(id)
		globalui.global_msg_query( sql_string, u"SQL" )
		self.info_selection = []
		try: 
			dbv.prepare(db, sql_string)
		except:
			db.open(self.dbpath)
			dbv.prepare(db, sql_string)
		dbv.get_line()
		for l in range(1, dbv.col_count()+1):
			try:
				self.info_selection.append(dbv.col(l))
			except Exception, err:
				globalui.global_msg_query( unicode(err), u"error" )
		db.close()
	def __create_list(self):
		sql_string = u"SELECT * FROM fuel ORDER BY date DESC"
		try: 
			dbv.prepare(db, sql_string)
		except:
			db.open(self.dbpath)
			dbv.prepare(db,sql_string)
		for i in range(1,dbv.count_line()+1):
			dbv.get_line()
			result = []
			for l in range(1,dbv.col_count()+1):
				try:
					result.append( dbv.col(l) )
				except:
					result.append(None)
			self.list_fuel.append((result[0],result[1]))
			dbv.next_line()
		db.close()
