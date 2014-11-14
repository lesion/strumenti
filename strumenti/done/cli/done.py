#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK


def main():
    import argcomplete, argparse
    from strumenti.libs import log
    from os import path
    from strumenti.done.libs.module import list_modules, get_run_callback

    modules = list_modules()

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='module')
    for module in modules:
        tmp_parser = subparsers.add_parser(module)
        for arg,value in get_run_callback(path.dirname( modules[module] ),module)()[2].iteritems():
            try:
                tmp_parser.add_argument('-'+arg).completer = value.completer
            except Exception:
                tmp_parser.add_argument('-'+arg)

    argcomplete.autocomplete(parser)
    (args,unknown) = parser.parse_known_args()
    log.info( "Loading module from `%s`" % args.module )
    run = get_run_callback( path.dirname( modules[args.module]), args.module )
    from cli import DoneCli 
    DoneCli( args.module, run, vars(args), unknown )

if __name__ == '__main__':
    main()
