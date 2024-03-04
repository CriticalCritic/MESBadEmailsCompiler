'''
Available Storage Log
Creates or updates a CSV file with the remaining storage on the computer and time
Meant to be run with a program such as TaskScheduler to track disk usage
Daniel Olevsky
'''

from shutil import disk_usage
import datetime
import csv
from os.path import exists

path = "C:"
filename = 'disk_usage.csv'

# Get the disk usage
disk_usage = disk_usage(path)

# Calculate the storage left in GB rounded to two decimal places
storage_left = round(disk_usage.free / (1024.0 ** 3), 2)

# Get the time and trim to 3 milliseconds
time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

try:
    # Prepare for writing
    data = [{'Time M/D/Y': time, 'Storage Left (GB)': storage_left}]
    fields = ['Time M/D/Y', 'Storage Left (GB)']

    # Write the data to a CSV file
    if exists(filename):
        # Add new data to existing
        with open(filename, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writerows(data)

    else:
        # Create new file and write data
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(data)

except:
    # Log error occurence
    errorTime = datetime.datetime.now().strftime('%Y-%m-%d %H.%M.%S.%f')[:-3] + '.txt'
    errorFile = open('Error ' + errorTime, 'w')
    errorFile.write('Error at ' + str(errorTime) + ' with storage ' + str(storage_left) + '\nMake sure csv file is closed')
