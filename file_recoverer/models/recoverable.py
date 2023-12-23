import os
import subprocess
import re

# Regular expression to parse the output of fls
fls_output_pattern = re.compile(r'r/r (\*?)\s*(\d+):\s*(.*)')

# Class to represent a recoverable file
class Recoverable:
    # Constructor
    # 
    # Parameters:
    # inode: The inode number of the file
    # name: The name of the file
    # deleted: Whether the file is deleted or not
    def __init__(self, inode, name, deleted=False):
        self.inode = inode
        self.name = name
        self.deleted = deleted

    # Human readable representation of the object
    def __str__(self):
        return f"{self.inode}: {self.name}"

    # The string representation of the object
    def __repr__(self):
        return f"Recoverable({self.inode}, {self.name})"
    
    # Equality check
    def __eq__(self, other):
        return self.inode == other.inode
    
    # Hashing function
    def __hash__(self):
        return hash(self.inode)
    
    # Function to recover the file
    #
    # Parameters:
    # disk_image: The disk image to recover the file from
    def recover(self, disk_image):
        # Recovering the file using icat
        output_file = f"recovered_file_{self.name}"
        subprocess.run(["icat", "-o", "0", disk_image, self.inode], stdout=open(output_file, "wb"))

        # Checking if the file was recovered successfully
        if os.path.exists(output_file):
            print(f"File with inode number {self.inode} has been successfully recovered as {output_file}")
        else:
            print(f"Error: File recovery for inode {self.inode} failed.")

    # Function to create a list of recoverable files from the output of fls
    #
    # Parameters:
    # fls_output: The output of fls
    @staticmethod
    def list_from_fls(fls_output):
        # print(fls_output)
        recoverables = []
        for line in fls_output.splitlines():
            # print(line)
            recoverable = Recoverable.from_line(line)
            if recoverable:
                recoverables.append(recoverable)
        return recoverables

    # Function to create an instance of Recoverable from a line of fls output
    #
    # Parameters:
    # line: A line of fls output
    @staticmethod
    def from_line(line):
        # Using the regular expression to parse the line into its components
        match = fls_output_pattern.match(line)

        if match:
            # Match found. Using the components to create an instance of Recoverable
            return Recoverable(match.group(2), match.group(3), bool(match.group(1)))
        else:
            # Match not found. Return None
            return None
