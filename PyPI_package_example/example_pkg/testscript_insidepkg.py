import os
print('Here inside the package')
print("Here's in {0}".format(os.path.realpath(__file__)))
print("Working dir: {0}".format(os.path.realpath(__file__)))