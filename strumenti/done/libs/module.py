from os import environ
from os.path import join
from strumenti.done import modules

module_paths = [ join( environ['HOME'], '.done_modules' ),
                 modules.__path__[0] ]

finish = (None,None,None)

def list_modules():

  from os import listdir
  from os.path import isdir, isfile

  module_list = {}

  for module_path in module_paths:
    if not isdir( module_path ): continue

    wannabe_modules = listdir( module_path )
    for wannabe_module in wannabe_modules:
      module_file = join( module_path, wannabe_module, wannabe_module + '.py' )
      if isfile( module_file ):
        module_list[wannabe_module] = module_file
  return module_list


def get_module_args( module_path, module_name ):
  import sys

  ## add path to sys.path if not yet there
  if module_path not in sys.path:
    sys.path.insert( 0, module_path )

  module = __import__( module_name, globals(), locals())
  obj = getattr( module, module_name[0].upper() + module_name[1:] + 'Module' )()
  try:
    return obj.args()
  except Exception, e:
    return None



def get_run_callback( module_path, module_name ):

  import sys

  ## add path to sys.path if not yet there
  if module_path not in sys.path:
    sys.path.insert( 0, module_path )

  module = __import__( module_name, globals(), locals())
  obj = getattr( module, module_name[0].upper() + module_name[1:] + 'Module' )()
  return obj.run




def fill_values( fn ):

  def fill_values_dec( self, values ):

    self.values.update( values )

    return fn( self, self.values )

  return fill_values_dec


"""
  ## type
  ## str (ask user an input value, if extra is long interface should show a bigger widget)
  ## int (ask user an integer, extra could be a dict containing max,min as keys)
  ## []  (ask user to choose from a list of items, if extra if more could select more items)
  ## ()  (ask user a list of item each one with key specified)
  ## strumenti.done.lib.module.date (ask user a date)
  ## strumenti.done.lib.types.time (ask user a time)
  ## strumenti.done.lib.types.event (this is a special field and will be filled by module with a callback)
  ## strumenti.done.lib.types.action (this is a special field and add an option to call a different callback)
"""

class Field():
  def __init__( self, name, value='', default='',mandatory=False, validate=False, extra=None ):
    self.name = name
    self.type = type( value )
    self.value = value
    self.mandatory=mandatory
    self.default=default
    self.extra = extra
    self.validate=validate

  def __str__( self ):
      return "\nField '%s' %s %s mandatory default => '%s']" % ( self.name, self.type,"NOT" if not self.mandatory else '',self.default )


