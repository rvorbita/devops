from googleapiclient.discovery import build
from google.oauth2 import service_account
from gdrive_creds import SERVICE_ACCOUNT, FOLDER_ID
import pyclip


#Pre-requisite 
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


# Define the scope and service account file path
SCOPE = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = SERVICE_ACCOUNT
PARENT_FOLDER_ID= FOLDER_ID



# Create credentials using the service account file
def create_credentials():

    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPE)

    return credentials


def upload_file(file_path, file_name, parent_folder_id=None):

    """
    Uploads a file to Google Drive.

    Args:
        file_path (str): The path to the file to upload.
        file_name (str): The name of the file to upload.
        folder_id (str, optional): The ID of the folder to upload the file to. Defaults to None.
    
        
    Returns:
        The ID of the uploaded file.


    """

    creds = create_credentials()
    service = build('drive', 'v3', credentials=creds)


    file_metadate = {
        'name': file_name,
        'parents': [parent_folder_id]
    }

    file = service.files().create(body=file_metadate, media_body=file_path, supportsAllDrives=True, fields='id').execute()
    return file.get('id')
    

# Example usage:
file_id = upload_file(r"C:\Users\rorbita\Downloads\output_1686881.zip", r"output_1686881.zip", PARENT_FOLDER_ID)
#for testing purposes.
print(f'File uploaded successfully.'  f'File ID: {file_id}')

#Google Drive URL
FOLDER_PATH = f"https://drive.google.com/file/d/{file_id}/view"

#copy the file id to the clipboard to download
pyclip.copy(FOLDER_PATH)
print("Copied the download file URL.")
