# SimTeACC

## Requirements
1. Python 3.9 (3.10 might not work due a deprecated feature in 3.10, however this was tested on 3.10 of Windows 10, and 3.9 of Ubuntu Linux)
2. Pillow (PIL) 9 (older versions might work)
3. matplotlib 3.5.1 (older versions might not work)
4. tk (there's only 1 version)

Optional

5. pyinstaller 5.0.dev0 (perhaps 4.9 could work)

## How to run
Once you have python and each requirement setup double clicking the file on windows would be enough, however if it doesn't work try use the command prompt/terminal. Open a command prompt/terminal in the same directory and type in `python SimTeacc.pyw` assuming that you have put python in your path and you don't 2 versions of python that might get in the way. The same goes for linux except make sure to use `python3` instead of `python`. Some unix systems comes with `python3` preinstalled, however the version is often lower than required e.g. 3.6 therefore it's best to install a later version e.g. 3.9 and then run by using `python3.9`.

## How to build
Build it using pyinstaller on the platform required.

Make sure to add the option  `--add-data resources/\*;resources/` for windows or `--add-data resources/*:resources/ --hidden-import=TIL._tk_finder` for unix.
