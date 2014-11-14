from argcomplete.completers import FilesCompleter

class Field(object):
    """generic representation of strumenti's field"""
    def __init__(self, args):
        super(Field, self).__init__()
        self.args = args

        self.default = None
        if 'default' in args.keys(): self.default = args['default'] # set default value if needed

        self.value = None

    def __str__(self):
        return str(self.value)


class IntField(Field):
    """Integer field"""
    def __init__(self, args):
        super(IntField, self).__init__( args )


    def validate(self):
        """integer validation"""
        print "Dentro validate di IntField del valure di %s = %s" % (self.value, type(self.value))
        try:
            self.value= int(self.value)
        except Exception:
            return False
        return True


class DirField(Field):
    def __init__(self,args):
        super(DirField, self).__init__( args )
        self.completer = FilesCompleter
        self.validate_fn = None
        if 'validate_fn' in args.keys():
            self.validate_fn = args['validate_fn']

    def validate(self):
        """docstring for validate"""
        from os.path import isdir
        valid = isdir(self.value)
        if valid and self.validate_fn != None:
            valid = self.validate_fn()
        return valid



class FileField(Field):
    def __init__(self,args):
        from rlcompleter import Completer
        super(FileField, self).__init__( args )
        self.completer = Completer

    def validate(self):
        """docstring for validate"""
        return True
