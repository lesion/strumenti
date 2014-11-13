
import pynotify

def show( title, message, icon='dialog-warning', timeout=2, urgency=pynotify.URGENCY_NORMAL, action=None ):

    pynotify.init( 'Done 1.0' )
    notification = pynotify.Notification( title, message, icon )
    notification.set_urgency( urgency )
    notification.set_timeout( timeout )
    if action:
      notification.add_action( 'clicked', 'click', action, None )
    notification.show()


