import os
import requests
import re

from zipfile import ZipFile
from bs4 import BeautifulSoup

modelDLFolder = ".\\steamcmd\\steamapps\\workshop\\content\\1840\\"
modelFinalFolder = ".\\Models\\"

if not os.path.isdir(modelFinalFolder):
    os.mkdir(modelFinalFolder)

w = os.walk(modelDLFolder)
for (paths, dirs, filenames) in w:
    for name in filenames:
        if name.endswith('.zip'):
            # Find workshop page from id
            wsID = filenames[0][0:-4]
            print("Charging {}...".format(wsID))
            URL = "https://steamcommunity.com/sharedfiles/filedetails/?id={}".format(wsID)
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, "html.parser")
            newName = soup.find(attrs={"class": "workshopItemTitle"}).get_text()
            print("Model : {}".format(newName))

            # Get link of preview image

            try:
                imgPreview = requests.get(soup.find(attrs={"id": "previewImageMain"})['src'])
            except TypeError:
                print("Main preview image not available, selecting the worskshop image instead...")
                imgPreview = requests.get(soup.find(attrs={"id": "previewImage"})['src'])
                      
            # Extract model into models folder
            print(r"Starting extraction from {}{}\\{}.zip".format(modelDLFolder,wsID,wsID))
            newNamePath = re.sub(r'[^\w_. -]', '', newName)
            
            with ZipFile(r"{}{}\\{}.zip".format(modelDLFolder,wsID,wsID)) as zippy:
                # zippy.printdir()
                zippy.extractall(r'{}{}'.format(modelFinalFolder, newNamePath))
            zippy.close()
            
            print(r'Extraction to {}{} complete !'.format(modelFinalFolder, newNamePath))
                  
            # Download preview image
            with open(modelFinalFolder + newNamePath + "\\" + newNamePath + ".jpg", "wb") as f:
                f.write(imgPreview.content)

            # Take description and steam user names in place in a file
            textDesc = soup.find(attrs={"class": "workshopItemDescription"}).get_text()
            # Find the usename account box, stript the tabs, take the username from the raw code by split at the newline
            creatorName = soup.find(attrs={"class": "friendBlockContent"}).get_text().strip().rsplit("\n")[0]
 
            print("Uploaded by : {}. Getting description... ".format(creatorName))
            
            with open("{}{}\\readme.txt".format(modelFinalFolder, newNamePath), 'w', encoding="utf-8") as f:
                f.write('{} (ID {})\nDownloaded from Steam, uploaded by {}.\n\nOriginal description : \n{}'.format(newName, wsID, creatorName, textDesc))

            print("{} successfully moved ! \n".format(newName))
