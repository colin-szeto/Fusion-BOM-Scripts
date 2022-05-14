import pandas as pd

# reformatting the default csv output from fusion to isolate neccessary information
df = pd.read_csv('prototype frame.csv')
df = df.drop(['Unnamed: 3','Unnamed: 4'], axis=1)
df = df.rename(columns={"PARTS LIST": "ITEM", "Unnamed: 1": "QTY", "Unnamed: 2": "PART NUMBER"})
df = df.iloc[1: , :]
max_value = df['ITEM'].max()

# seperating keys by delimieter to make it useful
def first_value(a,b, numb_len):
    try: 
        if b > numb_len:
            return 0
        else:
            return a.split('.')[b]
    except:
        return 0

def max_length(a): 
    return len(a.split('.'))
    
df['NUMB_LEN'] = df['ITEM'].apply(max_length)
max_length_value = df['NUMB_LEN'].max() 

# stores values of keys in own colums
added_columns_item = []
added_columns_match = []
for i in range(0,max_length_value):
    item = 'ITEM_{}'.format(i)
    match = 'MATCH_{}'.format(i)
    df[item] = df.apply(lambda x: first_value(x['ITEM'], i, x['NUMB_LEN']), axis = 1)
    df[match] = df[item].eq(df[item].shift())
    added_columns_item.append(item)
    added_columns_match.append(match)

# determines how many numbers in the key match up to previous row. Helps differentiate between components and sub assembilies
df['numb_match'] = [0] *len(df)
for i in range(3, len(df)-2):
    for b in range(0,max_length_value-1):
        match = 'MATCH_{}'.format(b)
        if df.loc[i-1, match] != False: # it is true
            df.loc[i, 'numb_match'] = df.loc[i, 'numb_match'] + 1
        else: 
            break

# hacky bit of the code to make differentiating components correct
df['numb_match'] = df['numb_match'].shift(-1)

# determining what are components of a sub assembly to multiply
for i in range(2, len(df)+1):
    b = 1
    while df.loc[i, 'numb_match'] == df.loc[i-b, 'numb_match']:
        df.loc[i, 'T_QTY'] = df.loc[i, 'QTY']
        b = b + 1
    try:
        value = df.loc[i, 'QTY']
        multipler = df.loc[i-b, 'QTY']
        df.loc[i, 'T_QTY'] =  int(value)*int(multipler) 
    except:
        df.loc[i, 'T_QTY'] = 'didnt work: {}'.format(df.loc[i-b, 'QTY'])

#order = ["ITEM", "QTY", 'T_QTY', "PART NUMBER"] + added_columns_item + added_columns_match + ['numb_match']
order = ["ITEM", "QTY", 'T_QTY', "PART NUMBER"]
df = df.reindex(columns= order)

# to isolate the part numbers and differentiates what are brackets and what are custom named components
def rename(partNumb):
    partNumbLen = len(partNumb)
    if partNumbLen < 20:
        try:
            # if the first 4 values are numbers then append the part number
            test_if_numb = int(partNumb[0:4])
            return partNumb[0:4]
        except: 
            return
    else:
        onlyNumb = partNumb[0:9]
        if partNumb[9] == '_' or partNumb[8] == '_':
            onlyNumb = onlyNumb.replace("_", "")
            return onlyNumb

df['PART NUMBER'] = df.apply(lambda x: rename(x['PART NUMBER']), axis = 1)
df = df.dropna()
df = df.groupby("PART NUMBER").sum()


order = ['T_QTY']
df = df.reindex(columns= order)

print(df.to_string()) 
print("max value is: {}".format(max_value))
print("max number length is: {}".format(max_length_value))

df.to_csv('out.csv')  
