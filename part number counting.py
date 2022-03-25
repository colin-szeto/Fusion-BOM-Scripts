import csv
import pandas as pd
name_to_read = '8.csv'
name_to_export = '8.1.csv'
with open(name_to_read) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    partNumbDict = []
    partNumbList = []
    
    for row in csv_reader:
        if line_count < 2:
            #skip the parts list and items list row
            line_count += 1
        else:
            partNumb = row[2]
            qty = row[1]
            partNumbLen = len(partNumb)
            if partNumbLen < 20:
                try:
                    # if the first 4 values are numbers then append the part number
                    test_if_numb = int(partNumb[0:4])
                    partNumbDict.append({partNumb[0:4]:qty})
                    partNumbList.append(partNumb[0:4])
                    print('8020 part: {}'.format(partNumb[0:4]))
                except:
                    # this means that this not a part number, appends the whole name
                    sep = '('
                    partNumb = partNumb.split(sep, 1)[0]
                    partNumbDict.append({partNumb:qty})
                    partNumbList.append(partNumb)
                    print('Named Part: {}'.format(partNumb))
            else:
                onlyNumb = partNumb[0:9]
                if partNumb[9] == '_' or partNumb[8] == '_':
                    print('is a McMaster part number: {}'.format(onlyNumb))
                    partNumbDict.append({onlyNumb:qty})
                    partNumbList.append(onlyNumb)
                else:
                    sep = '('
                    partNumb = partNumb.split(sep, 1)[0]
                    print('not a McMaster part number: {}'.format(partNumb))
                    partNumbDict.append({partNumb:qty})
                    partNumbList.append(partNumb)
 
            line_count += 1
            
    print(f'Processed {line_count} lines.')
    print(partNumbDict)
    print("")
    print(partNumbList)
        
    final = {}.fromkeys(partNumbList, 0)  
    for dict in partNumbDict:
        for key,value in dict.items():
            final[key] = int(final[key]) + int(value)

    full = []
    full.append(['QTY','Name'])
    for key, val in final.items():
        res = []
        res.append(val)
        res.append(key)
        full.append(res)

    full.pop(1) #removing the assembly name
    df = pd.DataFrame(full)
    df.to_csv(name_to_export)

