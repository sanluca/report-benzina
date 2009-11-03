import appuifw, e32, os, sys, e32db, key_codes

try:
	raise Exception
except Exception:
	fr = sys.exc_info()[2].tb_frame
	fpath = fr.f_code.co_filename
fdir, fname = os.path.split(fpath)
main_path = os.path.join('main', fdir)
sys.path.append(main_path)

view_path = os.path.join('view', fdir)
sys.path.append(view_path)

dbpath = os.path.join(main_path, 'test.db')

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
		sql_create = db.execute(u"CREATE TABLE interventi (id COUNTER, date FLOAT, cabina VARCHAR, strumento VARCHAR, note VARCHAR)")
	except: pass # gia creato
	try:
		sql_create = db.execute(u"CREATE TABLE buy (id COUNTER, date FLOAT, shop VARCHAR, type VARCHAR, paid VARCHAR, price FLOAT, another VARCHAR)")
	except: pass # gia creato
db.close()


class _app:
	def __init__(self):
		self.lock = e32.Ao_lock()
		self.list_box = None
		appuifw.app.title = u"Report Benzina"
		appuifw.app.screen = "normal"
		appuifw.note(u"Welcome to Py-Report")
		self.lista = [u"Hours", u"Cabins", u"Fuel", u"Buy", u"Exit"]
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
			cabins.Cabins(dbpath)
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
