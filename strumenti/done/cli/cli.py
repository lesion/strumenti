from sys import exit
import readline

class DoneCli():

    def __init__( self, module_name, run, key_args, pos_args ):

        readline.parse_and_bind("tab: complete")
        readline.set_completer_delims(' \t\n;')

        self.key_args = key_args
        self.pos_args = pos_args

        # first run call at this module to request fields needed
        # at the first step
        ( self.title, self.next_step, needed_args ) = run()
        self.process_args(needed_args)
        self.process_page()


    def process_page( self ):
        ( title, self.next_step, needed_args) =  self.next_step()

        if self.next_step == None:
          # print "[ This is last page ]\n", fields
          exit( 0 )

        self.process_args(needed_args)
        print "\t [ %s\n" % title
        self.process_page()


    def process_args(self, needed_args):
        args = {}

        # need to check if fields needed is inserted
        if needed_args:
            for name,arg in needed_args.iteritems():

                try:
                    readline.set_completer(arg.completer)
                except Exception:
                    pass

                # check if field.name is included in arguments
                if self.key_args[name]!=None:
                    arg.value = self.key_args[name]
                elif len(self.pos_args):
                    arg.value = self.pos_args.pop()
                elif arg.mandatory:
                    value = raw_input(" %s [%s]: " %(name,arg.default ))
                    if not value: value=arg.default
                    arg.value=value
                else:
                    arg.value=arg.default


                if arg.validate and not arg.value:
                    valid = False
                    while not valid:
                        value = raw_input(" %s [%s]: " %(name,arg.default ))
                        if not value: value=arg.default
                        arg.value=value
                        valid=arg.validate()

        return args



