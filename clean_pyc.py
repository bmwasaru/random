"""
delete all .pyc bytecode files in a directory tree
use command line arg as root if given else current working directory
"""

import os, sys

find_only = False
root_dir = os.getcwd() if len(sys.argv) == 1 else sys.argv[1]
found = removed = 0

for (this_directory_level, subs_here, files_here) in os.walk(root_dir):
    for filename in files_here:
        if filename.endswith('.pyc'):
            fullname = os.path.join(this_directory_level, filename)
            print("=>", fullname)
            if not find_only:
                try:
                    os.remove(fullname)
                    removed += 1
                except:
                    type, inst = sys.exc_info()[:2]
                    print('*'*4, 'Failed: ', filename, type, inst)
            found += 1

print('Found', found, ' files, removed', removed) 
