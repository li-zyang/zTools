import os
print('Hello World!')
print('This is example_pkg.__init__')
print("Here's in {0}".format(os.path.realpath(__file__)))
print("Working dir: {0}".format(os.path.realpath(__file__)))

from example_pkg.testscript_insidepkg import *