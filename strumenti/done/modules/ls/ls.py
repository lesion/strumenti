from strumenti.done.libs.module import list_modules, Field, finish, fill_values

class LsModule( ):
    ## values
    values = {}

    def run( self, values=None ):
        fields = { 'match': Field({}) }
        return ("List and search modules", self.ls, fields)

    @fill_values
    def ls(self,values):
        if not len(values):
            mods = list_modules()
        else:
            mods = [x for x in list_modules() if values['match'] in x]

        print "\t-[ %s" % ("\n\t-[ ".join(mods))
        return finish
