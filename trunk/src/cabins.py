#pagina in cui si configura la cabina con il numero degli 
#strumenti al suo interno, selezionando lo strumento all' interno
#della cabina si possono inserire varie manutenzioni o sistemazioni

import appuifw, time, os, sys
from time import strftime
from string import replace

class Cabins( object ):
    
    ## The constructor.
    def __init__( self ):
        self.list_cabins = [u'Insert', u'View', u'Config']
        self.res_cabins = appuifw.selection_list(self.list_cabins)
        
        if self.res_cabins == 0:
            appuifw.note(u"Be done!", 'info')
            
        elif self.res_cabins == 1:
            appuifw.note(u"Be done!", 'info')
          
        elif self.res_cabins == 2:
            appuifw.note(u'Be done!', 'info')
