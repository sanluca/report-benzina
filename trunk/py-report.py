import appuifw, e32, os, sys, e32db, key_codes

# this_path = "c:\\data\\Python\\main"
this_path = "E:\\Python\\main"
sys.path.append(this_path) 

# this_path = "c:\\data\\Python\\view"
this_path = "E:\\Python\\view"
sys.path.append(this_path) 

dbpath = u"%s\\test.db" % this_path

## Initialize database
db = e32db.Dbms()
try:
	db.open(dbpath)
except:
	db.create(dbpath)
	db.open(dbpath)
	try:
		sql_create = db.execute(u"CREATE TABLE fuel (id COUNTER, date VARCHAR, priceLiter FLOAT, euro FLOAT, paid VARCHAR, who VARCHAR, km FLOAT, another VARCHAR)")
		sql_create = db.execute(u"CREATE TABLE hours (id COUNTER, data VARCHAR, hourstart FLOAT, hourend FLOAT, lunch FLOAT, another VARCHAR)")
	except: pass # gia creato
db.close()


class _app:
	def __init__(self):
		self.lock = e32.Ao_lock()
		self.list_box = None
		appuifw.app.title = u"Report Benzina"
		appuifw.app.screen="normal"
		appuifw.note(u"Welcome to Py-Report")
		self.lista = [u"Hours", u"Cabins", u"Fuel", u"Exit"]
		self._initialize_main_()

	def _initialize_main_(self):
		appuifw.app.menu = [(u"Select", self.select_menu), (u"Exit", self.exit)]
		self.list_box = appuifw.Listbox(map(lambda x:x, self.lista))
		self.list_box.bind(key_codes.EKeySelect, self.select_menu)
		appuifw.app.body = self.list_box
		appuifw.app.exit_key_handler = self.exit

	def run(self):
		self.lock.wait()

	def select_menu(self):
		res = self.list_box.current()
		if res == 0:
			import hours
			hours.Hours(dbpath) # Gli passo il percorso del database senza doverlo cambiare in tutti i files
		elif res == 1:
			import cabins
			cabins.Cabins()
		elif res == 2:
			import fuel
			fuel.Fuel(dbpath) # Gli passo il percorso del database senza doverlo cambiare in tutti i files
		elif res == 3:
			self.exit()

	def exit(self):
		appuifw.note(u"Goodbye")
		self.lock.signal()
		# appuifw.app.set_exit()

pyReport = _app()
pyReport.run()
