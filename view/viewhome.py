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
		appuifw.app.title = u"Buy Home View"
		db.open(self.dbpath)
		# self.list_fuel = []
		self._initialize_home()

	def back(self):
		appuifw.app.body = self.old_body
		appuifw.app.menu = self.old_menu
		appuifw.app.exit_key_handler = self.old_quit
		appuifw.app.title = self.old_title
	
	def _initialize_home(self):
		appuifw.app.menu = [(u"Select", self._select_home), (u"Delete", self.__delete_field), (u"Back", self.back)]
		self.__create_list()
		try:
			self.list_box_home = appuifw.Listbox(map(lambda x:x[1], self.list_home))
		except:
			self.list_empty = []
			self.list_empty.append(u"< Empty >")
			self.list_box_home = appuifw.Listbox(map(lambda x:x, self.list_empty))
		self.list_box_home.bind(key_codes.EKeySelect, self._select_home)
		self.list_box_home.bind(key_codes.EKeyBackspace, self.__delete_field)
		appuifw.app.body = self.list_box_home
		appuifw.app.exit_key_handler = self.back

	def _select_home(self):
		if len(self.list_home) > 0:
			id = self.list_box_home.current()
			self.__get_info(self.list_home[id][0])
			self.__show_form(self.info_selection)

	def __show_form(self, lista):
		old_title = appuifw.app.title
		appuifw.app.title = u"ID: %s Buy Home" % lista[0]
		self._iFields = [( u"Date", "date", lista[1]),
						 ( u"Shop", "text", lista[2]),
						 ( u"Type", "text", lista[3]),
						 ( u"Paid", "text", lista[4] ),
						 ( u"Price", "number", lista[5] ),
						 ( u"Another item", "text", lista[6])]
		                 
		## Mostro il form.
		self._iForm = appuifw.Form(self._iFields, appuifw.FFormDoubleSpaced+appuifw.FFormViewModeOnly)
		self._iForm.execute()
		appuifw.app.title = old_title

	def __get_info(self, id):
		import globalui
		sql_string = u"SELECT * FROM home WHERE id=%d" % int(id)
		globalui.global_msg_query( sql_string, u"SQL Debug" )
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
		del globalui

	def __delete_field(self):
		if not len(self.list_home) > 0:
			return
		id = self.list_home[self.list_box_home.current()][0]
		import globalui
		if globalui.global_query(u"Delete ID: '%s'?" % id):
			sql_string = u"DELETE FROM home WHERE id=%d" % int(id)
			try:
				db.execute(sql_string)
			except:
				db.open(self.dbpath)
				db.execute(sql_string)
			# db.execute(u"ALTER TABLE fuel AUTO_INCREMENT = 1")
			appuifw.note(u"Deleted", "conf")
			db.close()			
		del globalui
		self._initialize_home()
	
	def __create_list(self):
		self.list_home = []
		sql_string = u"SELECT * FROM home ORDER BY date DESC"
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
					result.append(dbv.col(l))
				except:
					result.append(None)
			# self.list_fuel.append((result[0], unicode(strftime("%d/%m/%Y", time.localtime(result[1])))))
			self.list_home.append((result[0], unicode("[%s] %s" % (result[0], strftime("%d/%m/%Y", time.localtime(result[1]))))))
			dbv.next_line()
		db.close()
