import pandas as pd

df = pd.read_csv('prototype frame.csv')
df = df.drop(['Unnamed: 3','Unnamed: 4'], axis=1)
df = df.rename(columns={"PARTS LIST": "ITEM", "Unnamed: 1": "QTY", "Unnamed: 2": "PART NUMBER"})
df = df.iloc[1: , :]
max_value = df['ITEM'].max()

def first_value(a,b, numb_len):
    try: 
        if b > numb_len:
            return 0
        else:
            return a.split('.')[b]
    except:
        return 0
    
#def check_matching(current, previous):
#    if previous == :
#        return 
#    if current == previous:
#        return True

def max_length(a): 
    return len(a.split('.'))
    
df['NUMB_LEN'] = df['ITEM'].apply(max_length)
max_length_value = df['NUMB_LEN'].max() 

added_columns_item = []
added_columns_match = []
for i in range(0,max_length_value):
    item = 'ITEM_{}'.format(i)
    match = 'MATCH_{}'.format(i)
    df[item] = df.apply(lambda x: first_value(x['ITEM'], i, x['NUMB_LEN']), axis = 1)
    df[match] = df[item].eq(df[item].shift())
    #df['MATCH_{}'.format(i)] = df.apply(lambda x: check_matching(x[item], x[item]), axis = 1)
    added_columns_item.append(item)
    added_columns_match.append(match)

# proves how one can apply itteration and condintonal logic to determine what rows is multipled by what
# need to figure out how to only multiple numbers that have percurose number mathcing (multiplying the quanities of the parts by the number of instances the assembly appears)
df['total_quanity'] = [None] *len(df)
for i in range(3, len(df)-3):
    for b in range(0,max_length_value):
        match = 'MATCH_{}'.format(b)
        if df.loc[i-1, match] != False:
            df.loc[i, 'total_quanity'] = int(df.loc[i-1, 'QTY']) * int(df.loc[i, 'QTY'])

    
    
order = ["ITEM", "QTY", 'total_quanity', "PART NUMBER"] + added_columns_item + added_columns_match
df = df.reindex(columns= order)


print(df.to_string()) 
print("max value is: {}".format(max_value))
print("max number length is: {}".format(max_length_value))
