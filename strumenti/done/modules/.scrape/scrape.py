from strumenti.done.lib.types import *
from strumenti.done.lib.module import fill_values, Field

from strumenti.lib import scrape
from strumenti.lib.db import MySQL

import aste

class ScrapeModule():

  ## values
  values = {}
  selects = {}

  ## create the db
  conn = MySQL( password='a' )
  #conn.create_db( 'case' )
  conn.select_db( 'test' )

  conn.create_table( 'case', ( 
                      'procedura VARCHAR(10) PRIMARY KEY',
                      'ruolo VARCHAR(10) UNIQUE',
                      'lotto VARCHAR(100)',
                      'tipo VARCHAR(40)',
                      'comune VARCHAR(30)',
                      'provincia VARCHAR(30)',
                      'indirizzo VARCHAR(60)',
                      'tribunale VARCHAR(60)',
                      'cap INT',
                      'latitudine DOUBLE',
                      'longitudine DOUBLE',
                      'base INT',
                      'link VARCHAR(100)',
                      'vendita ENUM( "CON INCANTO", "SENZA INCANTO" )',
                      'descrizione TEXT',
                      'allegati SET( "AVVISO", "FOTO", "PERIZIA", "PLANIMETRIA" )',
                      'status ENUM( "FIRST", "SECOND" ) DEFAULT "FIRST"', #i campi sopra vengono riempiti al primo giro
                      'data DATETIME',
                      'aumenti INT',
                      'libera BOOL',
                      'affittata BOOL',
                      'affitto_mensile INT',
                      'regolare BOOL',
                      'spese INT',
                      'tags VARCHAR(50)',
                      'note TEXT' ), True )

  conn.create_table( 'allegati', ( 
                   'procedura VARCHAR(10) UNIQUE',
                   'tipo ENUM("AVVISO","FOTO","PERIZIA", "PLANIMETRIA")',
                   'file VARCHAR(100)' ), True )


  def _get_field( self, control ):

    pretty_name = self.options['fields'][control.name]

    if control.type == 'text':
      value = ''
    elif control.type == 'select':
      self.selects[pretty_name] = {}
      items = []
      for item in control.items:
        self.selects[pretty_name][item.attrs['label']] = item.name
        items.append( item.attrs['label'] )
      value = items

    return Field( pretty_name, value )



  def run( self, values=None):

    self.options = aste.get()
    self.form = scrape.get_form( self.options['url'] )

    fields = []

    for field in self.options['fields'].keys():

      control = self.form.find_control( field )
      fields.append( self._get_field( control ) )

    return ( 'Cerca case',  self.fill_db, fields )



  def fill_db( self, values ):
    from os import mkdir

    forms = {}

    for field, pretty_name in self.options['fields'].iteritems():
      if values.has_key( pretty_name ):
        if self.selects.has_key( pretty_name ):
          forms[field] = self.selects[pretty_name][values[pretty_name]]
        else:
          forms[field] = values[pretty_name]
    
    url = scrape.submit( self.form, forms, self.options['submit'] )
    self.case = scrape.parse( url, self.options['parser'], self.options['next_page'] )

    ## parse in deep
    for tmp_casa in self.case['case']:
      casa = scrape.parse( "%s/%s" % ( self.options['url'], tmp_casa['link'] ), self.options['subparser'] )
      print tmp_casa['link']
      print tmp_casa['procedura']

      ## download resources
      print aste.get_resource( tmp_casa )


      
      self.add_case( self.case['case'] )

    return ( 'Fine', None, "Inserite %d case" % len( self.case['case'] ) )


  def add_case( self, case ):
    from googlemaps import GoogleMaps
    from time import sleep

    gmaps = GoogleMaps()

    for casa in case:
      casa['cap'] = int( casa['cap'] )
      sleep( 0.2 ) 
      print "Calcolo latitudine/longitudine"

      ( casa['latitudine'], 
        casa['longitudine'] ) = gmaps.address_to_latlng( "%s %d, %s, %s" % ( 
                                                          casa['indirizzo'], casa['cap'], 
                                                          casa['comune'], casa['provincia'] ) ) 
                                                      

      casa['allegati'] = casa['allegati'].replace(' ',',')

      casa['tipo'] = casa['vendita'].upper()
      del( casa['vendita'] )

      casa['base'] = int( casa['costo'].replace('.','').split(',')[0] )
      del( casa['costo'] )

      self.conn.insert( 'case', casa )
      print
      

