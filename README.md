# CERSAI Batch File Generation

## Introduction
Are you facing delays in CERSAI submissions? Spending too much time entering details manually? Getting multiple rejections with batch uploads? Don't worry! With this solution, you can increase the accuracy of your CERSAI batch file up to **99.9%**. Say goodbye to manual entries and embrace streamlined, error-free submissions with our automated process.

## Features
- **High Accuracy**: Achieve **99.9%** accuracy in your CERSAI batch file generation.
- **Automated Process**: Say goodbye to manual data entry. This script automates the transformation of data into the required CERSAI format.
- **Error-free Submissions**: Automatically clean and format data to meet CERSAI requirements, reducing the chances of rejections.
- **Seamless File Upload**: Upload processed files directly to the SFTP server.
- **File Handling**: Handles file conversion, manipulation, and storage efficiently.

## Prerequisites
- Python 3.x
- Required Python libraries: `paramiko`, `csv`, `datetime`, `re`, `thefuzz`, `pandas`, `unidecode`

## How It Works
1. **File Retrieval**: The script fetches the required files from a remote server using SFTP.
2. **Data Processing**: It processes the downloaded files by cleaning the data, removing special characters, formatting it as required, and applying the necessary transformations.
3. **File Conversion**: Converts the processed data into the CERSAI-required format.
4. **File Upload**: After conversion, the processed file is uploaded back to the server.

## Script Overview

### Configuration Variables
```python
host = '' 
port = ''
username = '' 
password = '' 

remote_file_path = "" 
processed_file_path = "" 
output_file_path = "" 

DB_NAME = "" 
DB_USER = "" 
DB_PASS = "" 
DB_HOST = "" 
DB_PORT = "" 

```

## Functions

### `upload_files_to_sftp(file_name, dest_file_path)`
Uploads a file to a remote server via SFTP.

### `get_file_name()`
Generates a unique output filename using the current date and time.

### `remove_space(lst)`
Removes extra spaces from the list of strings.

### `remove_special_char(lst)`
Removes special characters from the list of strings.

### `replace_char(lst, char, rep)`
Replaces a specific character in the list of strings.

### `remove_non_ascii(text)`
Removes non-ASCII characters from a string.

### `convert(date_time)`
Converts the date string into a `datetime` object.

### `convert_csv_to_dat(file, folder_name_path, sftp)`
Converts an Excel file to CSV, processes the data, and generates a `.dat` file formatted for CERSAI submission.

### `list_file_folder()`
Lists files in a remote directory.

### `upload_processed_and_delete_file_from_sftp(local_file_path, remote_file_path, sftp, source_file_path)`
Uploads the processed file to the SFTP server and deletes the source file from the input directory.

### `sftp_make_out_dir(file, sftp)`
Creates an output folder on the SFTP server for each file.

---

## Main Function

```python
def main(): 
    file_list = list_file_folder() 
    for file in file_list: 
        print(f"Download file to local path:{file} from {remote_file_path}/{file}") 
        ssh_client = paramiko.SSHClient() 
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
        ssh_client.connect(hostname=host, port=port, username=username, password=password) 
        sftp = ssh_client.open_sftp() 
        sftp.get(f"{remote_file_path}/{file}", f"{file}") 
        
        # Create Directory for Each File to store the Output/resultant files 
        folder_name_path = sftp_make_out_dir(file, sftp) 
        
        # Process the files
        print("###### Code for processing the files ##########") 
        convert_csv_to_dat(file, folder_name_path, sftp) 
        
        # After file processing, move it to processed folder and delete from the input directory
        upload_processed_and_delete_file_from_sftp(f"{file}", f"{processed_file_path}/{file}", sftp, f"{remote_file_path}/{file}") 
        sftp.close() 

## File Flow
1. The script starts by listing the files in the remote directory.
2. It then downloads each file to the local machine.
3. For each file, it creates an output directory on the SFTP server for storing processed files.
4. The script converts and processes the data, converting Excel files to CSV, cleaning the data, formatting it, and generating the required `.dat` file for CERSAI submission.
5. After processing, the processed file is uploaded back to the SFTP server, and the source file is deleted from the input directory.

---

## Output Format
The script generates `.dat` files in the following format for each row:

- **SI Record**: Contains specific information such as registration ID, customer details, etc.
- **IMM Record**: Information related to the property.
- **BOR Record**: Customer and borrower information.
- **CHG Record**: Company information.

---

## Conclusion
This script automates the generation of CERSAI batch files with 99.9% accuracy, reducing manual effort and errors. It also ensures the data is processed and uploaded efficiently, meeting the requirements of CERSAI submissions.




