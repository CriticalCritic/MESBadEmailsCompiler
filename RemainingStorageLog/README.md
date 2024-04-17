# Device Storage Log SQL Server Version

## Summary

(ONLY PYTHON CODE / QUOTED QUERIES PART)

Creates/updates a table on a connected SQL Server database corresponding to the device

The table on the given database keeps track of the remaining storage and total storage of the current device with time stamps when taken

Errors are recorded on device running program in text files that can be added manually to table and/or deleted 


Can be hooked up to task scheduler to create a scheduled record 


## How to run

Requires python to be installed


Requires the following command to be run in the terminal ONCE so the program can connect to SQL server:

```
    pip install pyodbc
```

Afterward, the file "AvailableStorageLog_SQLServer.py" can be run at any time