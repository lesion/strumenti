from strumenti.done.libs.types import *
from strumenti.done.libs.module import fill_values, Field


class CreateScraperModule():

  ## values
  values = {}

  def run( self, values = None ):
    fields = [ 
               Field( 'Website', '' ) 
             ]

    return ( 'Choose a website', self.choose_fields, fields )


  @fill_values
  def choose_fields( self, values ):
    from strumenti.libs import scrape
    form = scrape.get_form( values['Website'] )

    fields = []
    submits = []
    for item in form.controls:
      print item.type
      print item.name
      if item.type == 'checkbox':
        fields.append( Field( 'checkbox_' + item.name, True ) )
      if item.type == 'text':
        fields.append( Field( 'input_' + item.name, True ) )
      if item.type == 'select':
        fields.append( Field( item.name, True ) )
        options = []
        for option in item.items:
          options.append( option.attrs['label'] ) 
        fields.append( Field( 'value preview ' + item.name, options ))

      if item.type == 'submit':
        submits.append(  item.attrs['value'] )

      # print item
      #print item.type
      #print dir( item )
      #print type( item )

    fields.append( Field( 'Submit', submits ) )
    return ( 'Select fields', self.choose_fields, fields )



