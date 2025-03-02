import paramiko 
import csv 
import datetime 
from datetime import date 
import re 
from string import digits 
from thefuzz import fuzz 
import pandas as pd 
from unidecode import unidecode 


#SFTP CREDENTIALS
host = 'your_sftp_host'
port = your_sftp_port
username = 'your_username'
password = 'your_password' 

#SFTP PATHS
remote_file_path = "path/to/remote/files"
processed_file_path = "path/to/processed/files"
output_file_path = "path/to/output/files"


#ADATABASE CONFIGURATION (NOT REQUIRED)
DB_NAME = "your_db_name"
DB_USER = "your_db_user"
DB_PASS = "your_db_password"
DB_HOST = "your_db_host"
DB_PORT = "your_db_port"


current_date_time = datetime.datetime.now() 
current_date_time = current_date_time.strftime("%Y_%m_%d") 

def upload_files_to_sftp(file_name,dest_file_path): 
    try: 
        transport = paramiko.Transport((host, port)) 
        transport.connect(username=username, password=password) 
        print("Connection Established Successfully") 
        sftp = paramiko.SFTPClient.from_transport(transport) 
        remote_file = dest_file_path 
        sftp.put(file_name,dest_file_path) 
        print(f"Uploaded {file_name} to {dest_file_path}") 
        sftp.close() 
        transport.close() 
    except Exception as e: 
        print("ERROR:" , e) 

def get_file_name(): 
    today = date.today() 
    current_time = datetime.datetime.now() 
    print(current_time) 
    current_time = str(current_time) 
    current_time = current_time[0:19] 
    current_time= current_time.replace('-','') 
    current_time = current_time.replace(':','') 
    current_time = current_time.replace(' ','') 
    print(current_time) 
    print(today) 
    
    #CRS_JC123_456789_YYYYMMDDHHMMSS 
    output_filename = f"CRS_JC123_456789_{current_time}.dat" 
    print(output_filename) 
    return output_filename 

def remove_space(lst): 
    return [re.sub(' +', ' ', s) for s in lst] 

def remove_special_char(lst): 
    return [re.sub('\W+',' ', s) for s in lst] 

def replace_char(lst, char,rep): 
    return [s.replace(char, rep) for s in lst] 

def remove_non_ascii(text): 
    return unidecode(text) 

def convert(date_time): 
    format = '%Y-%m-%d' 
    datetime_str = datetime.datetime.strptime(date_time, format) 
    return datetime_str 

