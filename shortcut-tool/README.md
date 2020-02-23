# shortcut-tool
Remove the stupid .exe mid-fix of shortcuts on Windows

## Installation
```
pip install shortcut-tool
```

## Usage
```
# process in the current directory
python -m shortcut_tool rmexe

# process in another directory
python -m shortcut_tool rmexe -i input/dir -o output/dir

# automatically delete the mid-fixed shortcut
python -m shortcut_tool rmexe -d
```