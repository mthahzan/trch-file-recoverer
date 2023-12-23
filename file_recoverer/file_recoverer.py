import os
import subprocess
from models.recoverable import Recoverable

# Function to list recoverable files and their inode numbers
def list_recoverable_files(disk_image):
    # Running fls on the disk image and getting the output
    fls_output = subprocess.check_output(["fls", "-F", disk_image], universal_newlines=True)

    # Creating a list of recoverable files from the string output
    file_list = Recoverable.list_from_fls(fls_output)

    return file_list

# Function to recover files by inode number
def recover_files(disk_image, recoverables):
    # Looping through the list of recoverable files and recovering them
    for recoverable in recoverables:
        recoverable.recover(disk_image)

# Function to check if The Sleuth Kit is installed
def check_tsk_installed():
    # Check if fls is installed
    # This can tell us if The Sleuth Kit is installed
    try:
        subprocess.run(["fls", "-V"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

# Function to print a list of recoverable files
def print_recoverables(recoverables):
    # Printing the header
    print("{:<10} {:<}".format("Inode", "Name"))
    print("-" * 55)

    # Looping through the list of recoverable files and printing them
    for recoverable in recoverables:
        print("{:<10} {:<}".format(recoverable.inode, recoverable.name))

# Main program
if __name__ == "__main__":
    # Check if The Sleuth Kit is installed
    if not check_tsk_installed():
        print("Error: The Sleuth Kit is not installed on your system.")
        sys.exit(1)

    # Check if the script is run with the correct number of arguments
    import sys
    if len(sys.argv) != 2:
        print("Usage: python recover_files.py <image_file>")
        sys.exit(1)

    disk_image = sys.argv[1]

    # Check if the provided file exists
    if not os.path.isfile(disk_image):
        print("Error: The provided image file does not exist.")
        sys.exit(1)

    # List recoverable files and their inode numbers
    file_list = list_recoverable_files(disk_image)

    print("List of recoverable files with more details:")
    print_recoverables(file_list)

    # Prompt the user to enter inode numbers for file recovery
    inode_input = input("Enter the inode number(s) of the file(s) you want to recover (comma-separated, 'ALL' for all, or 'q' to quit): ")

    # Check if the user wants to quit
    if inode_input == "q":
        sys.exit(0)

    # Check if the user wants to recover all files
    if inode_input == "ALL":
        recover_files(disk_image, file_list)
    else:
        # Split the user input into a list of inode numbers
        inode_numbers = inode_input.split(',')
        recoverables_of_interest = []
        for inode_number in inode_numbers:
            inode_number = inode_number.strip()
            try:
                recoverables_of_interest.append(next(recoverable for recoverable in file_list if recoverable.inode == inode_number))
            except StopIteration:
                print(f"Error: File with inode number {inode_number} does not exist.")
                sys.exit(1)

        # Recover the specified files
        recover_files(disk_image, recoverables_of_interest)
