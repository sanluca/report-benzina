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
		appuifw.app.title = u"Config View"
		db.open(self.dbpath)
		# self.list_fuel = []
		self._initialize_config()

	def back(self):
		appuifw.app.body = self.old_body
		appuifw.app.menu = self.old_menu
		appuifw.app.exit_key_handler = self.old_quit
		appuifw.app.title = self.old_title
	
	def _initialize_config(self):
		appuifw.app.menu = [(u"Select", self._select_config), (u"Modify", self.__modify_field), (u"Back", self.back)]
		self.__create_list()
		try:
			self.list_box_config = appuifw.Listbox(map(lambda x:x[1], self.list_config))
		except:
			self.list_empty = []
			self.list_empty.append(u"< Empty >")
			self.list_box_config = appuifw.Listbox(map(lambda x:x, self.list_empty))
		self.list_box_config.bind(key_codes.EKeySelect, self._select_config)
		self.list_box_config.bind(key_codes.EKeyBackspace, self.__delete_field)
		appuifw.app.body = self.list_box_config
		appuifw.app.exit_key_handler = self.back

	def _select_config(self):
		if len(self.list_config) > 0:
			id = self.list_box_config.current()
			self.__get_info(self.list_config[id][0])
			self.__show_form(self.info_selection)
			
	def __show_form(self, lista):
		
		old_title = appuifw.app.title
		appuifw.app.title = u"ID: %s View Config" % lista[0]
		self._iFields = [( u"Auto", "text", lista[1]),
						 ( u"Rimborso", "float", lista[2])]
		                 
		## Mostro il form.
		self._iForm = appuifw.Form(self._iFields, appuifw.FFormDoubleSpaced+appuifw.FFormViewModeOnly)
		self._iForm.execute()
		appuifw.app.title = old_title
		
	def __modify_field(self):
		if len(self.list_config) > 0:
			id = self.list_config[self.list_box_config.current()][0]
			#print "primo id %d" %id
			#self.__get_info(self.list_fuel[id][0])
			self.__get_info(id)
			#self.__get_info_prec(self.list_fuel[id][0])
			#self.__show_form_modify(self.info_selection, self.info_selection_prec,id)
			self.update_modify(self.info_selection)
	
	def show_form_modify(self, lista):
		
		old_title = appuifw.app.title
		appuifw.app.title = u"ID: %s Modify Config" % lista[0]
		self._iFields = [( u"Auto", "text", lista[1]),
						 ( u"Rimborso", "float", lista[2])]

		## Mostro il form.
		self._iIsSaved = False
		self._iForm = appuifw.Form(self._iFields, appuifw.FFormDoubleSpaced+appuifw.FFormEditModeOnly)
		self._iForm.save_hook = self._markSaved
		self._iForm.execute()
		#appuifw.app.title = old_title
		
		
	## save_hook send True if the form has been saved.
	def _markSaved( self, aBool ):
		self._iIsSaved = aBool

	## _iIsSaved getter.
	def isSaved( self ):
		return self._iIsSaved
	
	def update_modify(self, uno,id):
		old_title = appuifw.app.title
		appuifw.app.title = u"Modify Config"
		self.show_form_modify(uno)
		if self.isSaved():
			# estraggo i dati che mi servono
			auto = self.getAuto()
			cilindrata = self.getCilindrata()
			rimborso = self.getRimborso()
			#sql_string = u"UPDATE fuel SET (date, priceLiter, euro, paid, who, km, another) VALUES (%d, %f, %f, '%s', '%s', %d, '%s') WHERE id=%d" %( date, priceLiter, euro, paid, who, km, another, int(id) )
			sql_string = u"UPDATE config SET auto='%s', cilindrata=%f, rimborso=%f WHERE id=%d" %( auto, cilindrata, rimborso, int(id) )
			try:
				db.execute(sql_string)
			except:
				db.open(self.dbpath)
				db.execute(sql_string)
			appuifw.note(u"Update", "conf")
			db.close()
		appuifw.app.title = old_title
		
	## save_hook send True if the form has been saved.
	#def _markSaved( self, aBool ):
		#self._iIsSaved = aBool

	## _iIsSaved getter.
	#def isSaved( self ):
		#return self._iIsSaved
	
	def getAuto(self):
		# return strftime("%d/%m/%Y", time.localtime(self._iForm[0][2]))
		return self._iForm[0][2]
	def getCilindrata(self):
		return self._iForm[1][2]

	def getRimborso(self):
		return self._iForm[2][2]

		
	def __get_info(self, id):
		import globalui
		sql_string = u"SELECT * FROM config WHERE id=%d" % int(id)
		#globalui.global_msg_query( sql_string, u"SQL Debug" )
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
		if not len(self.list_config) > 0:
			return
		id = self.list_config[self.list_box_config.current()][0]
		import globalui
		if globalui.global_query(u"Delete ID: '%s'?" % id):
			sql_string = u"DELETE FROM config WHERE id=%d" % int(id)
			try:
				db.execute(sql_string)
			except:
				db.open(self.dbpath)
				db.execute(sql_string)
			# db.execute(u"ALTER TABLE fuel AUTO_INCREMENT = 1")
			appuifw.note(u"Deleted", "conf")
			db.close()			
		del globalui
		self._initialize_config()
	
	def __create_list(self):
		self.list_config = []
		sql_string = u"SELECT * FROM config"
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
			self.list_config.append((result[0], unicode("[%s]" % (result[1]))))#, ("%s", result[1])))))
			dbv.next_line()
		db.close()
