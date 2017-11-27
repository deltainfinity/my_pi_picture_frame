# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 18:33:22 2017

@author: Ben Snell
"""

import dropbox
from dropbox.dropbox import Dropbox
import os
import datetime
import time
import shutil

def main():
    dbx = Dropbox('mNkdY-ZvlnAAAAAAAAAAJdViEYG10v_XnP1Eil4E5z4kF9pEL1cW2TyKFuMKYxxi')
    photo_directory = os.getcwd() + os.sep + 'drop_box_files'
    result = dbx.files_list_folder('',True, False, True)
    for entry in result.entries:
        process_entry(dbx, entry, photo_directory)

def process_entry(dbx, entry, photo_directory):
    if isinstance(entry, dropbox.files.FileMetadata):
        sync_file(dbx, entry, photo_directory)
    elif isinstance(entry, dropbox.files.FolderMetadata):
        sync_folder(entry, photo_directory)
    elif isinstance(entry, dropbox.files.DeletedMetadata):
        remove_deleted(entry, photo_directory)    
        
def remove_deleted(entry, photo_directory):
    file_path = format_path(entry.name, entry.path_display, photo_directory)
    local_file_path = file_path + os.sep + entry.name
    if os.path.exists(local_file_path):
        if os.path.isdir(local_file_path):
            shutil.rmtree(local_file_path)
        else:
            os.remove(local_file_path)
    
def sync_folder(entry, photo_directory):
    folder_path = format_path('', entry.path_display, photo_directory)
    if not os.path.exists(folder_path):
        create_directory(folder_path)
    
def sync_file(dbx, entry, photo_directory):
    file_path = format_path(entry.name, entry.path_display, photo_directory)
    local_file_path = file_path + os.sep + entry.name
    #if the directory containing the file does not exist, create it
    #and all parent diretcories
    if not os.path.exists(file_path):
        directory_created = create_directory(file_path)
        if directory_created == True:
            #if the directory did not exist then download the file
            download_to_file(dbx, local_file_path, entry.path_display)
    else:
        #check if the file exists locally
        if not os.path.exists(local_file_path):
            #file does not exist so download it
            download_to_file(dbx, local_file_path, entry.path_display)
        else:
            #local file exists - check to see if there is an updated version in DropBox
            #get the time that the local file was last modified
            local_mtime = os.path.getmtime(local_file_path)
            #convert the local file modification time to GMT
            local_mtime_dt = datetime.datetime(*time.gmtime(local_mtime)[:6])
            #get the size of the local file
            local_file_size = os.path.getsize(local_file_path)
            #if the server modified time is newer than the local modified time or
            #the file sizes are different, download a new copy of the DropBox file
            if local_mtime_dt < entry.server_modified or local_file_size != entry.size:
                download_to_file(dbx, local_file_path, entry.path_display)
        
def format_path(file_name, path, photo_directory):
    os_specific_path = photo_directory + path.replace('/', os.sep)
    os_specific_path = os_specific_path.rstrip(file_name)
    os_specific_path = os_specific_path.rstrip(os.sep)
    return os_specific_path

def create_directory(file_path):
    try:
        os.makedirs(file_path)
    except OSError as e:
        print "Error creating directory " + file_path
        print "Error number " + e.errno
        print "Error message " + e.message
        return False
    return True

def download_to_file(dbx, local_file_path, dbx_file_path):
    try:
        dbx.files_download_to_file(local_file_path, dbx_file_path)
    except dropbox.exceptions.ApiError as e:
        print "Error downloading DropBox file " + dbx_file_path + " to " + local_file_path
        print "Error: " + e.message
        
if __name__ == '__main__':
    main()