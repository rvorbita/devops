import os 
import sys

"""
File Extension Renaming: Script to rename multiple file extension in a directory based on a specific pattern.

"""

#get the directory path as argument
directory_path = sys.argv[1]

def get_the_file_directory(directory_path):
    # Get a list of all files in the directory
    files = os.listdir(directory_path)
    return files

def print_the_files(directory_path):
    new_files = os.listdir(directory_path)
    for file in new_files:
        print(file)

def change_the_file_extension(files, file_extension_to_search, file_extension_to_change):
    # Loop through each file in the directory
    for file in files:
        # Get the file extension
        file_extension = os.path.splitext(file)[1]

        try:
            # Check if the file is a text file
            if file_extension == "." + file_extension_to_search:
                # Get the file name without the extension
                file_name = os.path.splitext(file)[0]

                #change the file extension to the user input
                file_extension = file_extension_to_change

                # Rename the file
                new_file_name = f"{file_name}.{file_extension}"
                os.rename(os.path.join(directory_path, file), os.path.join(directory_path, new_file_name))
                #print the result
                print(f"File {file} renamed to {new_file_name} successfully.")

            else:
                print(f"File '{file_extension_to_search}' extension not found.")
                break

        except Exception as e:
            print(f"Error renaming file '{file_extension_to_search}': {str(e)}")
    



change_the_file_extension(get_the_file_directory(directory_path), input("Enter the file extension to change: "), input("Enter the new file extension: "))
