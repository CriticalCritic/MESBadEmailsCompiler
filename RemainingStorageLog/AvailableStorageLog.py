'''
Available Storage Log
Creates or updates a CSV file with the remaining storage on the computer and time
Meant to be run with a program such as TaskScheduler to track disk usage
Best Case: O(n), Average Case: O(log(m))
Daniel Olevsky
'''

from shutil import disk_usage
import datetime
import csv
from os.path import exists

def writeCSV(filename, fields, lines):
    '''
    Create a CSV file with given information
    Overwrites existing CSV files

    Input:
    filename : name of file to create/modify
    fields : column names of CSV file
    lines : CSV data as Dictionaries
    '''
    # Access file
    with open(filename, "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        # Column names
        writer.writeheader()
        # Enter data
        for row in lines:
            writer.writerow(row)

def errorLog(location, storage_left):
    '''
    Create a text file with the time and storage info at error occurence

    Input:
    location: location of error log creation
    storage_left : Available space on machine at time of error
    '''
    # Get the time and trim to 3 milliseconds
    errorTime = datetime.datetime.now().strftime('%Y-%m-%d %H.%M.%S.%f')[:-3] + '.txt'
    # Create unique file
    errorFile = open(str(location) + 'Error_' + errorTime, 'w')
    # Log error occurence
    errorFile.write('Error at ' + str(errorTime) + ' with storage ' + str(storage_left) + '\nMake sure csv file is closed')

def AvailabelStorageLog(path, filename, location, maxLog):
    '''
    Create or update a CSV file with an entry of the current available storage and time

    Input:
    path : The storage to be checked ('C:' for whole computer)
    filename : name of CSV file log to create or modify
    location : location of CSV file to make/modify and possible new error files; must end with '\\' unless blank
    maxLog : max number of entries to be kept; oldest deleted first
    '''
    file = location + filename

    # Get the disk usage
    disk_use = disk_usage(path)

    # Calculate the storage left in GB rounded to two decimal places
    storage_left = round(disk_use.free / (1024.0 ** 3), 2)

    # Get the time and trim to nearest minute
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

    try:
        # Prepare for writing
        data = {'Time M/D/Y': time, 'Storage Left (GB)': storage_left}
        fields = ['Time M/D/Y', 'Storage Left (GB)']

        # Write the data to a CSV file
        if exists(file):

            # Create copy with new data inserted
            with open(file, "r", newline='') as f:
                # Read csv
                reader = csv.DictReader(f, fieldnames=fields)
                lines = []

                # Add new data to existing at top of list
                x = 0
                for line in reader:
                    # Remove oldest entries that overflow over max length allowed
                    if x < maxLog:
                        # Insert new data
                        if x == 0:
                            lines.append(data)
                        else:
                            lines.append(line)
                        x += 1
                    else:
                        break

            # Overwrite existing csv
            writeCSV(file, fields, lines)
                
        else:
            # Create new file and write data
            writeCSV(file, fields, [data])

    except:
        # Create error file
        errorLog(location, storage_left)

def main():
    path = "C:"
    filename = 'disk_usage.csv' 
    loc = '' 
    maxLog = 60

    AvailabelStorageLog(path, filename, loc, maxLog)

if __name__ == "__main__":
    main()