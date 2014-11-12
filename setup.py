from setuptools import setup, find_packages
from distutils import cmd
from os import system

class build_deb(cmd.Command):
  description = 'Create a deb package'
  user_options = []

  def initialize_options( self ):
    pass

  def finalize_options( self ):
    pass

  def run( self ):
    system( 'debuild -I.svn -I.bzr -Ibuild -tc -S' )


    
setup(
    name = "strumenti",
    version = "1.0",
    cmdclass = { 'build_deb': build_deb },
    packages = find_packages( ),
    entry_points = { 'console_scripts': [
      'strumenti = strumenti.done.gui.done:main' ] }

)
