import re
import os
import json
from datetime import datetime
import timeit
from pprint import pprint

#get the current date.
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")

def resource_path(relative_path):
    '''
    return the full path to image files in the project
    '''
    base_path = os.path.abspath(".")
    full_path = os.path.join(base_path, relative_path)

    return full_path

def get_the_directory_name(directory):
    '''
    Get the directory name from the given directory path
    '''
    dirname = os.path.dirname(directory)
    dirname = dirname.split("/")[-2]
    return dirname

def write_log_file(directory_name,filename):
    '''
    Write log file
    '''
    #make a log directory if it doesnt exist create it
    log_directory = "logs"
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    #create log file name
    log_file_name = f"get_installed_report-{CURRENT_DATE}.log"
    #open log file in append mode
    with open(os.path.join(log_directory, log_file_name), 'a') as log_file:
        log_file.write(f"{directory_name} - {pattern} - {filename} - {CURRENT_DATE} Success \n")

def save_to_json(data, output_file):
     '''
     Save to Json format
     '''
     with open(output_file, 'a') as file:
         json.dump(data, file, indent=4)

def extract_string(content, pattern):
    '''
    Extract the string content from the given content
    '''
    #get only the lines that match the pattern
    matches = [line.strip() for line in content if re.search(pattern, line)]
    numbers = set()

    for match in matches:
    #get the number of from the word PATCH | YEAREND
      match_number = re.search(r'\d+', match)
      #get only the number length is greater than 2.
      # #remove duplicates from the string
      # if match_number.group() not in numbers:
      if len(str(match_number.group())) > 2 and match_number.group() not in numbers:
        numbers.add(int(match_number.group()))
    #sort the converted numbers
    sorted_numbers = sorted(numbers, reverse=False)
    return sorted_numbers

def check_installation_success(log_text):
  ''''
  Checks if the lawappinstall installation was successful and extracts successful patch names.
  Returns A list of successful patch names.
  '''
  successful_patches = []
  patch_pattern = r"lawappinstall (UPDATE|ACTIVATE) ([A-Z0-9._]+) installation started"

  for match in re.finditer(patch_pattern, log_text):
    patch_name = match.group(2) 
    end_of_patch_section = log_text.find(f"lawappinstall {match.group(1)} {patch_name} installation completed successfully", match.end())
    if end_of_patch_section != -1:
      patch_section = log_text[match.start():end_of_patch_section]
      if "ERROR" not in patch_section:
        successful_patches.append(patch_name)

  return successful_patches

def main(input_file, output_file, pattern):
    '''
    Main function to execute the script
    '''
    # Read the content of the input file
    try:
        with open(input_file, 'r') as file:
            content = file.read()
            #get only the install success
            successful_patches = check_installation_success(content)
            #extract and sort the successful patches
            extracted_string = extract_string(successful_patches, pattern)
            
            if extracted_string:  
                #save string into json
                directory_name = get_the_directory_name(input_file)
                data = {f"{directory_name.lower()}_{pattern.lower()}": extracted_string}
                save_to_json(data, output_file)
                print(f"Patch numbers saved to {output_file}") # print success message
                write_log_file(directory_name, output_file)  # log success message

            else:
                print("No patch numbers found.")
                
    except Exception as e:
        print(f"Error processing file: {str(e)}")


def test_execution_time(input_file, output_file, pattern):
    start_time = timeit.default_timer()
    main(input_file, output_file, pattern)
    end_time = timeit.default_timer()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time:.2f} seconds")




#File path and input file
lsapps_input_file = r"C:/RaymartFiles/Learning/Python/projects/devops/Scripts/ctp_installed_report/lsapps/Admin/test_file.txt"
pristine_input_file = r"C:/RaymartFiles/Learning/Python/projects/devops/Scripts/ctp_installed_report/pristine/Admin/test_file.txt"
output_file = r"C:/RaymartFiles/Learning/Python/projects/devops/Scripts/ctp_installed_report/test_output.json"

#Working when using linux or Mac
# lsapps_input_file = resource_path(r"ctp_installed_report\lsapps\Admin\test_file.txt")
# pristine_input_file = resource_path(r"ctp_installed_report\pristine\Admin\test_file.txt")
# output_file = resource_path(r"ctp_installed_report\test_output.json")

patch_pattern = [r'PATCH', r'YEAREND']
patch_productline = [lsapps_input_file, pristine_input_file]

if __name__ == "__main__":
    #Pattern to search for patches
    for pattern in patch_pattern:
        #Loop through the product line files
        for PLs in patch_productline:
            #call the main function to execute the script
            # main(PLs, output_file, pattern)
            # Time the execution of the function
            test_execution_time(PLs, output_file, pattern)






