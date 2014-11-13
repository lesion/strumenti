#!/usr/bin/env python
"""
  strumenti library to manage HTTP stuff
  @author lesion@autistici.org
  @version $Id: http.py 12 2010-12-14 16:23:52Z lesion $

  @example

  from strumenti.lib import http

"""

import httplib
import urllib
import urllib2

class HTTP():

  def __init__( self ):
    handler = VerifiedHTTPSHandler()
    opener = urllib2.install_opener(handler)
    self.connection = urllib2.urlopen( urllib2.Request( 'https://www7.autistici.org' ) )


    



class VerifiedHTTPSConnection(httplib.HTTPSConnection):
  def connect(self):
    # overrides the version in httplib so that we do
    #    certificate verification
    sock = socket.create_connection((self.host, self.port),
                                    self.timeout)
    if self._tunnel_host:
      self.sock = sock
      self._tunnel()

    # wrap the socket using verification with the root
    # certs in trusted_root_certs
    print self.key_file
    self.sock = ssl.wrap_socket(sock,
                                self.key_file,
                                self.cert_file,
                                cert_reqs=ssl.CERT_REQUIRED,
                                ca_certs="trusted_root_cets")


# wraps https connections with ssl certificate verification
class VerifiedHTTPSHandler(urllib2.HTTPSHandler):
  def __init__(self, connection_class = VerifiedHTTPSConnection):
    self.specialized_conn_class = connection_class
    urllib2.HTTPSHandler.__init__(self)

  def open(self, url, data=None , timeout=100 ):
    self.timeout = timeout
    return self.do_open(self.specialized_conn_class, url)









