

class Field(object):
    """generic representation of strumenti's field"""
    def __init__(self, name, args):
        super(Field, self).__init__()
        self.name = name
        self.args = args

        self.default = None
        if 'default' in args: self.default = args['default'] # set default value if needed

        self.value = None


class IntField(Field):
    """Integer field"""
    def __init__(self, name, args):
        super(IntField, self).__init__( name, args )


    def validate(self):
        """integer validation"""
        print "Dentro validate di IntField del valure di %s = %s" % (self.value, type(self.value))
        try:
            self.value= int(self.value)
        except Exception:
            return False
        return True


class DirField(Field):
    def __init__(self,name,args):
        super(DirField, self).__init__( name, args )

    def validate(self):
        """docstring for validate"""
        print "Inside validate of DirField %s" % self.value       

    def completer(self,text,state):
        """DirField for completer"""
        print "Inside DirField completer %s" % text


class FileField(Field):
    def __init__(self,name,args):
        super(FileField, self).__init__( name, args )

    def validate(self):
        """docstring for validate"""
        return True

    def completer(self,text,state):
        """DirField for completer"""
        print "Inside DirField completer %s" % text



