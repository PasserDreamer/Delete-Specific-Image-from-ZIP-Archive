import hashlib
import os
import sys
import zipfile
import subprocess

def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    print("===========================================")
    print("Image MD5：  "+ hash_md5.hexdigest())
    print("===========================================")
    return hash_md5.hexdigest()

def decode_filename(filename):
    try:
        return filename.encode('cp932').decode('utf-8')
    except UnicodeDecodeError:
        return filename

def remove_image_by_md5(target_path, reference_image_md5):
    error_logs = []
    if os.path.isdir(target_path):
        for zip_file in os.listdir(target_path):
            zip_file_path = os.path.join(target_path, zip_file)
            if zip_file_path.endswith('.zip'):
                error_log = check_and_remove_image(zip_file_path, reference_image_md5)
                if error_log:
                    error_logs.append(error_log)
    elif target_path.endswith('.zip'):
        error_log = check_and_remove_image(target_path, reference_image_md5)
        if error_log:
            error_logs.append(error_log)
    else:
        print("The provided path is neither a zip file nor a folder.")
    
    # Print all collected error logs at the end of the process
    if error_logs:
        print("\n錯誤匯總|Error Logs：")
        for log in error_logs:
            print(log)

def check_and_remove_image(zip_path, target_md5):
    last_file = None
    last_file_md5 = None
    try:
        with zipfile.ZipFile(zip_path, 'r') as zfile:
            inner_files = zfile.namelist()
            if inner_files and (inner_files[-1].endswith('.png') or inner_files[-1].endswith('.jpg')):
                last_file_data = zfile.read(inner_files[-1])
                last_file_md5 = hashlib.md5(last_file_data).hexdigest()
                last_file = inner_files[-1]
    except Exception as e:
        return f"Error processing {zip_path}: {str(e)}"

    if last_file and last_file_md5 == target_md5:
        subprocess.run(['C:\\Program Files\\7-Zip\\7z.exe', 'd', zip_path, last_file], check=True)
        print("Image Removed.")
    elif last_file:
        print("| MD5 mismatch | " + zip_path)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python remove_specific_image.py {reference image path} {target zip path or target folder path}")
    else:
        reference_image_path = sys.argv[1]
        target_path = sys.argv[2]
        reference_image_md5 = calculate_md5(reference_image_path)
        remove_image_by_md5(target_path, reference_image_md5)
