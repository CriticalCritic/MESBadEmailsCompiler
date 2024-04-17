'''
Available Storage Log
Creates or updates a table in a SQL database with the remaing/total storage on the computer and time
Meant to be run with a program such as TaskScheduler to track disk usage
Daniel Olevsky
'''

# Requires following comment to be run from cmd line
# pip install pyobc

from shutil import disk_usage
from os.path import exists
import datetime
import socket
import pyodbc 

# Python Module with log in information
import loginfo

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
    errorFile.write('Error occured at ' + str(errorTime) + ' with ' + str(storage_left))

def AvailabelStorageLog(location, maxLog):
    '''
    Create or update a SQL Database Table with an entry of the current available storage and time

    Input:
    location : location for possible new error files; must end with '\\' unless blank
    maxLog : max number of entries to be kept; oldest deleted first
    '''
    dbName = 'Server_Disk_Usage'
    
    # Table name starts with device name
    tableName = str(socket.gethostname()) + '_disk_usage'
    fields = ["Time_M/D/Y"]

    # Identify hardware disks
    # In ASCII, 65 == 'A' and 91 == 'Z'
    # Excludes network drives by not checking past 'I' (73)
    drives = [chr(x) + ":" for x in range(65,73) if exists(chr(x) + ":")]

    # Get the time and trim to nearest minute
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

    data = [time]

    # Storage for each available disk
    for x in drives:
        # Add drive to output format
        fields.append(x + "_(GB)_Free/Total")

        disk_space = disk_usage(x)

        # Store the storage left for given drive in GB rounded to two decimal places
        data.append(str(round(disk_space.free / (1024.0 ** 3), 2)) + " / " + str(round(disk_space.total / (1024.0 ** 3), 2)))

    try:
        # Connect to SQL server
        connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};DATABASE={dbName};SERVER={loginfo.serverIP};UID={loginfo.userName};PWD={loginfo.paswrd};'
        mydb = pyodbc.connect(connectionString) 
        mycursor = mydb.cursor()

        # Using T-SQL

        # Format column names
        columns = ""
        for x in fields:
            columns += ("\"" + x + "\" varchar(255), ")

        # Create table corresponding to device if not exists
        mycursor.execute(f"IF NOT EXISTS(SELECT TABLE_NAME FROM {dbName}.INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME='{tableName}') BEGIN CREATE TABLE {tableName} ({columns}) END")
        mydb.commit()

        # Format adding operation
        addFields = ""
        for x in fields:
            addFields += ("\"" + x + "\", ")
        addFields = addFields[0:-2]

        addData = ""
        for x in data:
            addData += ("\'" + x + "\', ")
        addData = addData[0:-2]
        
        # Add data
        mycursor.execute(f"INSERT INTO {tableName} ({addFields}) VALUES ({addData})")
        mydb.commit()

        # If more entries than allowed, delete rows from oldest
        tempTableName = "tempSort"
        sortKey = "\"" + fields[0] + "\""

        # Make temp table to sort oldest entries over the log limit in original log
        # Remove entries from original log that are >= newset entry in temp table
        sql_Delete = f"""IF (SELECT count(*) FROM {tableName}) > {maxLog} BEGIN 

                            CREATE TABLE {tempTableName} ({sortKey} varchar(255)); 

                            INSERT {tempTableName} ({sortKey}) SELECT TOP ((SELECT count(*) FROM {tableName}) - {maxLog}) {sortKey} FROM {tableName} ORDER BY {sortKey} ASC;

                            DELETE FROM {tableName} WHERE {sortKey} <= (SELECT TOP 1 * FROM {tempTableName} ORDER BY {sortKey} DESC)

                            DROP TABLE {tempTableName};
                                
                        END"""
        
        mycursor.execute(sql_Delete)
        mydb.commit()

        # Display table
        mycursor.execute(f"SELECT * FROM {tableName} ORDER BY \"{fields[0]}\" DESC")

        # print(mycursor.fetchall())

        # Close connection
        mycursor.close()
        mydb.close()

    except:
        # Create error file
        errorLog(location, data)

# def main():
#     loc = ''
#     maxLog = 60

#     AvailabelStorageLog(loc, maxLog)

# if __name__ == "__main__":
#     main()
        
AvailabelStorageLog('', 60)