def convert_csv_to_dat(file,folder_name_path,sftp): 
    output_file = get_file_name() 
    excel_df = pd.read_excel(file) 
    file = file.replace('xlsx','csv') 
    excel_df.to_csv(file,index = None,header=True) 
    input_file = file 
    today = date.today() 
    file = open(output_file,'a') 
    
    with open(input_file, "r" , encoding='UTF-8') as input_csv: 
        reader = csv.reader(input_csv,delimiter=',') 
        count = len(list(reader))-1 
        print(count) 
        current_date = today 
        header = f"FH|SI_REGN|{count}|{current_date}" 
        file.write(f"{header}\n") 
        file.close() 
        file = open(output_file,'a') 
        
        with open(input_file, "r" , encoding='UTF-8') as input_csv: 
            reader = csv.reader(input_csv,delimiter=',') 
            next(reader) 
            for i, row in enumerate(reader): 
                print("inside") 
                rowline = row 
                print(i) 
                print(row) 
                row[14] = str(int(float(row[14]))) 
                row[15] = str(int(float(row[15]))) 
                row[16] = str(int(float(row[16]))) 
                row[17] = str(int(float(row[17]))) 
                row[26] = str(int(float(row[26]))) 
                row[27] = str(int(float(row[27]))) 
                row[28] = str(int(float(row[28]))) 
                row[29] = str(int(float(row[29]))) 
                row[4] = str(int(float(row[4]))) 
                row[5] = str(int(float(row[5]))) 
                row[6] = str(int(float(row[6]))) 
                row[7] = str(int(float(row[7]))) 
                asset_desc_str = row[10] 
                row[10] = asset_desc_str[0:90] 
                cus_addr_str = row[23] 
                row[23] = cus_addr_str[0:49] 
                plot_no = re.sub('\D', ' ', row[11]) 
                plot_no = re.sub(' +', ' ', plot_no) 
                
                if plot_no == ' ' or plot_no == '0': 
                    plot_no = row[11] 
                    plot_no = re.sub('[\W_]+',"",plot_no) 
                    plot_no = plot_no[0:14] 
                else: 
                    plot_no = plot_no[0:19] 
                
                test_str = row[13] 
                remove_digits = str.maketrans('', '', digits) 
                res = test_str.translate(remove_digits) 
                row[13] = res[0:45] 
                str_test = row[30] 
                str_1 = "sqft" 
                str_2 = "sqmt" 
                str_3 = "sqyd" 
                Ratio1 = fuzz.ratio(str_1.lower(),str_test.lower()) 
                Ratio2 = fuzz.ratio(str_2.lower(),str_test.lower()) 
                Ratio3 = fuzz.ratio(str_3.lower(),str_test.lower()) 
                max_Ratio = max(Ratio1,max(Ratio2,Ratio3)) 
                
                if Ratio1 == max_Ratio : 
                    row[30] = "6" 
                elif Ratio2 == max_Ratio : 
                    row[30] = "7" 
                else: 
                    row[30] = "8" 
                
                gender_code = row[20] 
                gender = gender_code[0:1] 
                dob = row[21] 
                dob = dob[0:10] 
                dob = convert(dob) 
                dob = str(dob) 
                dob = dob[0:10] 
                asset_area = row[12] 
                asset_area = asset_area.replace(' ','') 
                asset_area = int(float(asset_area)) 
                print(asset_area) 
                row = replace_char(row , '|' , ' ') 
                row = replace_char(row , '&' , 'and') 
                row = replace_char(row , '\n' , ' ') 
                row = remove_special_char(row) 
                row = remove_space(row) 
                asset_desc = row[10] 
                cus_addr = row[23] 
                project_name = row[13] 
                j = i+1 
                
                a = f"SI|{j}|1|1|0|17|21|1|{current_date}|{row[18]}|{row[0]}||FIRST|0|{row[2]}" 
                a = remove_non_ascii(a) 
                a = a.replace('.','') 
                a = re.sub(r'(?:(?<=\|) | (?=\|))','',a) 
                a = re.sub(' +', ' ', a) 
                a = re.sub(r'(?:(?<=\|) | (?=\|))','',a) 
                
                b = f"IMM|1|1||1||{asset_desc}|{asset_desc}|{plot_no}|{asset_area}|{row[30]}|{plot_no}|||{project_name}|||{int(row[14])}|{int(row[14])}|{int(row[15])}|{int(row[16])}|{int(row[17])}|IND||||" 
                b = remove_non_ascii(b) 
                b = b.replace('.','') 
                b = re.sub(r'(?:(?<=\|) | (?=\|))','',b) 
                b = re.sub(' +', ' ', b) 
                b = re.sub(r'(?:(?<=\|) | (?=\|))','',b) 
                print(row[26]) 
                print(row[27]) 
                print(row[28]) 
                print(row[29]) 
                
                c = f"BOR|1|IND|1||||||||||{gender}|{row[9]}|{row[22]}|{dob}|||{cus_addr}|||{int(row[26])}|{int(row[27])}|{int(row[28])}|{int(row[29])}|IND" 
                c = remove_non_ascii(c) 
                c = c.replace('.','') 
                c = re.sub(r'(?:(?<=\|) | (?=\|))','',c) 
                c = re.sub(' +', ' ', c) 
                c = re.sub(r'(?:(?<=\|) | (?=\|))','',c) 
                
                company_name = ""
                company_desc = ""
                d = f"CHG||{company_name}|{company_desc}|||{int(row[4])}|{int(row[5])}|{int(row[6])}|{int(row[7])}|IND" 
                d = remove_non_ascii(d) 
                d = d.replace('.','') 
                d = re.sub(r'(?:(?<=\|) | (?=\|))','',d) 
                d = re.sub(' +', ' ', d) 
                d = re.sub(r'(?:(?<=\|) | (?=\|))','',d) 
                
                print(a) 
                print(b) 
                print(c) 
                print(d) 
                
                file.write(f"{a}\n") 
                file.write(f"{b}\n") 
                file.write(f"{c}\n") 
                file.write(f"{d}\n") 
                file.close() 
                file.close() 
                
                upload_files_to_sftp(output_file,f"{folder_name_path}/{output_file}") 

def list_file_folder(): 
    ssh_client = paramiko.SSHClient() 
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
    ssh_client.connect(hostname=host,port=port,username=username,password=password) 
    sftp = ssh_client.open_sftp() 
    files = sftp.listdir(remote_file_path) 
    sftp.close() 
    ssh_client.close() 
    return files 

def upload_processed_and_delete_file_from_sftp(local_file_path,remote_file_path,sftp,source_file_path): 
    upload_files_to_sftp(local_file_path,remote_file_path) 
    sftp.remove(source_file_path) 
    
def sftp_make_out_dir(file,sftp): 
    folder_name = f"{file.replace('.xlsx','')}{current_date_time}" 
    sftp.mkdir(f"{output_file_path}/{folder_name}") 
    output_folder_path_get = f"{output_file_path}/{folder_name}" 
    return output_folder_path_get 

def main(): 
    file_list = list_file_folder() 
    for file in file_list: 
        print(f"Download file to local path:{file} from {remote_file_path}/{file}") 
        ssh_client = paramiko.SSHClient() 
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
        ssh_client.connect(hostname=host,port=port,username=username,password=password) 
        sftp = ssh_client.open_sftp() 
        # Dowloading file to local 
        sftp.get(f"{remote_file_path}/{file}", f"{file}") 
        
        # Create Directory for Each File to store the Output/resultant files 
        folder_name_path = sftp_make_out_dir(file,sftp) 
        
        #Code to Get the API Response and Transform into required Format 
        print("######Code for processing the files##########") 
        convert_csv_to_dat(file,folder_name_path,sftp) 
        
        # After File Processing Completed Add File to Processed Folder and delete file from Input Directory
        upload_processed_and_delete_file_from_sftp(f"{file}",f"{processed_file_path}/{file}",sftp,f"{remote_file_path}/{file}") 
        sftp.close() 
        
if __name_ == "_main_": 
    main()