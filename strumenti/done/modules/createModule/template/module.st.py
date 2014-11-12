from strumenti.done.lib.module import Field
from strumenti.done.lib.types import *

class ${module_name[0].upper() + module_name[1:]}Module( ):
  <% 
    n_page = len( pages )
    page_name, fields = pages.pop()  
  %>
  % while n_page:
  def ${page_name.replace(' ','_')}( self, values ):

    # TODO
    # Do something related to ${page_name} here

    fields = [ 
        % for field in fields:
          Field( '${field['name']}', ${field['value']} ), 
        % endfor
             ]


    % if n_page > 1:
    return ( '${page_name.replace('_',' ')}', <%  page_name, fields = pages.pop()  %>
       self.${page_name.replace(' ','_')} , fields )
    % else:
    return ( '${page_name.replace(' ','_')}', None, 'Finish' )
    % endif


    <% n_page-=1 %>

  % endwhile


