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
