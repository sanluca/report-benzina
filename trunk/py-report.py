import appuifw, e32, os, sys, e32db
sys.path.append("E:\\Python\\src") 
#from db import db

db=e32db.Dbms()
dbv=e32db.Db_view()
try:
    db.open(u'E:\\Python\\src\\test.db')
except:
    db.create(u'E:\\Python\\src\\test.db')
    db.open(u'E:\\Python\\src\\test.db')

    #to create ur table
    #db.execute(u"create table fuel (id counter, date varchar, priceLiter float, euro float, paid varchar, who varchar, km float, another long varchar)")

class pyreport:
    def __init__(self):
        appuifw.app.title = u'Py-Report'
        appuifw.app.screen='full'
        appuifw.note(u"Welcom to Py-Report", 'info')
        self.true = True
    def run(self):
        while self.true:
            self.refresh()
            self.menu()
            
    def refresh(self):
        self.lista = [u'Hours',u'Cabins',u'Fuel',u'Exit']
        self.res = appuifw.selection_list(self.lista)

    def menu(self):
        if self.res == 0:
            self.hours()
        elif self.res == 1:
            self.cabins()
        elif self.res == 2:
            self.fuel()
        elif self.res == 3:
            self.exit()
    
    def hours(self):
        import hours
        hours.Hours()
    
    def cabins(self):
        import cabins
        cabins.Cabins()
                                                 
    def fuel(self):
    	import fuel
    	fuel.Fuel()
    	
       	
        
    def exit(self):
        appuifw.note(u"Goodbye", 'info')
        appuifw.app.set_exit()
        self.true = False



if __name__ == '__main__':
    pyreport().run()


