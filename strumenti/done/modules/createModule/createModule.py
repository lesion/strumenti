from strumenti.done.libs.module import Field, fill_values, module_paths

class CreateModuleModule( ):

  ## values
  values = {}

  def __init__( self ):
    self.n_page = 0
    self.pages = []
    self.module_name = ''


  def run( self, values=None ):
    fields = [ Field( 'module_name',mandatory=True ) ]
    return ( 'Creation of a new module', self.ask_fields, fields )


  @fill_values
  def ask_fields( self, values ):

    print values

    if values.has_key( 'fields' ):
      if values.has_key( 'page_name' ):
        self.pages.append( ( values['page_name'], values['fields'] ) )
      else:
        self.pages.append( ( 'run', values['fields'] ) )
        self.values['page_name'] = 'run'
    else:
      self.module_name = values['module_name']

    fields = [ Field( 'fields', { 'type': [ 'string', 'date', 'time', 'boolean', 'list', 'longstring', 'tuple' ],
                                  'name': '' } ) , 
               Field( 'Finish', self.create_component  ) ]

    if self.n_page>0:
      fields.insert( 0, Field( 'page_name',mandatory=True ) )

    self.n_page += 1
    return ( 'Creation of page %d' % self.n_page, self.ask_fields, fields )


  @fill_values
  def create_component( self, values ):

    translate_type = { 'string': "''",
                       'date': "date.today()",
                       'time': "time(10,00)",
                       'bool': "True",
                       'tuple': "('element1','element2')",
                       'action': "self.function",
                       'list': "['element1','element2']",
                       'longstring': "'', 'long'" }
    
    self.pages.append( ( values['page_name'], values['fields'] ) )

    for page_name, fields in self.pages:
      for field in fields:
        field['value']= translate_type[field['type']]

    print self.pages

    self.pages.reverse()

    args = { 'module_name': self.module_name, 'pages': self.pages } 

    ## create body of module from template and page
    from strumenti.libs import template
    from os.path import join, dirname

    module_path = join( module_paths[1] , values['module_name'] )
    template.run( join( dirname( __file__ ), 'template' ) , args, module_path )
    return ( 'Fine', None, 'Finito<br><a href="file:///%s">Vai al modulo</a>' % module_path )

