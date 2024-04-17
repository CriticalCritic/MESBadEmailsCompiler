'''
Available Storage Log
Creates or updates a CSV file with the remaining storage on the computer and time
Meant to be run with a program such as TaskScheduler to track disk usage
Best Case: O(n), Average Case: O(log(m))
Daniel Olevsky
'''

from shutil import disk_usage
import datetime
import socket
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
    storage_left : Available space on machine in each drive at time of error
    '''
    # Get the time and trim to 3 milliseconds
    errorTime = datetime.datetime.now().strftime('%Y-%m-%d %H.%M.%S.%f')[:-3] + '.txt'
    # Create unique file
    errorFile = open(str(location) + 'Error_' + errorTime, 'w')
    # Log error occurence
    errorFile.write('Error at ' + str(errorTime) + ' with ' + str(storage_left) + '\nMake sure csv file is closed')

def AvailabelStorageLog(location, maxLog):
    '''
    Create or update a CSV file with an entry of the current available storage and time

    Input:
    location : location of CSV file to make/modify and possible new error files; must end with '\\' unless blank
    maxLog : max number of entries to be kept; oldest deleted first
    '''
    # File name starts with device name
    filename = str(socket.gethostname()) + '_disk_usage.csv'
    fields = ['Time M/D/Y']
    file = location + filename

    # Identify hardware disks
    # In ASCII, 65 == 'A' and 91 == 'Z'
    # Excludes network drives by not checking past 'I' (73)
    drives = [chr(x) + ":" for x in range(65,73) if exists(chr(x) + ":")]

    # Get the time and trim to nearest minute
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

    data = {str(fields[0]): time}

    # Storage for each available disk
    for x in drives:
        # Add drive to output format
        fields.append(x + ' (GB) Free/Total')

        disk_space = disk_usage(x)

        # Store the storage left for given drive in GB rounded to two decimal places
        data[fields[-1]] = str(round(disk_space.free / (1024.0 ** 3), 2)) + ' / ' + str(round(disk_space.total / (1024.0 ** 3), 2))

    try:        
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
        errorLog(location, data)

# def main():
#     loc = ''
#     maxLog = 60

#     AvailabelStorageLog(path, filename, loc, maxLog)

# if __name__ == "__main__":
#     main()
        
AvailabelStorageLog('', 60)