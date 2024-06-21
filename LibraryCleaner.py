import os
import unidecode

files = os.scandir()

for x in files :
    newPath = x.path[2:]
    if x.is_file() and newPath != 'LibraryCleaner.py' :
        if x.name[0].isnumeric():
            os.rename(x, "0/{}".format(newPath))
            print("0/{}".format(newPath))
            
        else:
            os.rename(x, "{}/{}".format(unidecode.unidecode(x.name[0]), newPath))
            print("{}/{}".format(x.name[0], newPath))

input("Press any key...")