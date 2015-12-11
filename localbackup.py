#!/usr/bin/env python
# Author : Sebastian Gumprich http://zufallsheld.de
# Modifier : Ketan Patel http://k2patel.in
# License : BSD
# Usage : python localbackup.py -h
####

import os
import shutil
import argparse
import logging
import logging.handlers
import datetime
from datetime import date
from sh import rsync


#Parse arguments
parser = argparse.ArgumentParser(
    description=__doc__)

parser.add_argument("BACKUPDIR", help="Specify the directory to backup.")
parser.add_argument("DESTINATIONDIR", help="Specify the directory where the backup is stored.")
parser.add_argument("-r", "--retention", help="No. of copy to retain.", type=int)
parser.add_argument("-e", "--exclude", help="Exlude the following directories from backup.", action="append")
parser.add_argument("-l", "--logfile", help="Specify the logfile to monitor.")
parser.add_argument("-q", "--quiet", help="Do not print to stdout.", action="store_true")

time_stamp =  date.today()

args = parser.parse_args()

# Define variables
backupdir = args.BACKUPDIR
destinationroot = args.DESTINATIONDIR
destinationdir = destinationroot + '/' + str(time_stamp)
logfile = args.logfile
retention = args.retention

#Logging
root_logger = logging.getLogger()
log_formatter = logging.Formatter("%(asctime)s - %(message)s")
root_logger.setLevel(logging.INFO)
if logfile:
    file_handler = logging.FileHandler(logfile)
    file_handler.setFormatter(log_formatter)
    root_logger.addHandler(file_handler)
else:
    default_handler = logging.handlers.SysLogHandler(address = '/dev/log')
    root_logger.addHandler(default_handler)

if not args.quiet:
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    root_logger.addHandler(console_handler)


# directory exist-check
def check_dir_exist(os_dir):
    """ This Function check if directory exists or not. """
    if not os.path.exists(os_dir):
        logging.error("{} does not exist.".format(os_dir))
        exit(1)

check_dir_exist(backupdir)

# delete function
def delete_files(directory):
    """ This function delete files if required to maintain retention. """
    try:
        print "removing the " + directory
        shutil.rmtree(directory)
        logging.info("Deleting " + directory)
    except OSError:
        logging.warning("Could not delete " + dirctory)
        pass

# list all folder in backup
def listdirs(folder):
    """ This function list the all folder in backup folder. """
    return [d for d in os.listdir(folder) if os.path.isdir(os.path.join(folder, d))]

# Check if existing folder is older than retention period
if args.retention:
    for k2 in listdirs(destinationroot):
        if ((time_stamp-datetime.datetime.strptime(k2, '%Y-%m-%d').date()).days >= retention):
            rem_directory = destinationroot + '/' + k2
            print rem_directory
            delete_files(rem_directory)

# handle exclusions
exclusions = []
if args.exclude:
    for argument in args.exclude:
        exclusions.append("--exclude={}".format(argument))


# Do the actual backup
logging.info("Starting rsync.")
if logfile and exclusions and args.quiet:
    rsync("-auhv", exclusions, "--log-file={}".format(logfile), backupdir, destinationdir)
elif logfile and exclusions:
    print(rsync("-auhv", exclusions, "--log-file={}".format(logfile), backupdir, destinationdir))
elif args.quiet and exclusions:
    rsync("-av", exclusions, backupdir, destinationdir)
elif logfile and args.quiet:
    rsync("-av", "--log-file={}".format(logfile), backupdir, destinationdir)
else:
    rsync("-av", backupdir, destinationdir)

logging.info("done.")
