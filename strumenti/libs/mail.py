#!/usr/bin/env python
"""
  usefull lib to send email
"""


def send_mail(send_from, send_to, subject, text, files=[], server="localhost" ):
  """
  Send email
  @param send_from from of message
  @return 
  """
  import smtplib
  import os
  from email.MIMEMultipart import MIMEMultipart
  from email.MIMEBase import MIMEBase
  from email.MIMEText import MIMEText
  from email.Utils import COMMASPACE, formatdate
  from email import Encoders

  assert type(send_to)==list
  assert type(files)==list

  msg = MIMEMultipart()
  msg['From'] = send_from
  msg['To'] = COMMASPACE.join(send_to)
  msg['Date'] = formatdate(localtime=True)
  msg['Subject'] = subject

  msg.attach( MIMEText(text) )

  for f in files:
    part = MIMEBase('application', "octet-stream")
    
    part.set_payload( open(f,"rb").read() )
    Encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
    msg.attach(part)

  try: 
    smtp = smtplib.SMTP(server)
  except Exception, e:
    return False, "Connection error '%s'" % server

  try:
    ret =smtp.sendmail(send_from, send_to, msg.as_string())
  except Exception, e:
    return False, "SMTP Error: %s" % e[0]
  smtp.close()

  return True



if __name__ == '__main__':
  ret = send_mail( 'lesion@autistici.org', 
             [ 'lesion@autistici.org'], 
             '[strumenti] send_mail test', 
             'Test attachments', [ 'lib_email.py' ] )
  print ret
