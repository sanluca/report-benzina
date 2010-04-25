import appuifw, e32, os, sys, e32db, key_codes
canvas = appuifw.Canvas()
import graphics
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

dbpath = unicode(os.path.join(main_path, 'test.db'))
#dbpath = unicode(os.path.join('c:\\system', 'report.db'))
# dbpath = u'%stest.db' % os.getcwd()

## Initialize database
db = e32db.Dbms()
try:
	db.open(dbpath)
except:
	db.create(dbpath)
	db.open(dbpath)
try:
	sql_create = db.execute(u"CREATE TABLE fuel (id COUNTER, date FLOAT, auto VARCHAR, priceLiter FLOAT, euro FLOAT, paid VARCHAR, who VARCHAR, km FLOAT, another VARCHAR)")
	#sql_create = db.execute(u"CREATE TABLE config (id COUNTER, auto VARCHAR, rimborso FLOAT)")
except: pass # gia creato
try:
	sql_create = db.execute(u"CREATE TABLE config (id COUNTER, auto VARCHAR, cilindrata FLOAT, rimborso FLOAT)")
	#sql_create = db.execute(u"INSERT INTO config (auto, rimborso) VALUES (auto, rimborso)")
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
		self.lista = [u"Fuel", u"Config", u"About", u"Exit"]
		self._initialize_main_()
		
		#inserisco immagine di sfondo
		appuifw.app.body = c = appuifw.Canvas()
		appuifw.app.directional_pad = False
		w,h = 20,20
		im = graphics.Image.open("e:\\python\\car.jpg")

		# here's prototype
		# blit(im, source=(0,0,w,h), target=(0,0), mask=None, scale=0)
		# here are examples
		c.blit(im)  # put entire image on top-left
		c.blit(im, target=(70,70)) # put it about mid-screen
		c.blit(im, (0,0,w/2,h/2))  # put a quater image on top-left

		# double the image size and put it about mid-screen
		c.blit(im, target=(60,60,100,100), scale=1)


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
			import fuel
			fuel.Fuel(dbpath) # Gli passo il percorso del database senza doverlo cambiare in tutti i files
		elif res == 1:
			import config
			config.Config(dbpath)
		elif res == 2:
			pass
		elif res == 3:
			self.exit()
			
	def exit(self):
		appuifw.note(u"Goodbye")
		self.lock.signal()
		# appuifw.app.set_exit()

pyReport = _app()
pyReport.run()
