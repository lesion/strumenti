from mechanize import ParseResponse, urlopen
from scrapemark import scrape


def get_form( url ):
  response = urlopen( url )
  forms = ParseResponse(response, backwards_compat=False)
  return forms[0]

def submit( form, values, submit ):

  for key, value in values.iteritems():
    if type(form[key]) == list:
      form[key]= [ value ]
    else:
      form[key] = value

  return form.click( submit )



def parse( url, parser, next_page=None ):
  html = urlopen( url ).read()
  return scrape( parser, html) 








