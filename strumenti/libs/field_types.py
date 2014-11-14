from argcomplete.completers import FilesCompleter

class Field(object):
    """generic representation of strumenti's field"""
    def __init__(self, args):
        super(Field, self).__init__()
        self.args = args

        self.completer = None
        if 'completer' in args.keys():
            self.completer = args['completer']

        self.default = None
        if 'default' in args.keys(): self.default = args['default'] # set default value if needed

        self.mandatory = False
        if 'mandatory' in args.keys():
            self.mandatory = args['mandatory']

        self.value = None

    def __str__(self):
        return str(self.value)

    def validate(self):
        pass


class IntField(Field):
    """Integer field"""
    def __init__(self, args):
        super(IntField, self).__init__( args )


    def validate(self):
        """integer validation"""
        try:
            self.value= int(self.value)
        except Exception:
            return False
        return True


class DirField(Field):
    def __init__(self,args):
        super(DirField, self).__init__( args )
        if not self.completer:
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
        super(FileField, self).__init__( args )
        if not self.completer:
            from rlcompleter import Completer
            self.completer = Completer


    def validate(self):
        """docstring for validate"""
        return True
