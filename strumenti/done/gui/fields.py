from PyQt4.QtGui import *
from PyQt4.QtCore import *

from strumenti.done.lib.types import *


class Field( ):

  def __init__( self, parent, name, value, extra=None ):

    widget = None
    self.type = type( value )
    self.wizard = parent.wizard

    if self.type == bool:
      widget = QCheckBox( name, parent )
      if value:
        widget.setCheckState( Qt.Checked )

    elif self.type == date:
      widget = QCalendarWidget( parent )

    elif self.type == time:
      widget = QTimeEdit( QTime( value.hour, value.minute ), parent )

    elif self.type == tuple:
      widget = QListWidget( parent )
      for item in value:
        widget.addItem( item )

    elif self.type == list:
      if type( value[0] ) == dict:
        widget = QDataGrid( parent, value )
      else:
        widget = QComboBox( parent )
        for item in value:
          widget.addItem( item )
    
    elif self.type == int:
      widget = QSpinBox( parent )

    elif self.type == dict:
      widget = QDict( parent, value )

    elif self.type == str:
      if extra == 'long' :
        widget = QTextEdit( parent )
      else: 
        widget = QLineEdit( parent )

      widget.setText( value )

    ## action
    elif callable( value ):
      widget = QPushButton( name, parent.wizard )
      
      def action_clicked( self, callback ):
        def clicked():
          self.wizard.next_call = callback
          self.wizard.validate = True
          self.wizard.next()

        return clicked

      parent.connect( widget, SIGNAL('clicked()'), action_clicked( self, value) )



    if widget:
      self.widget = widget
    else:
      print "Ehm, piccolo problema"
      print field



  def get_value( self ):
    widget = self.widget
    widget_type = type( widget )

    if widget_type == QCheckBox:
      return widget.isChecked()

    elif widget_type == QComboBox:
      return str( widget.currentText() )

    elif widget_type == QListWidget:
      return str( widget.currentItem().text() )

    elif widget_type == QSpinBox:
      return widget.value()

    elif widget_type == QLineEdit:
      return str( widget.text() )

    elif widget_type == QTextEdit:
      return str( widget.toPlainText() )

    elif widget_type == QTimeEdit:
      selected_time = widget.time()
      return time( selected_time.hour(), selected_time.minute() )

    elif widget_type == QDataGrid:
      return widget.value()

    elif widget_type == QDict:
      return widget.value()

    elif widget_type == QCalendarWidget:
      selected_date =  widget.selectedDate()
      return date( selected_date.year(), 
                   selected_date.month(), 
                   selected_date.day() )



class QDataGrid( QTreeWidget ):
  def __init__( self, parent, values ):
    QTreeWidget.__init__( self, parent )
    self.col_id = values[0].keys().index('id')
    print "Dentro DataGrid e col_id", self.col_id
    self.setColumnCount( len( values[0] ) )
    self.setHeaderLabels( values[0].keys() )
    self.setColumnHidden( self.col_id, True )
    self.setSortingEnabled( True )

    for row in values:
      item = QTreeWidgetItem( self ) 
      i = 0
      for col in row.values():
        item.setText( i, QString(col) )
        i+=1

      self.insertTopLevelItem(0, item )

  def value( self ):
    print "Dentro value di DataGrid"
    val = self.currentItem().text( self.col_id )
    return str(val)



class QDict( QWidget ):

  def __init__( self, parent, values ):

    QWidget.__init__( self, parent )
    self.parent = parent

    self.layout = QGridLayout( self )

    self.values = values
    self.n_field = 0

    ## inizio con le label delle chiavi
    i = 0
    for key in values.keys():
      l = QLabel( key, self )
      self.layout.addWidget( l, 0, i )
      i += 1
  
    i = 0
    self.fields = []
    self.fields.append( {} )
    for key, value in values.items():
      self.fields[0][key] = w = Field( parent, key, value  )
      self.layout.addWidget( w.widget, 1, i )
      i += 1

    self.n_field = 1
    button = QPushButton( QIcon.fromTheme('list-add'), 'Add', self )
    self.layout.addWidget( button, 1, i )
    self.connect( button, SIGNAL( 'clicked()' ), self.add_field )

    self.setLayout( self.layout )

  
  def value( self ):
    values = []
    i = 0
    for field in self.fields:
      values.append( {} )
      for key, field in field.items():
        values[i][key] = field.get_value()
      i+=1

    return values


  def add_field( self ):
    i = 0
    self.fields.append( {} )
    for key, value in self.values.items():
      self.fields[self.n_field][key] = w = Field( self.parent, key, value )
      self.layout.addWidget( w.widget, self.n_field+1, i )
      i += 1

    button = QPushButton( QIcon.fromTheme('list-remove'), 'Remove', self )
    button.id = self.n_field
    self.layout.addWidget( button, self.n_field+1, i )
    button.connect( button, SIGNAL( 'clicked()' ), self.remove_field )
    self.n_field += 1

  def remove_field( self ):
    """
    @todo ehm, how we get the button pressed?
    """
    print type( self )
    print self.id



