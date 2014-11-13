

class MySQL( ):
  """ Use this class to connect to MySQL database:
  MySQL( host, user, password ) """


  def __init__( self, host='localhost', user='root', password='' ):
    import MySQLdb
    self.connection = MySQLdb.connect( host, user, password, use_unicode=True, charset='utf8' )
    self.connection.autocommit(True)
    self.cursor = self.connection.cursor()


  def list_db( self ):
    """ return a list of databases """
    self.cursor.execute( 'show databases' )
    databases = ()
    for database in self.cursor.fetchall():
      databases += database
    return databases

  def query( self, query, fetch='all' ):
    self.cursor.execute( query )
    if fetch == 'all':
      return self.cursor.fetchall()
    elif fetch == 'one':
      return self.cursor.fetchone()
  
  def list_acl( self, db=None ):
    pass

  def add_user( self, username, password, db ):
    self.cursor.execute( "GRANT ALL PRIVILEGES ON '%s'.* TO '%s'@%% IDENTIFIED BY '%s' " %
                         ( db, username, password ) )

  def list_fields( self, table ):
    self.cursor.execute( 'DESC %s' % table )
    return self.cursor.fetchall()

  def drop_field( self, table, field ):
    self.cursor.execute( 'ALTER TABLE `%s` DROP COLUMN `%s`' % ( table, field ) )

  def create_db( self, db ):
    self.cursor.execute( 'CREATE DATABASE `%s`' % db )

  def create_table( self, name, fields, drop=False ):
    """ Create a new table

    db.create_table( 'users',
    ( 'id INT NOT NULL AUTO_INCREMENT PRIMARY KEY',
      'username VARCHAR(40) NOT NULL',
      'email VARCHAR(50) NOT NULL',
      'password VARCHAR(40) NOT NULL',
      'status ENUM( "ENABLED", "DISABLED", "WAIT_CONFIRM" ) NOT NULL',
      'confirmation_code VARCHAR(32)',
      'creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
    ), drop=True )

    """

    if drop:
      self.cursor.execute( "DROP TABLE IF EXISTS `%s`" % name )

    query = "CREATE TABLE IF NOT EXISTS `%s` ( %s ) ENGINE = InnoDB " \
            % ( name, ",\n".join( fields ) ) \
            + " DEFAULT CHARACTER SET = utf8 COLLATE = utf8_bin"
    self.cursor.execute( query )


  
  
  def insert( self, table, fields ):
    keys = ', '.join( fields.keys() )
    values = "', '".join( fields.values() )
    self.cursor.execute( "REPLACE INTO `%s` (%s) VALUES ('%s');" % ( table, keys, values ))
      




  def alter_field( self, field, new_field ):
    pass

  def select_db( self, db ):
    self.cursor.execute( 'USE `%s`' % db )

  def list_tables( self ):
    self.cursor.execute( 'SHOW TABLES' )
    tables = ()
    for table in self.cursor.fetchall():
      tables += table
    return tables


  def close( self ):
    self.connection.commit()
    self.connection.close()

  def show_acl( self, db=None ):
    pass



class SQLite(MySQL):

  def __init__( self, db ):
    import sqlite3
    self.connection = sqlite3.connect( db )
    self.cursor = self.connection.cursor()


  def create_table( self, name, fields, drop=False ):
    """ Create a new table

    db.create_table( 'users',
    ( 'id INT NOT NULL AUTO_INCREMENT PRIMARY KEY',
      'username VARCHAR(40) NOT NULL',
      'email VARCHAR(50) NOT NULL',
      'password VARCHAR(40) NOT NULL',
      'status ENUM( "ENABLED", "DISABLED", "WAIT_CONFIRM" ) NOT NULL',
      'confirmation_code VARCHAR(32)',
      'creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
    ), drop=True )

    """

    if drop:
      self.cursor.execute( "DROP TABLE IF EXISTS `%s`" % name )

    query = "CREATE TABLE IF NOT EXISTS '%s' ( %s ) " \
            % ( name, ",\n".join( fields ) ) 
    self.cursor.execute( query )


  def insert( self, table, fields ):

    q = 'REPLACE INTO "%s" ' % table

    q += '(' + ('%s,'*len(fields.keys()))[:-1] % tuple( fields.keys() ) + ')'
    q += ' VALUES ( ' + '?,'*(len(fields)-1) + '?)'

    self.cursor.execute( q, fields.values() )

