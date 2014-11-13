from strumenti.done.libs.types import *
from strumenti.done.libs.module import fill_values, Field


class WorkModule():

  ## values
  values = {}

  def run( self, values = None ):
    fields = [ 
               Field( 'cliente', [ 'Parella', 'CUB' ] ),
               Field( 'su_chiamata', False ),
               Field( 'data_intervento', date.today() ) 
             ]

    return ( 'Creazione report intervento', self.chiedi_luogo_se_a_chiamata, fields )


  @fill_values
  def chiedi_luogo_se_a_chiamata( self, values ):

    if values['su_chiamata'] == True:
      return self.create_mail_template( values )

    luogo_intervento = { 'Parella': [ 'Marsigli',   #'il dormitorio in Via Marsigli 12',
                                      'Ghiacciaie', #'il dormitorio in strada delle Ghiacciaie 52/b',
                                      'Tazzoli',    #'il dormitorio Tazzoli, in via Tazzoli 76',
                                      'Sede' ] ,       #'la Cooperativa Parella in via Bellardi 76' ],
                         'CUB'    : [ 'Marconi' ] } #'la CUB Torino in Corso Marconi 34 (Torino)' ] }

    fields = [ Field( 'luogo_intervento', luogo_intervento[ values['cliente'] ] ),
               Field( 'data_chiamata', date.today() )  ]

    return ( 'Luogo intervento',
             self.create_mail_template,
             fields )



  @fill_values
  def create_mail_template( self, values ):

    from os.path import dirname, join

    #modify email template
    from strumenti.libs import template
    from strumenti.libs import log
    from os.path import join, dirname

    luogo_intervento = { 'Marsigli' : 'il dormitorio in Via Marsigli 12',
                         'Ghiacciaie': 'il dormitorio in strada delle Ghiacciaie 52/b',
                         'Tazzoli': 'il dormitorio Tazzoli, in via Tazzoli 76',
                         'Sede': 'la Cooperativa Parella in via Bellardi 76' ,
                         'Marconi': 'la CUB Torino in Corso Marconi 34 (Torino)' }

    log.debug( values )
    values['luogo_intervento_tmpl'] = luogo_intervento[ values['luogo_intervento'] ]
    values['data_intervento'] = values['data_intervento'].strftime( '%d/%m/%Y' )

    template_path = join( dirname( __file__ ), 'templates' )
    mail_template = template.run( join( template_path, 'diciannove.tmpl' ), values )

    #mail_a = { 'Parella': 'parella@parella.org',
    #           'CUB': 's.pironti@cubpiemonte.org' }

    mail_a = { 'Parella': 'lesion@autistici.org',
               'CUB': 'rocco.depatto@mailbox19.net' }


    fields = [
               Field( 'oggetto', 'Report intervento %s' % values['data_intervento'] ),
               Field( 'da', [ 'lesion@autistici.org', 'rocco.depatto@mailbox19.net' ] ),
               Field( 'a',  mail_a[values['cliente']] ),
               Field( 'mail', mail_template, 'long' ),
             ]


    return( 'Conferma mail', self.attach_report, fields )


  @fill_values
  def attach_report( self, values ):

    from os import environ

    referente = { 'Parella': 'Monica Pecchio',
                  'CUB': 'Stefania Pironti' }


    fields = [
               Field( 'referente', referente[values['cliente']] ),
               Field( 'ora_inizio', time( 10, 00 ) ),
               Field( 'ora_fine', time( 11, 00 ) ),
               Field( 'report', '', 'long' ),
               Field( 'salva_report', '%s/work/report-%s-%s.pdf' % ( environ['HOME'],
                                                                     values['cliente'],
                                                                     values['data_intervento'].strftime( '%d%h%y' ) ) ),
               Field( 'consulente', 'Rocco De Patto' )
             ]


    return ( 'Allega report intervento', self.send, fields )



  @fill_values
  def send( self, values ):
    from os.path import join, dirname


    #modify open office report
    from strumenti.libs import oo
    from datetime import datetime

    luogo_intervento = { 'Marsigli' : 'Via Marsigli 12',
                         'Ghiacciaie': 'Strada delle Ghiacciaie 52/b',
                         'Tazzoli': 'via Tazzoli 76',
                         'Sede': 'Cooperativa Parella, via Bellardi 76' ,
                         'Marconi': 'Corso Marconi 34' }

    values['luogo_intervento'] = luogo_intervento[ values['luogo_intervento'] ]

    values['durata'] = ( values['ora_fine'] - values['ora_inizio'] ).strftime( "%H:%M ore" )
    values['ora_inizio'] = values['ora_inizio'].strftime( '%H:%M' )
    values['ora_fine'] = values['ora_fine'].strftime( '%H:%M' )

    values['data_intervento'] = values['data_intervento'].strftime( '%d/%m/%Y' )
    values['data_chiamata'] = values['data_chiamata'].strftime( '%d/%m/%Y' )

    template_path = join( dirname( __file__ ), 'templates' )
    oo.fill_doc_fields( join( template_path, 'diciannove.odt' ),  values, values['salva_report'] )

    #send email
    from strumenti.libs.mail import send_mail
    ret = send_mail( values['da'],[ values['da'], values['a'] ], values['oggetto'], values['mail'], [values['salva_report']] )

    #add report in dotproject
    #url_dotproject = { 'Parella' : 281,
    #                   'Dermes'  : 

    return( "Fine", None, "REPORT: <a href='file://%s'>report</a><br/>MAIL: %s\n" % ( values['salva_report'], ret ) )

