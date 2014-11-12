from PyQt4.QtGui import *
from PyQt4.QtCore import *
from strumenti.done import version_name
from strumenti.lib import log
from pageWizard import Page


log.setLoggerLevel( 'debug' )

class MainWindow( QWizard ):
  """ Main window for strumenti.done GUI,
  this is a complete dynamic wizard,
  we don't know here how many pages will
  serve or what kind of pages """


  ## needed because nextId is called twice (we need to catch only the last)
  validated = False

  ## this is a callback to the next function 
  ## we use to fill up the next page
  next_call = None

  ## the module we loaded
  module_name = ''

  ## called queue
  call_queue = []
  
  ## fields
  fields = {}

  ## current page id
  last_id = 0

  def __init__( self ):

    QWizard.__init__( self )
    self.setOptions( QWizard.NoBackButtonOnStartPage )
    self.setWindowTitle( version_name )
    self.connect( self, SIGNAL( "currentIdChanged(int)" ), self.currentIdChanged )

    #self.setGeometry( QRect( 10, 10, 200, 200 ) )

    ## the page where user will choose module to load
    self.addPage( ModuleList( self ) )

    self.show()




  def nextId( self ):
    """ Each time 'Next' button is pressed
    this function is called. We create the next or
    last page here calling self.next_call callback to
    retrieve title of next page, the fields and a pointer
    to a new callback (if None this will be the last page  

    @todo implement the Back feature 
    @sa Page"""


    if self.validated == True:

      ## as a convention strumenti.done.modules callback
      ## has to return a tuple with title, the next callback
      ## and a list of fields to fill up this page content

      self.call_queue.append( self.next_call )

      #try:
      ( title, self.next_call, fields ) = self.next_call( self.fields )
      #except Exception, e:
      #  from strumenti.lib import notification
      #  notification.show( "Error", str( e ) ) 
      #  raise e

      
      ## next call to nextId will be ignored
      ## this is because nextId is called twice
      self.validated = False

      ## in case next_call is none LastPage is called
      ## and validated is set to None (returning -1 at next nextId 
      ## call by Qt will show the Finish button in wizard)
      ## http://doc.trolltech.org/4.4/qwizardpage.html#nextId
      if self.next_call==None:
        self.validated = None
        return self.addPage( LastPage( self, title, fields ) )
     
      ## create and add the new page to wizard returning it's ID
      ## this will show it immediately
      return self.addPage( Page( self, title, fields ) )

    ## ignore first call to nextId
    elif self.validated == False:
      return 0

    ## ehi, this is the end
    elif self.validated == None:
      return -1

  def currentIdChanged( self, id ):
    if id < self.last_id:
      self.next_call = self.call_queue.pop()
    else:
      self.last_id = id


class LastPage( QWizardPage ):
  def __init__( self, parent, title, args ):
    QWizardPage.__init__( self, parent )
    self.wizard = parent

    self.setTitle( title )
    self.pageLayout = QVBoxLayout()
    self.setLayout( self.pageLayout )
    self.pageLayout.setContentsMargins( 10,10,10,10 )

    label = QLabel( args )
    label.setOpenExternalLinks( True )
    self.pageLayout.addWidget( label )

  def nextId( self ):
    return -1



class ModuleList( QWizardPage ):
  """ This wizard page will show a list of done.modules
  to choose from and fill "wizard.next_call" properly

  @todo keybindings to each module
  @todo choose module on double click 
  """

  def __init__( self, parent ):

    from strumenti.done.lib import module

    QWizardPage.__init__( self, parent )
    self.wizard = parent

    self.setTitle( "Choose module" )
    self.pageLayout = QVBoxLayout()
    self.setLayout( self.pageLayout )
    self.pageLayout.setContentsMargins( 10,10,10,10 )

    self.moduleList = QListWidget()

    self.modules = module.list_modules()
    
    for nmodule in self.modules:
      self.moduleList.addItem( nmodule )
    
    self.pageLayout.addWidget( self.moduleList, 0 )


  def validatePage( self ):
    """ this event is called when user press 'Next' button.
    we use this to get module choosen and fill up wizard.next_call
    """
    from strumenti.done.lib.module import get_run_callback
    from os.path import dirname

    self.wizard.validated = True
    
    module_name = str( self.moduleList.currentItem().text() )
    self.wizard.next_call = get_run_callback( dirname( self.modules[module_name] ), module_name )

    return True

