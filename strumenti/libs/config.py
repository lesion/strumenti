""" 
  manage configuration

  example usage:
  from strumenti.lib import config

  config.get('done.scrape.case')

"""


from strumenti.lib.db import MySQL
from strumenti.lib import log
from sys import exit

log.setLoggerLevel( 'debug' )

try:
  db = MySQL( password='a' ) 
except Exception, e:
  log.fatal( "Error connecting to config database: %s" % e )
  exit( 1 )

try:
  db.select_db( 'strumenti' )
except Exception, e:
  if e[0] != 1049:
    log.fatal( "Error connecting to config database: %s" % e )
    exit( 1 )

  log.info( "`strumenti` db does not exists, let's create it!" )
  db.create_db( 'strumenti' )
  db.select_db( 'strumenti' )
  log.debug( "Create table config" )
  db.create_table( 'config', 
                   ( 'name VARCHAR(50) NOT NULL PRIMARY KEY',
                     'value TEXT') )


def get( key ):
  """get configuration value of specified key"""
  value = db.query( "SELECT value FROM config WHERE name = '%s' LIMIT 1" % key , fetch='one')[0]
  return value

def set( key, value ):
  db.insert( 'config' , { 'name': key, 'value': value } )



