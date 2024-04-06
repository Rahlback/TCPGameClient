from shutil import copyfile
from sys import executable
from subprocess import check_call
from os.path import exists


# Install required packages
check_call([executable, "-m", "pip", "install","-r","requirements.txt"])

# Copy config 
file_exists = exists("config.yml")
if (file_exists):
    print("config.yml already exists!")
else:
    copyfile('config_template.yml', 'config.yml')
