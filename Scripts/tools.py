import os 
import subprocess
import paramiko

#install the paramiko module to use the ssh_command functionality
#pip install paramiko


"""
    SimpleTool 

    create_file : create a file with the specified name and contents
    read_file : read a file with the specified name and contents
    update_file : update the content of the specified file
    delete_file : delete the specified file

    create_directory : create a directory with the specified name
    delete_directory : delete the specified directory and all its contents
    list_files_directory : list all files and directories in the specified directory
    change_directory : change the current working directory to the specified directory

    execute_command : execute a given command and return the result
    ssh_command : execute a command over ssh using paramiko with pem file.

"""



class SimpleTool:

    #Basic file operations using python os.
    #CRUD Operation

    def create_file(file_name, content):
        #Create a new file with the given content
        try:
            with open(file_name, 'w') as file:
                file.write(content)
            print(f"File '{file_name}' created successfully.")
        except Exception as e:
            print(f"Error creating file '{file_name}': {str(e)}")

    def read_file(file_name):
        #Read the content of the given file
        try:
            with open(file_name, 'r') as file:
                print(file.read())
        except FileNotFoundError:
            print(f"File '{file_name}' not found.")
        except Exception as e:
            print(f"Error reading file '{file_name}': {str(e)}")

    def update_file(file_name, content):
        #Update the content of the given file
        try:
            with open(file_name, 'w') as file:
                file.write(content)
            print(f"File '{file_name}' updated successfully.")
        except FileNotFoundError:
            print(f"File '{file_name}' not found.")
        except Exception as e:
            print(f"Error updating file '{file_name}': {str(e)}")


    def delete_file(file_name):
        #Delete the given file
        try:
            os.remove(file_name)
            print(f"File '{file_name}' deleted successfully.")
        except FileNotFoundError:
            print(f"File '{file_name}' not found.")
        except Exception as e:
            print(f"Error deleting file '{file_name}': {str(e)}")



    #Directory operation scripts
    #Create directory , list files , subdirectory and delete directory

    def create_directory(directory_name):
        #Create a new directory
        try:
            os.mkdir(directory_name)
            print(f"Directory '{directory_name}' created successfully.")
        except FileExistsError:
            print(f"Error name already exist. '{directory_name}")
        except Exception as e:
            print(f"Error creating directory '{directory_name}")


    def delete_directory(directory_name):
        #Delete the given directory
        try:
            os.rmdir(directory_name)
            print(f"Directory '{directory_name}' deleted successfully.")
        except FileNotFoundError:
            print(f"Directory '{directory_name}' not found.")
        except Exception as e:
            print(f"Error deleting directory '{directory_name}': {str(e)}")


    def list_files_in_directory(directory_name_path):
        #List all files in the given directory
        try:
            files = os.listdir(directory_name_path)
            print(f"Files in directory '{directory_name_path}':")
            for file in files:
                print(file)
        except FileNotFoundError:
            print(f"Directory '{directory_name_path}' not found.")
        except Exception as e:
            print(f"Error listing files in directory '{directory_name_path}': {str(e)}")


    def delete_directory(directory_name):
        #Delete the given directory
        try:
            os.rmdir(directory_name)
            print(f"Directory '{directory_name}' deleted successfully.")
        except FileNotFoundError:
            print(f"Directory '{directory_name}' not found.")


    def change_directory(current_directory, new_directory):
        #Change the directory from the current directory to the new directory
        try:
            os.chdir(new_directory)
            print(f"Current directory '{current_directory}'")
            print(f"Changed directory to '{new_directory}'.")
            #print the new current directory
            print(f"Current directory: {os.getcwd()}")
            #use the list files to print the files in the new directory
            SimpleTool.list_files_in_directory(new_directory)
        except FileNotFoundError:
            print(f"Directory '{new_directory}' not found.")
            print(f"Current directory: {os.getcwd()}")
        except Exception as e:
            print(f"Error changing directory: {str(e)}")



#Execute shell command using subprocess
def execute_command(command):
    #Execute the given shell command and print the output and error messages if any.
    try:
        output = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(output.stdout)
        print(output.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e.returncode}, {e.output}")


def ssh_command(hostname, username, pem_file_path, command):
    """
      Executes a command on a remote server using SSH with a .pem key file.

    Args:
        server_ip_address: The hostname or IP address of the remote server.
        username: The username to use for SSH authentication.
        pem_file_path: The path to the .pem key file.
        command: The command to execute on the remote server.

    Returns:
        The output of the command.
        If the command fails, it returns the error message.
    """

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        #load the pem file
        key = paramiko.RSAKey.from_private_key_file(pem_file_path)

        # connect to the remote server using the loaded key
        # and execute the command
        ssh.connect(hostname=hostname, username=username, pkey=key)
        stdin, stdout, stderr = ssh.exec_command(command)

        print(stdout.read().decode())
        print(stderr.read().decode())

        #Close the ssh connection    
        ssh.close()

    except paramiko.AuthenticationException:
        print("Authentication failed")
    except Exception as e:
        print(f"Error executing SSH command: {str(e)}")


