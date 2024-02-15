'''
MES Bad Emails Compiler
Daniel Olevsky
'''

# access file system
from pathlib import Path
# create excel file type
from pandas import DataFrame

def readFiles(folder, key):
    '''
    Record the next line after the first occurence of the key in each .bad file in the selected folder
    Intended to log all unique "bad emails" (no duplicates)

    Average Case: O(n*log(m))
    Worst Case: O(n*m)
    n : number of files in folder
    m : number of lines in each file

    Input:
    folder : path to open files from
    key : phrase consistant for all files to locate bad email

    Output:
    set of bad emails 
    '''

    # no duplicates + cut down run time
    emailSet = set(())

    # list all files in folder
    files = Path(folder).glob('*') 

    if not files:
        raise ValueError("No files in folder selected or folder doesn't exist")

    # for each file in folder
    for filename in files:
        # check file type
        if filename.suffix == '.BAD':
            # open and read file as list of lines
            file = open(filename, "r")
            text = file.readlines()

            # for each line in text
            for x in range(len(text)):
                # check line for key
                # if key found in file
                if key in text[x]:
                    try:
                        # add formatted email to set
                        emailSet.add(text[x + 2].replace(" ", ""))
                        # end current file search
                        break 
                    # key found on last line of page somehow
                    except IndexError:
                        pass
                    break
                
        else:
            # wrong file type
            raise TypeError("A file with a format other than '.bad' was selected")

    return emailSet


def printToExcel(inSet, name):
    '''
    Write each item in set to excel file
    Will not overrite existing files

    Input:
    emailSet : set of bad emails
    name : name of create excel file

    Output:
    if completed excel file: true, else: false
    '''

    try: 
        # create data frame with items of function input
        df = DataFrame(list(inSet))
        # create excel file from data frame
        df.to_excel(name, index=False)
    except:
        return False

    return True
    

if __name__=="__main__": 
    badEmails = readFiles("Bad Emails", 'Delivery to the following recipients failed.')
    # print(badEmails) # TESTING
    print(printToExcel(badEmails, 'MES_Bad_Emails.xlsx'))
