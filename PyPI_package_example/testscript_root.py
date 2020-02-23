import os
print('Here at the package root')
print("Here's in {0}".format(os.path.realpath(__file__)))
print("Working dir: {0}".format(os.path.realpath(__file__)))