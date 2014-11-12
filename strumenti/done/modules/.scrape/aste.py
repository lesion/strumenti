# vim: set fileencoding=utf-8:

def get():

  options = {}

  options['url'] = 'http://www.astegiudiziarie.it'
  options['submit'] = 'ctl00$ContentPlaceHolder1$Mascherericerche1$ImmobiliareGenerale1$btnCerca'
  options['next_page'] = 'ctl00$ContentPlaceHolder1$Primasel2_1$dlstPrimasel$ctl10$btnSuccessiva'
  options['parser'] = """
          <table>
          {* 
            <td headers="record{{}}_int{{}}">{{ [case].procedura }}</td>
            <td>{{[case].tribunale}}</td>
            <td>{{[case].tipo}}</td> 
            <td>{{[case].ruolo}}</td> 
            <td>{{}}</td> 
            <td>€{{[case].costo}}</td> 

            <div class="datibene">
            <p><strong>{{[case].vendita}}</strong></p>
            <p>{{[case].lotto}}</p>
            <p><strong>{{[case].comune}} (<abbr title="{{[case].provincia}}"></abbr>)</strong>- {{[case].indirizzo}} - {{[case].cap}}
            <br />{{[case].descrizione}}</p>
            </div>
            <div class="elencoallegati">{{[case].allegati}}</div>
            <a href="{{[case].link}}">SCHEDA DETTAGLIATA{{}}</a>

          
          *}
          </table>
            """

  options['subparser'] = """
                  <td headers="{{}}_Descrizione">{{descrizione}}</td>
                  <td headers="{{}}_dataoraevar"><strong>{{giorno|int}}/{{mese|int}}/{{anno|int}} ore {{ore|int}}.{{minuti|int}}</strong></td>
                  """

  _prefix = 'ctl00$ContentPlaceHolder1$Mascherericerche1$ImmobiliareGenerale1$'
  options['fields'] = { _prefix + 'txtFasciaPrezzoA' : 'Fino a euro', 
             _prefix + 'drpdNRecord' : 'Records', 
             _prefix + 'txtComuneImmobile' : 'Comune', 
             _prefix + 'drpdProvincie' : 'Provincia' }

  return options
  #{ 'url': url, 'submit': submit, 'next_page': next_page, 'parser': parser, 'fields': fields }


def get_resource( casa ):
  from strumenti.lib import scrape
  from os import mkdir, path

  if path.isdir( casa['procedura'] ):
    return

  mkdir( casa['procedura'] )

  type_table = { 'AVVISO': 'AV', 'PERIZIA': 'PE', 
                 'ORDINANZA': 'OR', 'FOTO': 'FO',
                 'PLANIMETRIA': 'PL' }

  for allegato in casa['allegati'].split():
    if not type_table.has_key( allegato ):
      continue

    print "\n\nScarico %s" % allegato
    url = 'http://astegiudiziarie.it/browsedoc.aspx%s&sigla=%s' % ( casa['link'][15:], type_table[allegato] )

    if allegato == 'FOTO' or allegato == 'PLANIMETRIA':
      parser = """<a id="{{}}_HplinkDownloadZip" href="{{zip}}>"""
      link  = scrape.parse( url, parser )['zip']
      print get_zip_resource( casa['procedura'], link )

    else:
      from urllib import urlopen
      fd = urlopen( url )
      f = open( "%s/%s.pdf" % ( casa['procedura'], allegato ), 'w' )
      f.write( fd.read() )
      f.close()
      fd.close()




def get_zip_resource( procedura, link ):
  from urllib import urlopen
  from zipfile import ZipFile

  ## open remote zip
  res = urlopen( link )
  zip = open( '/tmp/tmp.zip', 'w' )
  zip.write( res.read() )
  res.close()
  zip.close()
  zip = ZipFile( "/tmp/tmp.zip" )
  zip.extractall( procedura )
  return zip.namelist()

