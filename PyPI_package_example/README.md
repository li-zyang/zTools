# example_pkg
An example PyPI package

## Project structure
Project structure of a PyPI package
```
Project-root/
 │
 ├─Package-root/  # Determines the package / program name 
 │ │              # import <the-name> or python -m <the-name>
 │ │
 │ ├─subpackage_1/
 │ ├─subpackage_2/
 │ ├─...
 │ │
 │ ├─submodule_1.py
 │ ├─submodule_2.py
 │ ├─...
 │ │
 │ └─__init__.py    # Initialize the package (when be imported)
 │                  # or run as the entry of a program (when called with python -m)
 │
 ├─setup.py         # Used when packaging & installing
 ├─README.md        # Readme
 └─LICENSE          # License of the package
```
## Writing setup.py
```
import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name = "--distribution-name--",                   # the name shown in 'pip search'. 
                                                    # note: use '-' instead of '_'
  version = "--0.0.1--",
  author = "--your-name--",
  author_email = "--your-email--",
  description = "--short-discription--",
  long_description = long_description,              # from README.md, no need to modify
  long_description_content_type = "text/markdown",  # description type, no need to modify
  url = "--project-repository--",
  packages = setuptools.find_packages(),            # grep packages automatically
  classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],                                                # https://pypi.org/classifiers/
  python_requires = '>=3.6',
)
```
## Writing \_\_init\_\_.py
### import submodules / subpackages
```
import <this-package>.<sub>
```
or  
```
from <this-package>.<sub> import <something>
```
&lt;sub&gt; (in the file system) can be a script file such as `submodule.py` or another package such as `subpackage_1/`  
### write other code
#### detect whether this package is being called as a program or imported as a library
```
if __name__ == '__name__':
  # called as a program
  do_something()
```
#### detect where the script itself is
```
where_am_I = os.path.realpath(__file__) # -> str, actually concatenatedthe working dirctory with 
                                        # the relative path of the script (__file__) 
```
#### detect where python is
```
where_is_python = sys.executable        # -> str
```

## Uploading package to PyPI
1. **install setuptools, wheel, twine for uploading**
```
pip install setuptools wheel twine
```
2. **Pack your package**
```
python setup.py sdist bdist_wheel       # -> dist/<sth>.whl, dist/<sth>.tar.gz
```
3. **Use twine to upload your package**
```
# assume you're in the "Project-root" where "dist/" is generated there
twine upload --repository-url https://test.pypi.org/legacy/ dist/*  # test PyPI index (may not needed)
twine upload dist/*   # real PyPI index
```
The username is your username (*not email*) on PyPI, and the password is your PyPI password  
Or create an config file `~/.pypirc` to skip the username & password etc.  
```
[distutils]
index-servers = pypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = <username>
password = <password>
```

## Manage the uploaded package
Login to https://pypi.org/ (or https://test.pypi.org/ if test PyPI was used) and manage the uploaded package

## Install the uploaded package
```
pip install your-package
```
or if PyPI was used
```
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps <THE-PACKAGE-NAME>
```