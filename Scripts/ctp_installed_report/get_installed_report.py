import re
import os
import json
from datetime import datetime

#Date today
current_date = datetime.now().strftime("%Y-%m-%d")



def get_the_directory_name(directory):
    '''
    Get the directory name from the given directory path
    '''
    dirname = os.path.dirname(directory)
    dirname = dirname.split("/")[-2]
    return dirname


def write_log_file(filename,directory):
    '''
    Write log file
    '''
    #make a log directory if it doesnt exist create it
    log_directory = "logs"
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    #create log file name
    log_file_name = f"get_installed_report-{current_date}.log"

    #open log file in append mode
    with open(os.path.join(log_directory, log_file_name), 'a') as log_file:
        log_file.write(f"{filename} - {current_date} Success \n")

def extract_string(content, pattern):
    '''
    Extract the string content from the given content
    '''
    matches = []
    for line in content:
      if re.search(pattern, line):
        matches.append(line.strip())

        numbers = set()
        for match in matches:
        #get the number of from the word PATCH
          match_number = re.search(r'\d+', match)
            #get only the number length is greater than 2.
          if len(str(match_number.group())) > 2:
            #remove duplicates from the string
            if match_number.group() not in numbers:
              numbers.add(match_number.group())

        #convert set to a list and sort them.
        sorted_numbers = sorted(numbers, reverse=True)
    return sorted_numbers


def save_to_json(data, output_file):
     '''
     Save to Json format
     '''
     with open(output_file, 'a') as file:
         json.dump(data, file, indent=4)


def main(input_file, output_file, pattern):
    '''
    Main function to execute the script
    '''
    # Read the content of the input file
    try:
        with open(input_file, 'r') as file:
            content = file.readlines()

            extracted_string = extract_string(content, pattern)
            
            if extracted_string:  
                #save string into json
                directory_name = get_the_directory_name(input_file)
                data = {f"{directory_name} : {pattern}": extracted_string}
                save_to_json(data, output_file)
                print(f"Patch numbers saved to {output_file}") # print success message
                write_log_file(output_file, directory_name)  # log success message
            else:
                print("No patch numbers found.")

    except FileNotFoundError:
        print(f"File {input_file} not found.")

    except Exception as e:
        print(f"Error processing file: {str(e)}")


#File path and input file
lsapps_input_file = r"/Users/raymartorbita/Documents/DevOps/Scripts/ctp_installed_report/lsapps/Admin/test_file.txt"
output_file = r"/Users/raymartorbita/Documents/DevOps/Scripts/ctp_installed_report/test_output.json"

pristine_input_file = r"/Users/raymartorbita/Documents/DevOps/Scripts/ctp_installed_report/pristine/Admin/test_file.txt"
output_file = r"/Users/raymartorbita/Documents/DevOps/Scripts/ctp_installed_report/test_output.json"

patch_pattern = [r'PATCH', r'YEAREND']
patch_productline = [lsapps_input_file, pristine_input_file]



if __name__ == "__main__":
    #Pattern to search for patches
    for pattern in patch_pattern:
        #Loop through the product line files
        for PLs in patch_productline:
            #call the main function to execute the script
            main(PLs, output_file, pattern)




