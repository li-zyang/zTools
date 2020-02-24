# example_pkg
An example PyPI distribution package  

----
# Making a python distribution package

## Project structure
Project structure of a PyPI package
```
Project-root/
 │
 ├─Package_root/  # Determines the package / program name 
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
 │ ├─__main__.py    # entry of a 'program' (when being called with python -m)
 │ └─__init__.py    # Initialize the package (when being imported)
 │
 ├─setup.py         # Used when packaging & installing
 ├─README.md        # Readme
 └─LICENSE          # License of the package
```
### Execution sequence of scripts
#### $ python -m Package_root
```
start => '__init__.py' => imports => '__main__.py' => end
```
#### >>> import Package_root
```
start => '__init__.py' => imports => return
```
### Namespace model
```
+------------------------------------------------------------+
|                          Python                            |
|   +-------------+       +-------------+ +-------------+    |
|   | Script      |       | module 1    | | package 1   |    |
|   | ---         | ====> | {...}       | | {...}       |    |
|   | ----------- |       +-------------+ +-------------+    |
|   | -------     |       +-------------+ +-------------+    |
|   |  -------    |       | module 2    | | package 2   |    |
|   |  ----       | <==== | {...}       | | {...}       |    |
|   | {...}       |       +-------------+ +-------------+    |
|   +-------------+       ...                                |
|                                                            |
+------------------------------------------------------------+
```
### Import model
```
                                 +--------------------------+
+-----------------------+        | (Package-pool)           |
| # entry.py            |        |                          |
| ---                   |        |                          |
| -------               |        |    +---------------+     |
| -----                 |        +----| # __init__.py |-----+
| import demopkg -------+-----------> | ----          |
|                       |             | ---------     |
|                       |             | ...           |
|                       |             |               |
|          +----------+ |        +----| -- EXIT --    |-----+
|          | demopkg  | |        |    +---------------+     |
|          | {...}    | | <===== | demopkg                  |
|          +----------+ |        |                          |
| ------  <-------------+------- | {...}                    |
| ----------            |        +--------------------------+
| ...                   |
|                       |
+-----------------------+

1. the __init__.py is executed when the package is being imported but not initialized
2. __init__.py reads the packages from the package pool and import what it want to the package
3. the package is initialized and being accepted as an object by the script
```
> Note: Using `import <this-package>.<subpackage>` instead of `import <subpackage>` is still needed in `__init__.py`
  because python seeks the package in the package pool (python's package directory & the sibling directory where the 
  package itself lays) but not inside the package  

> Note: `__init__.py` should only do imports, codes that interacts with user / system etc. should be included in `__main__.py`
### Execution model
```
                            +-------------------------+
                            | (Package-pool)          |
                            |                         |
                            |    +---------------+    |
+-----------------------+   +----| # __init__.py |----+
|                       |        |               |          +-------------------+
| $ python -m demopkg --+------> | ...           |          | # __main__.py     |
|                       |        | -- EXIT --   -+--------> | import demopkg    |
|                       |   +----|               |----+     | +-----------+     |
|                       |   |    +---------------+    |     | | demopkg   |     |
|                       |   | demopkg                 | ==> | | {...}     |     |
|                       |   | {...}                   |     | +-----------+     |
|                       |   +-------------------------+     | -------           |
|                       |                                   | ---               |
|                       |                                   | ...               |
|                       |                                   |                   |
| $ _                 <-+---------------------------------- | -- EXIT --        |
|                       |                                   +-------------------+
+-----------------------+

1. __init__.py initializes the package and prepare for further execution (similar to importing)
2. the package is called as a software package, so the __main__.py is executed after the __init__.py
3. __main__.py manages what the program do
4. when __main__.py finishes, the program quits
```
### other code
#### \_\_name\_\_ variable
```
# __name__ is the package name in __init__.py
print(__name__)   # -> str, the package name
# while in __main__.py, it's '__main__'
print(__name__)   # -> '__main__'
```
#### detect where the script itself is
```
where_am_I = os.path.realpath(__file__) # -> str, actually concatenated the working dirctory with 
                                        # the relative path of the script (__file__) 
```
#### detect where python is
```
where_is_python = sys.executable        # -> str
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

## Packaging python distribution
1. **Install setuptools, wheel (if haven't)**
```
pip install setuptools wheel
```
2. **Run setup.py to pack a distribution**
```
python setup.py sdist bdist_wheel       # -> dist/<sth>.whl, dist/<sth>.tar.gz
```

## Installing the distribution
```
ls dist
pip install dist/<sth>.whl
```
and the package is now available for testing
```
python -m <package> ...
```

## Uploading package to PyPI
1. **install twine (if haven't)**
```
pip install twine
```
2. **Use twine to upload your package**
```
# assume you're in the "Project-root" where "dist/" is generated there

# test PyPI index (may not needed)
# twine upload --repository-url https://test.pypi.org/legacy/ dist/*

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