"""
  @author lesion@autistici.org
  @version $Id$

"""

class OO():
  
  def start(self):
    pass


  def open(self,filename):
    """ open a document """
    pass

  def close(self):
    """ close current instance openoffice """
    pass


from OOoLib import *

def fill_doc_fields( document_path, valorized_fields, save_path , format='pdf' ):

  import os
  import sys
  import uno
  import unohelper

  
  StarDesktop = getDesktop()

  document_path = unohelper.systemPathToFileUrl( os.path.abspath( document_path ) )

  try:
    oDoc = StarDesktop.loadComponentFromURL( document_path , "_blank", 0, Array() ) 
  except Exception, e:
    print "Error loading document from %s" % document_path
    return

  master_fields = oDoc.getTextFieldMasters()
  fields = oDoc.getTextFields()

  master_field_prefix = 'com.sun.star.text.FieldMaster.User.'
  for key, value in valorized_fields.iteritems():
    try:
      master_fields.getByName( master_field_prefix + key ).Content = value
    except:
      print "Error filling field %s" % key

  fields.refresh()

  if format == 'pdf':
    properties = (makePropertyValue( 'FilterName', 'writer_pdf_Export' ),)
  
  url = unohelper.systemPathToFileUrl(os.path.abspath(save_path))
  oDoc.storeToURL(url, properties)
  oDoc.close(1)
  StarDesktop.terminate()


