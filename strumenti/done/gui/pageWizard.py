from PyQt4.QtGui import QWizard, QWizardPage, QGridLayout, QLabel
from strumenti.done.gui.fields import Field
from strumenti.lib import log

class Page( QWizardPage ):
  """ Page construct a wizard page with specified title and fields """

  def __init__( self, wizard, title, fields ):

    ## construct a new QWizardPage
    QWizardPage.__init__( self, wizard )
    self.wizard = wizard

    ## this will store widgets created from fields
    self.widgets = {}

    self.setTitle( title )

    layout = QGridLayout( self )
    self.setLayout( layout )

    ## create and add widget for each field at this page
    ## for each field we add a label with it's name and the widget 
    ## describing the field
    ## @sa Field
    i = 0
    for field in fields:
      item = Field( self, field.name, field.value, field.extra )
      self.widgets[field.name] = item
      self.widgets[field.name].id = i

      if not callable( field.value ):
        label = QLabel( field.name.replace( '_', ' ' ) )
        layout.addWidget( label, i , 0 )

      layout.addWidget( self.widgets[field.name].widget, i, 1 )
      i+=1
    

  def validatePage( self ):
    """
    Used to fill wizard.fields dict based on each field value.
    that dict will be passed as argument to next_call
    @todo validate field value
    """
    self.wizard.validated = True

    for field_name, field in self.widgets.iteritems():
      self.wizard.fields[field_name] = field.get_value()
    return True

