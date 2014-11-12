from strumenti.lib import template
from strumenti.done.lib.module import Field, fill_values

#args = { 'user': True, 
#         'db': True, 
#         'db_host': 'localhost',
#         'db_name': 'test',
#         'db_user': 'root',
#         'base_url': 'http://localhost/test/',
#         'encryption_key': 'asdfadsf',
#         'site_name' : 'test',
#         'create_admin': True,
#         'admin_name': 'les',
#         'admin_password': 'les',
#         'admin_email': 'lesion@autistici.org',
#         'use_sessions': True,
#         'db_pass': '' }

class WebSiteModule():
  
  values = { 'encryption_key': 'adsfasf' }

  def run( self, values=None ):
    fields = [ Field( 'site_name' ), Field( 'base_url', 'http://localhost/' ) ]
    return ( 'Creation of a new site', self.want_users, fields )

  @fill_values
  def want_users( self, values ):
    fields = [ Field('want_users', True), Field('create_admin',True) ]
    return ( 'Your new website needs authentication?', self.want_db, fields )


  @fill_values
  def want_db( self, values ):

    #users needs db
    if values['want_users'] or values['create_admin']:
      values['want_db'] = True
      return self.ask_db_data( values )

    fields = [ Field('want_db', True) ]
    return ( 'Your new website needs database?', self.ask_db_data, fields )


  @fill_values
  def ask_db_data( self, values ):
    if not values['want_db']:
      return self.ask_where( values )

    fields = [ Field('db_host', 'localhost'), Field('db_name', values['site_name'] + '_db'),Field('db_user'),Field('db_pass') ]
    return ( 'Please fill database data', self.ask_admin_data, fields )


  @fill_values
  def ask_admin_data( self, values ):
    if not values['create_admin']:
      return self.ask_where( values )

    fields = [ Field('admin_name','admin'), Field('admin_email'), Field('admin_password') ]
    return ( 'Administrator account configuration', self.ask_where, fields )


  @fill_values
  def ask_where( self, values ):
    fields = [ Field( 'dest_path', '/var/www/' + values['site_name'] ) ]
    return ( 'Ok! Where to put your skeleton website?', self.create_website, fields )


  @fill_values
  def create_website( self, values ):
    from os import path
    from strumenti.lib.db import MySQL

    if values['want_db']:
      db = MySQL( values['db_host'], values['db_user'], values['db_pass'] )
      db.create_db( values['db_name'] )
      db.close()

    template_path = path.dirname( path.realpath( __file__ ) )
    template.run( path.join( template_path, 'template/codeigniter' ), values, values['dest_path'] )
    return ( 'Complete!', None, 'Web site creation done!<br><a href="file:///%s">Take a look</a>' % values['dest_path'] )
