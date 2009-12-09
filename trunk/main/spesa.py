import appuifw, time, os, sys, e32db, key_codes, e32
from time import strftime
from string import replace

# view_path = "c:\\data\\Python\\view"
# view_path = "E:\\Python\\view"
# sys.path.append(view_path)

db = e32db.Dbms()
dbv = e32db.Db_view()

class Spesa( object ):
	## The constructor.
	def __init__(self, dbpath):
		self.dbpath = dbpath
		self.sqlpath = "%s.home.sql" % self.dbpath
		self.old_title = appuifw.app.title
		self.old_quit = appuifw.app.exit_key_handler
		self.old_body = appuifw.app.body
		self.old_menu = appuifw.app.menu
		appuifw.app.title = u"Spesa Menu"
		db.open(self.dbpath)
		self.list_spesa = [u"Insert", u"View", u"Export", u"Configure", u"Back"]
		## Bool
		self._iIsSaved = False
		# self.res_fuel = appuifw.selection_list(self.list_fuel)
		self._initialize_spesa()

	def back(self):
		appuifw.app.body = self.old_body
		appuifw.app.menu = self.old_menu
		appuifw.app.exit_key_handler = self.old_quit
		appuifw.app.title = self.old_title
	
	def _initialize_spesa(self):
		appuifw.app.menu = [(u"Select", self.select_spesa), (u"Back", self.back)]
		self.list_box_spesa = appuifw.Listbox(map(lambda x:x, self.list_spesa))
		self.list_box_spesa.bind(key_codes.EKeySelect, self.select_spesa)
		appuifw.app.body = self.list_box_spesa
		appuifw.app.exit_key_handler = self.back

	def select_spesa(self):
		res_spesa = self.list_box_spesa.current()
		if res_spesa == 0:
			self.insert()
		elif res_spesa == 1:
			self.view()
		elif res_spesa == 2:
			self.export()
		elif res_spesa == 3:
			self.configure()
		elif res_spesa == 4:
			self.back()

	def export( self ):#sql_create = db.execute(u"CREATE TABLE spesa (id COUNTER, stato NUMBER, tipo VARCHAR)") 
		sql_string = u"INSERT INTO home (id, date, shop, type, paid, price, another) VALUES (%d, '%s', '%s', '%s', %f, '%s');\n"
		db.open(self.dbpath)
		if os.path.exists(self.sqlpath):
			os.remove(self.sqlpath)
		file = open(self.sqlpath, 'a')
		file.write(unicode("DROP TABLE IF EXISTS home;\nCREATE TABLE IF NOT EXISTS home (id INT, date DOUBLE, shop VARCHAR(255), type VARCHAR(255), paid VARCHAR(255), price FLOAT, another VARCHAR(255), PRIMARY KEY (id));\n"))
		dbv.prepare(db, unicode("SELECT * FROM home"))
		for i in range(1, dbv.count_line()+1):
			dbv.get_line()
			file.write(sql_string % ( dbv.col(1), dbv.col(2), dbv.col(3), dbv.col(4), dbv.col(5), dbv.col(6), dbv.col(7), dbv.col(8) ))
			dbv.next_line()
		file.close()
		db.close()
		appuifw.note(u"Saved in %s" % self.sqlpath, "conf")

	def checkbox(self):
		Lista=[u'Chiama',u'Sms',u'Mms',u'Gioca']
		richiesta = appuifw.multi_selection_list(Lista , style='checkbox', search_field=1)

	def insert(self):
		old_title = appuifw.app.title
		appuifw.app.title = u"Add Spesa Home"
		self.checkbox()
		#sql_string = u"INSERT INTO home (date, shop, type, paid, price, another) VALUES (%d, '%s', '%s', '%s', %f, '%s')" %( date, shop, type, paid, price, another )
		#try:
		#	db.execute(sql_string)
		#except:
			#db.open(self.dbpath)
		#	db.execute(sql_string)
		appuifw.note(u"Saved", "conf")
		db.close()
		appuifw.app.title = old_title

	def view(self):
		pass
		#import viewhome
		#viewhome.View(self.dbpath)
	def configure(self):
		old_title = appuifw.app.title
		appuifw.app.title = u"Add Tipo Spesa"
		tipo=appuifw.query(u"Tipo: ","text")
		zero = 0
		#sql_create = db.execute(u"CREATE TABLE spesa (id COUNTER, stato NUMBER, tipo VARCHAR)")
		sql_string = u"INSERT INTO spesa (stato, tipo) VALUES (%d, '%s')" %(zero, tipo)
		try:
			db.execute(sql_string)
		except:
			db.open(self.dbpath)
			db.execute(sql_string)
		appuifw.note(u"Saved", "conf")
		db.close()
		appuifw.app.title = old_title
