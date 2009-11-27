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
		appuifw.app.title = u"Hours View"
		db.open(self.dbpath)
		# self.list_hours = []
		self._initialize_hours()

	def back(self):
		appuifw.app.body = self.old_body
		appuifw.app.menu = self.old_menu
		appuifw.app.exit_key_handler = self.old_quit
		appuifw.app.title = self.old_title

	def _initialize_hours(self):
		appuifw.app.menu = [(u"Select", self._select_hours), (u"Delete", self.__delete_field), (u"Modify", self.__modify_field), (u"Back", self.back)]
		self.__create_list()
		try:
			self.list_box_hours = appuifw.Listbox(map(lambda x:x[1], self.list_hours))
		except:
			self.list_empty = []
			self.list_empty.append(u"< Empty >")
			self.list_box_hours = appuifw.Listbox(map(lambda x:x, self.list_empty))
		self.list_box_hours.bind(key_codes.EKeySelect, self._select_hours)
		self.list_box_hours.bind(key_codes.EKeyBackspace, self.__delete_field)
		appuifw.app.body = self.list_box_hours
		appuifw.app.exit_key_handler = self.back

	def _select_hours(self):
		if len(self.list_hours) > 0:
			id = self.list_box_hours.current()
			self.__get_info(self.list_hours[id][0])
			self.__show_form(self.info_selection)

	def __show_form(self, lista):
		old_title = appuifw.app.title
		appuifw.app.title = u"ID: %s Hours" % lista[0]
		self._iFields = [( u"Date", "date", lista[1]),
						 ( u"Start Time", "time", lista[2]),
						 ( u"End Time", "time", lista[3]),
						 ( u"Lunch (min)", "float", lista[4]),
						 ( u"km", "float", lista[5]),
						 ( u"Another item", "text", lista[6])]
		## Mostro il form.
		self._iForm = appuifw.Form(self._iFields, appuifw.FFormDoubleSpaced+appuifw.FFormViewModeOnly)
		self._iForm.execute()
		appuifw.app.title = old_title
		
	def __modify_field(self):
		if len(self.list_hours) > 0:
			id = self.list_hours[self.list_box_hours.current()][0]
			self.__get_info(id)
			self.update_modify(self.info_selection,id)
	
	def show_form_modify(self,lista):
		print lista
		old_title = appuifw.app.title
		appuifw.app.title = u"ID: %s Hours" % lista[0]
		self._iFields = [( u"Date", "date", lista[1]),
						 ( u"Start Time", "time", lista[2]),
						 ( u"End Time", "time", lista[3]),
						 ( u"Lunch (min)", "float", lista[4]),
						 ( u"km", "float", lista[5]),
						 ( u"Another item", "text", lista[6])]

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
	
	def getDate(self):
		# return strftime("%d/%m/%Y", time.localtime(self._iForm[0][2]))
		return self._iForm[0][2]

	def getStartTime(self):
		return self._iForm[1][2]

	def getEndTime( self ):
		return self._iForm[2][2]

	def getLunch( self ):
		return self._iForm[3][2]
	
	def getKm( self ):
		return self._iForm[4][2]

	def getAnother( self ):
		return self._iForm[5][2]

	## Return date field value.
	def getDay( self ):
		return strftime("%d/%m/%Y")
	
	def update_modify(self,lista,id):
		old_title = appuifw.app.title
		appuifw.app.title = u"Modify Hours"
		self.show_form_modify(lista)
		if self.isSaved():
			# estraggo i dati che mi servono
			date = self.getDate()
			hourstart = self.getStartTime()
			hourend = self.getEndTime()
			lunch = self.getLunch()
			km = self.getKm()
			another = self.getAnother()
			#sql_string = u"INSERT INTO hours (date, hourstart, hourend, lunch, km, another) VALUES (%d, %d, %d, %f,%d, '%s')" % ( date, hourstart, hourend, lunch, km, another )
			sql_string = u"UPDATE hours SET date=%d, hourstart=%d, hourend=%d, lunch=%f, km=%d, another='%s' WHERE id=%d" %( date, hourstart, hourend, lunch, km, another, int(id) )
			try:
				db.execute(sql_string)
			except:
				db.open(self.dbpath)
				db.execute(sql_string)
			appuifw.note(u"Update", "conf")
			db.close()
		appuifw.app.title = old_title
	
	

	def __get_info(self, id):
		import globalui
		sql_string = u"SELECT * FROM hours WHERE id=%d" % int(id)
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
		if not len(self.list_hours) > 0:
			return
		id = self.list_hours[self.list_box_hours.current()][0]
		import globalui
		if globalui.global_query(u"Delete ID: '%s'?" % id):
			sql_string = u"DELETE FROM hours WHERE id=%d" % int(id)
			try:
				db.execute(sql_string)
			except:
				db.open(self.dbpath)
				db.execute(sql_string)
			# db.execute(u"ALTER TABLE hours AUTO_INCREMENT = 1")
			appuifw.note(u"Deleted", "conf")
			db.close()			
		del globalui
		self._initialize_hours()
	
	def __create_list(self):
		self.list_hours = []
		sql_string = u"SELECT * FROM hours ORDER BY date DESC"
		try: 
			dbv.prepare(db, sql_string)
		except:
			db.open(self.dbpath)
			dbv.prepare(db, sql_string)
		for i in range(1,dbv.count_line()+1):
			dbv.get_line()
			result = []
			for l in range(1,dbv.col_count()+1):
				try:
					result.append( dbv.col(l) )
				except:
					result.append(None)
			# self.list_hours.append((result[0], unicode(strftime("%d/%m/%Y", time.localtime(result[1])))))
			self.list_hours.append((result[0], unicode("[%s] %s" % (result[0], strftime("%d/%m/%Y", time.localtime(result[1]))))))
			dbv.next_line()
		db.close()
