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
		# self.list_fuel = []
		self._initialize_fuel()

	def back(self):
		appuifw.app.body = self.old_body
		appuifw.app.menu = self.old_menu
		appuifw.app.exit_key_handler = self.old_quit
		appuifw.app.title = self.old_title
	
	def _initialize_fuel(self):
		appuifw.app.menu = [(u"Select", self._select_fuel), (u"Delete", self.__delete_field), (u"Modify", self.__modify_field), (u"Back", self.back)]
		self.__create_list()
		try:
			self.list_box_fuel = appuifw.Listbox(map(lambda x:x[1], self.list_fuel))
		except:
			self.list_empty = []
			self.list_empty.append(u"< Empty >")
			self.list_box_fuel = appuifw.Listbox(map(lambda x:x, self.list_empty))
		self.list_box_fuel.bind(key_codes.EKeySelect, self._select_fuel)
		self.list_box_fuel.bind(key_codes.EKeyBackspace, self.__delete_field)
		appuifw.app.body = self.list_box_fuel
		appuifw.app.exit_key_handler = self.back

	def _select_fuel(self):
		if len(self.list_fuel) > 0:
			id = self.list_box_fuel.current()
			self.__get_info(self.list_fuel[id][0])
			self.__get_info_prec(self.list_fuel[id][0])
			self.__show_form(self.info_selection, self.info_selection_prec)
			
	def __show_form(self, lista, lista1):
		
		percorsi = lista[6]-lista1[6]
		litri_serbatoio = lista1[3] / lista1[2]
		media_km = percorsi / litri_serbatoio
		
		old_title = appuifw.app.title
		appuifw.app.title = u"ID: %s Fuel" % lista[0]
		self._iFields = [( u"Date", "date", lista[1]),
						 ( u"Price for liter", "float", lista[2]),
						 ( u"Euro", "float", lista[3]),
						 ( u"Paid", "text", lista[4] ),
						 ( u"Who", "text", lista[5] ),
						 ( u"Km", "number", lista[6] ),
						 ( u"Another item", "text", lista[7]),
		                 ( u"Km percorsi", "number", percorsi),
		                 ( u"Litri Serbatoio", "number", litri_serbatoio),
		                 ( u"Media Km", "number", media_km)]
		                 
		## Mostro il form.
		self._iForm = appuifw.Form(self._iFields, appuifw.FFormDoubleSpaced+appuifw.FFormViewModeOnly)
		self._iForm.execute()
		appuifw.app.title = old_title
		
	def __modify_field(self):
		if len(self.list_fuel) > 0:
			id = self.list_box_fuel.current()
			self.__get_info(self.list_fuel[id][0])
			self.__get_info_prec(self.list_fuel[id][0])
			self.__show_form_modify(self.info_selection, self.info_selection_prec,id)
	
	def __show_form_modify(self, lista, lista1, id):
		
		percorsi = lista[6]-lista1[6]
		litri_serbatoio = lista1[3] / lista1[2]
		media_km = percorsi / litri_serbatoio
		
		old_title = appuifw.app.title
		appuifw.app.title = u"ID: %s Fuel" % lista[0]
		self._iFields = [( u"Date", "date", lista[1]),
						 ( u"Price for liter", "float", lista[2]),
						 ( u"Euro", "float", lista[3]),
						 ( u"Paid", "text", lista[4] ),
						 ( u"Who", "text", lista[5] ),
						 ( u"Km", "number", lista[6] ),
						 ( u"Another item", "text", lista[7]),
		                 ( u"Km percorsi", "number", percorsi),
		                 ( u"Litri Serbatoio", "number", litri_serbatoio),
		                 ( u"Media Km", "number", media_km)]

		## Mostro il form.
		self._iIsSaved = False
		self._iForm = appuifw.Form(self._iFields, appuifw.FFormDoubleSpaced+appuifw.FFormEditModeOnly)
		self._iForm.save_hook = self._markSaved
		self._iForm.execute()
		appuifw.app.title = old_title
		
		if self.isSaved():
			# estraggo i dati che mi servono
			date = self.getDate()
			priceLiter = self.getPriceLiter()
			euro = self.getEuro()
			paid = self.getPaid()
			who = self.getWho()
			km = self.getKm()
			another = self.getAnother()
			sql_string = u"UPDATE fuel SET (date, priceLiter, euro, paid, who, km, another) VALUES (%d, %f, %f, '%s', '%s', %d, '%s') WHERE id=%d" %( date, priceLiter, euro, paid, who, km, another, int(id) )
			try:
				db.execute(sql_string)
			except:
				db.open(self.dbpath)
				db.execute(sql_string)
			appuifw.note(u"Saved", "conf")
			db.close()
		appuifw.app.title = old_title
		
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
		return self._iForm[3][2]
		## ritorno chi  stato pagato
	def getWho( self ):
		return self._iForm[4][2][1]

	def getKm( self ):
		return self._iForm[5][2]

	def getAnother( self ):
		return self._iForm[6][2]

	## Return date field value.
	def getDay( self ):
		return strftime("%d/%m/%Y")
		
	def __get_info(self, id):
		import globalui
		sql_string = u"SELECT * FROM fuel WHERE id=%d" % int(id)
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
	
	def __get_info_prec(self, id):
		import globalui
		#prendo i km precedenti
		if id >= 1:
			sql_string = u"SELECT * FROM fuel WHERE id=%d" % int(id-1)
			globalui.global_msg_query( sql_string, u"SQL Debug" )
			self.info_selection_prec = []
		else:
			sql_string = u"SELECT * FROM fuel WHERE id=%d" % int(id)
			globalui.global_msg_query( sql_string, u"SQL Debug" )
			self.info_selection_prec = []

		try: 
			dbv.prepare(db, sql_string)
		except:
			db.open(self.dbpath)
			dbv.prepare(db, sql_string)
		dbv.get_line()
		for l in range(1, dbv.col_count()+1):
			try:
				self.info_selection_prec.append(dbv.col(l))
			except Exception, err:
				globalui.global_msg_query( unicode(err), u"error" )
		db.close()
		del globalui

	def __delete_field(self):
		if not len(self.list_fuel) > 0:
			return
		id = self.list_fuel[self.list_box_fuel.current()][0]
		import globalui
		if globalui.global_query(u"Delete ID: '%s'?" % id):
			sql_string = u"DELETE FROM fuel WHERE id=%d" % int(id)
			try:
				db.execute(sql_string)
			except:
				db.open(self.dbpath)
				db.execute(sql_string)
			# db.execute(u"ALTER TABLE fuel AUTO_INCREMENT = 1")
			appuifw.note(u"Deleted", "conf")
			db.close()			
		del globalui
		self._initialize_fuel()
	
	def __create_list(self):
		self.list_fuel = []
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
					result.append(dbv.col(l))
				except:
					result.append(None)
			# self.list_fuel.append((result[0], unicode(strftime("%d/%m/%Y", time.localtime(result[1])))))
			self.list_fuel.append((result[0], unicode("[%s] %s" % (result[0], strftime("%d/%m/%Y", time.localtime(result[1]))))))
			dbv.next_line()
		db.close()
