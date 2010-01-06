import appuifw, e32, os, sys, e32db, key_codes

try:
	raise Exception
except Exception:
	fr = sys.exc_info()[2].tb_frame
	fpath = fr.f_code.co_filename
fdir, fname = os.path.split(fpath)
main_path = os.path.join(fdir, 'main')
sys.path.append(main_path)

view_path = os.path.join(fdir, 'view')
sys.path.append(view_path)

# dbpath = unicode(os.path.join(main_path, 'test.db'))
dbpath = u'%stest.db' % os.getcwd()

## Initialize database
db = e32db.Dbms()
try:
	db.open(dbpath)
except:
	db.create(dbpath)
	db.open(dbpath)
try:
	sql_create = db.execute(u"CREATE TABLE fuel (id COUNTER, date FLOAT, priceLiter FLOAT, euro FLOAT, paid VARCHAR, who VARCHAR, km FLOAT, another VARCHAR)")
except: pass # gia creato
try:
	sql_create = db.execute(u"CREATE TABLE hours (id COUNTER, date FLOAT, hourstart FLOAT, hourend FLOAT, lunch FLOAT, km FLOAT, another VARCHAR)")
except: pass # gia creato
try:
	sql_create = db.execute(u"CREATE TABLE cabine (id COUNTER, nome VARCHAR, regione VARCHAR, provincia VARCHAR, indirizzo VARCHAR, note VARCHAR)")
except: pass # gia creato
try:
	sql_create = db.execute(u"CREATE TABLE strumenti (id COUNTER, nome VARCHAR, cabina VARCHAR, note VARCHAR)")
except: pass # gia creato
try:
	sql_create = db.execute(u"CREATE TABLE tickets (id COUNTER, date FLOAT, cabina VARCHAR, strumento VARCHAR, note VARCHAR)")
except: pass # gia creato
try:
	sql_create = db.execute(u"CREATE TABLE buy (id COUNTER, date FLOAT, shop VARCHAR, type VARCHAR, paid VARCHAR, price FLOAT, another VARCHAR)")
except: pass # gia creato
try:
	sql_create = db.execute(u"CREATE TABLE home (id COUNTER, date FLOAT, shop VARCHAR, type VARCHAR, paid VARCHAR, price FLOAT, another VARCHAR)")
except: pass # gia creato
try:
	sql_create = db.execute(u"CREATE TABLE spesa (id COUNTER, stato NUMBER, tipo VARCHAR)")
except:
	pass
db.close()


class _app:
	def __init__(self):
		self.lock = e32.Ao_lock()
		self.list_box = None
		appuifw.app.title = u"Py-Report"
		appuifw.app.screen = "normal"
		appuifw.note(u"Welcome to Py-Report")
		self.lista = [u"Seleziona dal menu'"]
		#self.lista = [u"Hours", u"Tickets", u"Fuel", u"Buy", u"Exit"]
		self._initialize_main_()

	def _initialize_main_(self):
		#appuifw.app.menu = [(u"Select", self.select_menu), (u"Exit", self.exit)]
		appuifw.app.menu = [(u"Lavoro",((u"Hours", self.hours),(u"Tickets", self.tickets), (u"Buy", self.buy))), (u"Casa", ((u"Spesa", self.home), (u"Benzina", self.fuel), (u"Spesa check", self.spesa_check))),(u"Exit", self.exit)]
		self.list_box = appuifw.Listbox(map(lambda x:x, self.lista))
		self.list_box.bind(key_codes.EKeySelect, self.select_menu)
		appuifw.app.body = self.list_box
		appuifw.app.exit_key_handler = self.exit

	def run(self):
		self.lock.wait()
		
	def hours(self):
		import hours
		hours.Hours(dbpath)
	def tickets(self):
		import tickets
		tickets.Tickets(dbpath)
	def buy(self):
		import buy
		buy.Buy(dbpath)
	def home(self):
		import home
		home.Home(dbpath)
	def fuel(self):
		import fuel
		fuel.Fuel(dbpath)
	def spesa_check(self):
		import spesa
		spesa.Spesa(dbpath)
#da eliminare
	def select_menu(self):
		res = self.list_box.current()
		if res == 0:
			import hours
			hours.Hours(dbpath) # Gli passo il percorso del database senza doverlo cambiare in tutti i files
		elif res == 1:
			import tickets
			tickets.Tickets(dbpath)
		elif res == 2:
			import fuel
			fuel.Fuel(dbpath) # Gli passo il percorso del database senza doverlo cambiare in tutti i files
		elif res == 3:
			import buy
			buy.Buy(dbpath)
		elif res == 4:
			self.exit()

	def exit(self):
		appuifw.note(u"Goodbye")
		self.lock.signal()
		# appuifw.app.set_exit()

pyReport = _app()
pyReport.run()
