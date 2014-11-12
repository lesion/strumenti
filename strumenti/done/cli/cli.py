from sys import exit
import glob
import readline

class DoneCli():

    def __init__( self, module_name, run, args ):

        readline.parse_and_bind("tab: complete")
        readline.set_completer(self.complete)
        readline.set_completer_delims(' \t\n;')
        key_args = {}
        pos_args = []

        # split positional arguments from key/value args
        for arg in args:
            if '=' in arg:
                arg_name, arg_value = arg.split( '=' )
                key_args[ arg_name ] = arg_value
            else:
                pos_args.append(arg)

        self.key_args = key_args
        self.pos_args = pos_args


        # first run call at this module to request fields needed
        # at the first step
        ( self.title, self.next_step, needed_args ) = run()
        args = self.process_args(needed_args)
        self.process_page( args )


    def complete(self,text,state):
        """autocomplete"""
        #print "\nSTATE:", state
        #readline.insert_text(glob.glob(text+'*')[state])
        return (glob.glob(text+'*')+[None])[state]


    def process_page( self, args ):
        ( title, self.next_step, needed_args) =  self.next_step( args )

        if self.next_step == None:
          # print "[ This is last page ]\n", fields
          exit( 0 )

        args = self.process_args(needed_args)
        print "\t [ %s\n" % title
        self.process_page(args)


    def process_args(self, needed_args):
        args = {}

        # need to check if fields needed is inserted
        if needed_args:
            for arg in needed_args:

                # check if field.name is included in arguments
                if arg.name in self.key_args.keys():
                    print "Setting %s to %s" % (arg.name,self.key_args[arg.name])
                    args[arg.name] = self.key_args[arg.name]
                elif len(self.pos_args):
                    args[arg.name] = self.pos_args.pop()
                elif arg.mandatory:
                    value = raw_input(" %s [%s]: " %(arg.name,arg.default ))
                    if not value: value=arg.default
                    args[arg.name]=value
                else:
                    args[arg.name]=arg.default

                if arg.validate:
                    while not arg.validate(args[arg.name]):
                        value = raw_input(" %s [%s]: " %(arg.name,arg.default ))
                        if not value: value=arg.default
                        args[arg.name]=value


        return args



