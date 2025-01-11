from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload
from gdrive_creds import SERVICE_ACCOUNT
import pyclip
import os
import sys
from datetime import datetime
from zipfile import ZipFile
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, simpledialog
import shutil
import time


'''
Script to upload files to Google Drive and generate google drive url

Author: Raymart
Version: 1.0
Date: 11-01-25

Usage:
   Tool is a GUI tool that allows users to upload files to Google Drive and retrieve the Google Drive URL.

Note:
    Storage quota is limited to 15GB. base on the free google drive plan per user.


Pre-requisite to use this tool:

# Create a Google Cloud Project:
    # Go to the Google Cloud Console.
    # Create a new project or select an existing one.
# Enable the Drive API:
    # In the project's dashboard, enable the "Google Drive API".
# Create Service Account:
    # In the project's credentials page, create a new service account.
    # Download the JSON key file for the service account.
    # Replace 'path/to/your/keyfile.json' with the actual path to the downloaded key file.
# Set parent_folder_id (optional):
    # If you want to upload the file to a specific folder, get the folder's ID and set the parent_folder_id argument accordingly.

'''


# Define the scope and service account file path
SCOPE = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = SERVICE_ACCOUNT
PARENT_FOLDER_ID = None

log_path = os.getcwd() + "\logs"
root = None

def set_folder():
    '''
    Set the parent folder ID
    '''
    global PARENT_FOLDER_ID

    new_parent_folder_id = simpledialog.askstring("Set Parent Folder ID", "Enter the parent folder ID:", initialvalue=PARENT_FOLDER_ID)

    if new_parent_folder_id:
        PARENT_FOLDER_ID = new_parent_folder_id
    else:
        messagebox.showwarning("Error", "Parent folder ID not set.")


# Create credentials using the service account file
def create_credentials():
    '''
    Create credentials using the service account file
    '''
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPE)

    return credentials


def resource_path(relative_path):
    '''
    return the full path to image files in the project
    '''
    base_path = os.path.abspath(".")

    full_path = os.path.join(base_path, relative_path)

    return full_path


def write_log(file_to_upload):
    '''
    write a log entry when file is uploaded for audit

    '''
    global log_path
    log_file = f"gdrive_upload.log"

    if not os.path.exists(log_path):
        os.makedirs(log_path)

    with open(f"{log_path}\{log_file}", "a") as log:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - {file_to_upload} File uploaded \n"
        log.write(log_entry)


def zip_files(files_to_zip):
    #get the current date and time
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    #create a temp directory
    temp_dir = os.path.join(os.getcwd(), "temp")

    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
        

    #convert the path to a list and get the file name using os.path.basename 
    file_name = [os.path.basename(files_to_zip)]

    #name of the backup directory.
    zip_full_name = f"{file_name[0]}_{timestamp}.zip"
 
    #change the directory to the directory of the file
    os.chdir(os.path.dirname(files_to_zip))

    try:
        #iterate through the files and zip them
        with ZipFile(zip_full_name, "w") as zipf:
            for file in file_name:
                zipf.write(file)
         #copy the zip file to the temp directory
        shutil.copy(zip_full_name, temp_dir)
    except Exception as e:
        print(f"An error occurred while moving the zip file to the temp directory. {e}")
        
    return zip_full_name


def retrieve_url():
    '''
    Retrieve the Google Drive URL
    '''
    try:
        #Google Drive URL
        FOLDER_PATH = f"https://drive.google.com/file/d/{file_id}/view"

        display_window = tk.Toplevel()
        display_window.title("GDrive URL")
        display_message = tk.Label(display_window,text=f"Copy the link below to download the file", background="black", foreground="yellow")
        display_message.pack()

        text_area = scrolledtext.ScrolledText(display_window, wrap=tk.WORD, width=40, height=10)
        text_area.insert(tk.END, FOLDER_PATH)
        text_area.pack()

        #copy the file id to the clipboard to download
        copy_button = tk.Button(display_window, text="Copy to Clipboard", command=lambda: (pyclip.copy(FOLDER_PATH), messagebox.showinfo("Copied", "URL copied to clipboard.")))
        copy_button.pack()

        close_button = tk.Button(display_window, text="Close", command=display_window.destroy)
        close_button.pack()

    except Exception:
        messagebox.showerror("Error", f"An error occurred: You need to Upload before retrieving the URL.")


def clean_the_zip(uploaded_file_name, max_retries=3):
    '''
    Clean the zip file
    '''
    if uploaded_file_name in os.listdir():
        
        for attempt in range(max_retries):
            try:
                os.remove(uploaded_file_name)
                print("File deleted successfully.")
                break # Exit the loop if the file is deleted successfully
            except Exception as e:
                print(f"Error deleting file: {e}")
                time.sleep(8) # Wait for 8 seconds before the next attempt
    print(f"Failed to delete {uploaded_file_name} after {max_retries} attempts.")


def upload_file():
    '''
    Uploads a file to Google Drive.
    '''
    global file_id

    #open the file dialog and get the selected file
    selected_file = filedialog.askopenfilename()

    if not PARENT_FOLDER_ID:
        messagebox.showerror("Please add the parent folder ID.", "Please add the parent folder ID before uploading a file.")

    else:
        if selected_file:
            if len(selected_file) > 1:
                #zip the files
                zip_file_path = zip_files(selected_file)
                file_to_upload = zip_file_path
            else:
                file_to_upload = selected_file[0]
        
        #get the file name
        uploaded_file_name = os.path.basename(file_to_upload)
        #create credentials
        creds = create_credentials()
        #create drive api client
        service = build('drive', 'v3', credentials=creds)
        file_metadate = {
            'name': uploaded_file_name,
            'parents': [PARENT_FOLDER_ID]
        }

        try:
            #Process to upload the file 
            media = MediaFileUpload(uploaded_file_name, mimetype='text/plain', resumable=True)
            file = service.files().create(body=file_metadate, media_body=media, supportsAllDrives=True, fields='id').execute()
            #create a log entry
            write_log(uploaded_file_name)
            #get the file id
            file_id = file.get('id')
            messagebox.showinfo("Success", f"File uploaded successfully. \nPlease use the Retrieve URL button to download the file.")

        except Exception as e:
            messagebox.showerror("Error", f"Error uploading file: {e}")

def gui():
    '''
    Gui for the program 
    '''
    global root

    root = tk.Tk()
    root.title("GDrive Upload Tool")
    root.geometry("420x190")
    root.eval("tk::PlaceWindow . center")
    root.iconbitmap(resource_path(".\img\gdrive.ico"))
    # root.iconbitmap("C:\RaymartFiles\Learning\Python\projects\devops\Scripts\img\gdrive.ico")

    img = tk.PhotoImage(file=resource_path(".\img\gdrive.png"))
    # img = tk.PhotoImage(file="C:\RaymartFiles\Learning\Python\projects\devops\Scripts\img\gdrive.png")
    
    parent_folder_button = tk.Button(root, image=img, text="Add Folder Name", command=set_folder)
    parent_folder_button.pack(side=tk.LEFT, anchor='nw')

    upload_button = tk.Button(root, text="Upload File", width=20, command=upload_file)
    upload_button.pack(side=tk.TOP)

    retrieve_button = tk.Button(root, text="Retrieve GDrive URL", width=20, command=retrieve_url)
    retrieve_button.pack(side=tk.TOP)

    close_button = tk.Button(root, text="Close", width=20, command=root.destroy)
    close_button.pack(side=tk.TOP)

    root.mainloop()


def main():
    #Run the application
    gui()
    

if __name__ == "__main__":
    main()
    

