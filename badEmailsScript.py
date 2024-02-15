'''
MES Bad Emails Compiler
Daniel Olevsky
'''

# access file system
from pathlib import Path
# create excel file type
from pandas import DataFrame

def readFiles(folder):
    '''
    Record unique (no duplicates) bad emails, their # of occurences, and their unique subject lines along with thier # of occurences for all .bad file in the selected folder

    Average Case: O(n*log(m))
    Worst Case: O(n*m)
    n : number of files in folder
    m : number of lines in each file

    Input:
    folder : path to open files from

    Output:
    Dictionary of bad emails and # of occurences
    '''

    # no duplicates + cut down run time
    emailDict = {}

    # list all files in folder
    files = Path(folder).glob('*') 

    # no files or folder
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
                if 'This is an automatically generated Delivery Status Notification.' in text[x]:
                    # locate email from remaining text
                    for i in range(len(text) - x):
                        # emial found in line
                        if '@' in text[x + i]:
                            # add formatted email to dict
                            if text[x + i].replace(" ", "") in emailDict:
                                emailDict[text[x + i].replace(" ", "")][0] += 1
                            else:
                                emailDict[text[x + i].replace(" ", "")] = [1, {}]
                            
                            # locate subject from remaining text
                            for n in range(len(text) - x - i):
                                if 'Subject:' in text[x + i + n]:
                                    # if subject already associated with email
                                    if text[x + i + n] in emailDict[text[x + i].replace(" ", "")][1]:
                                        emailDict[text[x + i].replace(" ", "")][1][text[x + i + n]] += 1
                                    else: 
                                        emailDict[text[x + i].replace(" ", "")][1][text[x + i + n]] = 1
                            break

                        # record associated message
                        else:
                            pass

                    break
                
        else:
            # wrong file type
            raise TypeError("A file with a format other than '.bad' was selected")

    return emailDict


def printToExcel(inDict, name):
    '''
    Write each item in Disctionary to excel file
    Will not overrite existing files

    Input:
    emailSet : set of bad emails
    name : name of create excel file

    Output:
    if completed excel file: true, else: false
    '''

    #format data
    data = {"Emails":[], "Count":[], "Subjects":[]}
    for x in inDict:
        # sort into catagories
        data["Emails"].append(x)
        data["Count"].append(inDict[x][0])
        data["Subjects"].append(inDict[x][1])

    try: 
        # create data frame with items of function input
        df = DataFrame(data)
        # create excel file from data frame
        df.to_excel(name, index=False)
    except:
        return False

    return True
    

if __name__=="__main__": 
    badEmails = readFiles("Bad Emails")
    # print(badEmails) # TESTING
    print(printToExcel(badEmails, 'MES_Bad_Emails.xlsx'))
