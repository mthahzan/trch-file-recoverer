import os
import subprocess
import logging

from .models.recoverable import Recoverable

# Logger for the file recovery script
logger = logging.getLogger(__name__)

# Function to list recoverable files and their inode numbers
def list_recoverable_files(disk_image):
    # Running fls on the disk image and getting the output
    logger.debug(f"Running fls -F {disk_image}")
    fls_output = subprocess.check_output(["fls", "-F", disk_image], universal_newlines=True)

    # Creating a list of recoverable files from the string output
    logger.debug("Creating a list of recoverable files from the output of fls")
    file_list = Recoverable.list_from_fls(fls_output)
    logger.debug(f"Created a list of {len(file_list)} recoverable files")

    return file_list

# Function to recover files by inode number
def recover_files(disk_image, recoverables):
    # Looping through the list of recoverable files and recovering them
    for recoverable in recoverables:
        logger.debug(f"Recovering file with inode number {recoverable.inode}")
        recoverable.recover(disk_image)

# Function to check if The Sleuth Kit is installed
def check_tsk_installed():
    # Check if fls is installed
    # This can tell us if The Sleuth Kit is installed
    try:
        logger.debug("Checking if fls is installed")
        subprocess.run(["fls", "-V"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        logger.debug("fls is installed")
        return True
    except subprocess.CalledProcessError:
        logger.error("fls is not installed")
        return False

# Function to print a list of recoverable files
def print_recoverables(recoverables):
    # Printing the header
    print("{:<10} {:<}".format("Inode", "Name"))
    print("-" * 55)

    # Looping through the list of recoverable files and printing them
    for recoverable in recoverables:
        print("{:<10} {:<}".format(recoverable.inode, recoverable.name))

def main():
    # Check if The Sleuth Kit is installed
    if not check_tsk_installed():
        logger.error("The Sleuth Kit is not installed. Exiting."")
        print("Error: The Sleuth Kit is not installed on your system. Please check README.md for installation instructions.")
        sys.exit(1)

    # Check if the script is run with the correct number of arguments
    import sys
    if len(sys.argv) != 2:
        logger.error("Incorrect number of arguments provided. Exiting.")
        print("Usage: python recover_files.py <image_file>")
        sys.exit(1)

    disk_image = sys.argv[1]

    # Check if the provided file exists
    if not os.path.isfile(disk_image):
        logger.error("The provided image file does not exist. Exiting.")
        print("Error: The provided image file does not exist.")
        sys.exit(1)

    # List recoverable files and their inode numbers
    file_list = list_recoverable_files(disk_image)

    print("List of recoverable files with more details:")
    logger.debug("Printing the list of recoverable files")
    print_recoverables(file_list)

    # Prompt the user to enter inode numbers for file recovery
    logger.debug("Prompting the user to enter inode numbers for file recovery")
    inode_input = input("Enter the inode number(s) of the file(s) you want to recover (comma-separated, 'ALL' for all, or 'q' to quit): ")

    # Check if the user wants to quit
    if inode_input == "q":
        logger.debug("User chose to quit. Exiting.")
        sys.exit(0)

    # Check if the user wants to recover all files
    if inode_input == "ALL":
        logger.debug("User chose to recover all files")
        recover_files(disk_image, file_list)
    else:
        # Split the user input into a list of inode numbers
        inode_numbers = inode_input.split(',')
        logger.debug(f"User chose to recover {len(inode_numbers)} files")

        recoverables_of_interest = []
        for inode_number in inode_numbers:
            inode_number = inode_number.strip()
            try:
                # Find the recoverable with the specified inode number
                logger.debug(f"Finding the recoverable with inode number {inode_number}")
                recoverables_of_interest.append(next(recoverable for recoverable in file_list if recoverable.inode == inode_number))
            except StopIteration:
                logger.error(f"File with inode number {inode_number} does not exist. Exiting.")
                print(f"Error: File with inode number {inode_number} does not exist.")
                sys.exit(1)

        # Recover the specified files
        logger.debug(f"Recovering {len(recoverables_of_interest)} files")
        recover_files(disk_image, recoverables_of_interest)

# Main program
if __name__ == "__main__":
    logger.debug("Starting the file recovery script by directly running file_recoverer.py")
    main()
