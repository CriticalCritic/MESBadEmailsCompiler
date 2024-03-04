import pandas as pd

file1 = 'UsersList.xlsx'
file2 = 'WhosWho.xlsx'

# create data frames from excel
df1 = pd.read_excel(file1, usecols='C')
df2 = pd.read_excel(file2, usecols='A')

# easier to use (?)
dfx = df1.apply(tuple)
dfy = df2.apply(tuple)

# relative complement of users on whoswho 
difference = list(set(dfx[' Last Name']).difference(dfy['Last']))
# difference = pd.concat([dfx[' Last Name'], dfy['Last']]).drop_duplicates(keep=False, inplace=False).reset_index()

# create data frame with items of function input
df = pd.DataFrame(difference)

# create excel file from data frame
df.to_excel('RelativeComplement.xlsx', index=False)
