import os
import requests
from zipfile import ZipFile
from bs4 import BeautifulSoup

modelDLFolder = "./steamcmd/steamapps/workshop/content/1840/"
modelFinalFolder = "Models/"

if not os.path.isdir(modelFinalFolder):
    os.mkdir(modelFinalFolder)

w = os.walk(modelDLFolder)
for (paths, dirs, filenames) in w:
    for name in filenames:
        if name.endswith('.zip'):
            # Find workshop page from id
            wsID = filenames[0][0:-4]
            URL = "https://steamcommunity.com/sharedfiles/filedetails/?id={}".format(wsID)
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, "html.parser")
            newName = soup.select_one(".workshopItemTitle").get_text()
            print(wsID + ' ' + newName)

            # Get link of preview image
            imgPreview = requests.get(soup.find(attrs={"id": "previewImageMain"})['src'])

            # Extract model into models folder
            zippy = ZipFile(modelDLFolder + wsID + "/" + wsID + ".zip","r")
            zippy.extractall(modelFinalFolder + newName)

            # Download preview image
            with open(modelFinalFolder + newName + "/" + newName + ".jpg", "wb") as f:
                f.write(imgPreview.content)

            # Take description and steam user names in place in a file
            textDesc = soup.find(attrs={"class": "workshopItemDescription"}).get_text()
            # Find the usename account box, stript the tabs, take the username from the raw code by split at the newline
            creatorName = soup.find(attrs={"class": "friendBlockContent"}).get_text().strip().rsplit("\n")[0]
            
            print(textDesc)
            print(creatorName)

            with open(modelFinalFolder + newName + "/" +'readme.txt', 'w') as f:
                f.write('Downloaded from Steam, from {}. \n Original description : \n{}'.format(creatorName, textDesc))
