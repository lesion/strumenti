
from strumenti.lib import log

def run( template_path, args, destination_path=None, file_match='st' ):
  """ 
  This is a generic template engine using mako as backend
  usefull to manage templated directory.
  Commons template engine do not manage the case of a directory tree
  we want to use as a template and put some files and not another
  or modify just some contents beginning from it. 
  this is why this method.

  @param template_path string, in case this is a file, its content
  is processed with mako, if it's a directory we process all files
  recursively inside it or use .strumenti_template.py:list if found,
  or ones matching the file_match filter regexp. default behaviour
  is to copy all files and compute with mako ones matching *.st.*

  @param args dict, here is stored substitution variables passed
  to mako engine and the list method if found

  @param destination_path string, in case template_path is a directory 
  this parameter is required and computed output is written in this 
  path, elsewhere is returned
  """

  from os.path import isdir
  log.setLoggerLevel( 'debug' )

  if not isdir( template_path ):
    return compute( template_path, args )

  else:
    
    from os.path import  join
    from os import makedirs
    from shutil import copy
    from fnmatch import fnmatch


    if destination_path is None:
      raise Exception( "destination_path parameter has to be set if template_path is a directory" )

    ## create this directory if needed
    if not isdir( destination_path ):
      makedirs( destination_path )

    for item in get_files( template_path, args ):

      if item == 'strumenti_template.py' or item == '.svn':  continue

      if type(item) is tuple:
        ( item_src, item_dst ) = item
      else:
        item_src = item_dst = item

      item_src_path = join( template_path, item_src )
      item_dst_path = join( destination_path, item_dst )

      ## if item is a directory recurse
      if isdir( item_src_path ):
        log.debug( "Directory .. recursing %s" % item_src_path )
        run( item_src_path, args, item_dst_path, file_match )
      else:

        ## check if match file_match
        if fnmatch( item_dst_path, '*.%s.*' % file_match ):
          ## compute this with mako and write to destination_path (removing template extension)
          item_dst_path = join( destination_path, item_dst.replace('.%s.' % file_match,'.') )
          fd = open( item_dst_path,  'w+' )
          fd.write( compute( item_src_path , args ) )
          fd.close()
          log.debug( "Copy %s => %s" % ( item_src_path, item_dst_path ) )

        else:
          ## copy to destination_path
          copy( item_src_path, item_dst_path )
          log.debug( "Copy %s => %s" % ( item_src_path, item_dst_path ) )




def compute( template_path, args ):
  from mako.template import Template
  from mako import exceptions

  tmpl = Template( filename=template_path )
  try:
    return tmpl.render( **args )
  except:
    raise Exception( exceptions.text_error_template().render() )


def get_files(template_path,args=None):
  from os.path import isfile, join, abspath
  from os import chdir, path
  import sys

  if isfile( join(template_path, 'strumenti_template.py' ) ):

    sys.path.insert( 0, abspath( template_path ) )
    log.debug( "Inside %s [%s]" % ( template_path, sys.path[:3] ) )

    strumenti_tpl = __import__( 'strumenti_template', globals(), locals(), [], -1 )
    return strumenti_tpl.run( args )

  else:
    from os import listdir
    return listdir(template_path)


    


