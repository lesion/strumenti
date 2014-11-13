from datetime import date, time

class time( time ):
  """
  @todo antani
  """

  def __str__( self ):
    return self.strftime( "%H:%M" )

  def __sub__( self, b ):
    a_minutes = self.minute + self.hour*60
    b_minutes = b.minute + b.hour*60
    diff_minute = abs( a_minutes-b_minutes )
    return time( diff_minute/60, diff_minute%60 )



class event( ):
  pass

class action( ):
  pass

