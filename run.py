from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
from datetime import datetime
import os

now = datetime.now()
gauth = GoogleAuth(settings_file='settings.yaml', http_timeout=None)
drive = GoogleDrive(gauth)

MAIN_FOLDER_NAME = 'RPiTimelapse'
DATE_FOLDER_NAME = now.strftime('%Y-%m-%d')
FULL_DATE_STRING = now.strftime('%Y-%m-%d_%H-%M-%S')
PHOTO_FILE_NAME = FULL_DATE_STRING + '.jpg'

def getFolderId(folderName, parentFolder='root'):
    file_list = drive.ListFile({'q': "'" + parentFolder + "' in parents and trashed=false"}).GetList()
    for file in file_list:
        if file['title'] == folderName:
            return file['id']
    return None

def createFolder(folderName, parentFolderId=None):
    metadata = {
        'title': folderName,
        'mimeType': 'application/vnd.google-apps.folder',
    }
    if parentFolderId != None:
        metadata['parents'] = [{"kind": "drive#fileLink", "id": parentFolderId}]
    folder = drive.CreateFile(metadata)
    folder.Upload()
    print 'created folder ' + folderName + ' with id ' + folder['id']
    return folder['id']

main_folder_id = getFolderId(MAIN_FOLDER_NAME)
if main_folder_id == None:
    main_folder_id = createFolder(folderName=MAIN_FOLDER_NAME)
print('main_folder_id', main_folder_id)

date_folder_id = getFolderId(DATE_FOLDER_NAME, main_folder_id)
if date_folder_id == None:
    date_folder_id = createFolder(folderName=DATE_FOLDER_NAME, parentFolderId=main_folder_id)
print('date_folder_id', date_folder_id)

os.system('raspistill -t 2000 -w 2592 -h 1944 -rot 180 -awb auto -o ' + PHOTO_FILE_NAME)

photo = drive.CreateFile(metadata={
    'title': PHOTO_FILE_NAME,
    'parents': [{"kind": "drive#fileLink", "id": date_folder_id}]
})
photo.SetContentFile(PHOTO_FILE_NAME)
photo.Upload()

os.remove(PHOTO_FILE_NAME)

print('OK')