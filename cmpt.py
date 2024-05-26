import os
import tarfile
import subprocess

MAX_SIZE = 30 * 1024 * 1024  # 30 MiB

def create_tar_archive(input_file_paths, tar_name):
    with tarfile.open(tar_name, "w") as tar:
        for file_path in input_file_paths:
            tar.add(file_path, arcname=os.path.basename(file_path))
    print(f"Created tar archive {tar_name}.")

def split_tar_archive(tar_name, max_size):
    split_command = ["split", "-b", str(max_size), tar_name, tar_name + ".part_"]
    subprocess.run(split_command)
    print(f"Split tar archive into parts with maximum size of {max_size / (1024 * 1024)} MiB.")

def compress_files_to_split_tar(input_file_paths, max_size=MAX_SIZE):
    tar_name = "archive.tar"
    create_tar_archive(input_file_paths, tar_name)
    split_tar_archive(tar_name, max_size)
    os.remove(tar_name)  # Optionally remove the original tar file after splitting

if __name__ == "__main__":
    # Get input file paths (dragged-in files)
    input_file_paths = input("Enter the paths to the input files, separated by commas: ").strip().split(',')

    # Validate input file paths
    valid_file_paths = []
    for input_file_path in input_file_paths:
        input_file_path = input_file_path.strip()
        if not os.path.isfile(input_file_path):
            print(f"Error: Input file not found: {input_file_path}")
        else:
            valid_file_paths.append(input_file_path)
    
    if valid_file_paths:
        compress_files_to_split_tar(valid_file_paths)
    else:
        print("No valid files to compress.")
