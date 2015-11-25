#!/usr/bin/env python

import os
import shutil
import argparse
import logging
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

timeStamp =  date.today()

args = parser.parse_args()

# Define variables
backupdir = args.BACKUPDIR
destinationroot = args.DESTINATIONDIR
destinationdir = destinationroot + '/' + str(timeStamp)
logfile = args.logfile
retention = args.retention

#Logging
rootLogger = logging.getLogger()
logFormatter = logging.Formatter("%(asctime)s - %(message)s")
rootLogger.setLevel(logging.INFO)
if logfile:
    fileHandler = logging.FileHandler(logfile)
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)

if not args.quiet:
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)


# directory exist-check
def check_dir_exist(os_dir):
    if not os.path.exists(os_dir):
        logging.error("{} does not exist.".format(os_dir))
        exit(1)

check_dir_exist(backupdir)

# delete function
def delete_files(directory):
    try:
        print "removing the " + directory
        shutil.rmtree(directory)
        logging.info("Deleting " + directory)
    except OSError:
        logging.warning("Could not delete " + dirctory)
        pass

# list all folder in backup
def listdirs(folder):
    return [d for d in os.listdir(folder) if os.path.isdir(os.path.join(folder, d))]

# Check if existing folder is older than retention period
if args.retention:
    for k2 in listdirs(destinationroot):
        if ((timeStamp-datetime.datetime.strptime(k2, '%Y-%m-%d').date()).days >= retention):
            remDirectory = destinationroot + '/' + k2
            print remDirectory
            delete_files(remDirectory)

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
