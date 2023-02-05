# Put task1a.py code here
import csv
import pandas as pd
import numpy
from pandas import DataFrame


csv_buy_small = pd.read_csv("buy_small.csv", encoding='ISO-8859-1')
csv_abt_small = pd.read_csv("abt_small.csv", encoding='ISO-8859-1')   
    
# convert dataframe into two lists
df_abt = pd.DataFrame(csv_abt_small, columns= ['idABT', 'name'])
abt_list = df_abt.values.tolist()
df_buy = pd.DataFrame(csv_buy_small, columns= ['idBuy', 'name'])
buy_list = df_buy.values.tolist()

punctuation = "!()-[]{};:'\,<>/?@#$%^&*_~"


# split the names in both lists and make them in lower cases, remove punctuations.
name_n_idbuy = []
for i in buy_list:   
    word_list = []
    split_word = i[1].split(" ")
    for j in split_word:
        # change all the words in lower case.
        lower_case = j.lower()
        if len(lower_case) > 1:
            # remove the punctuation of each words.
            no_punct = ''.join(char for char in lower_case if char not in punctuation)
        else:
            no_punct = lower_case
        word_list.append(no_punct)  
    name_n_idbuy.append([i[0], word_list])
name_n_idabt = []
for i in abt_list:   
    word_list = []
    split_word = i[1].split(" ")
    for j in split_word:
        lower_case = j.lower()
        if len(lower_case) > 1:
            no_punct = ''.join(char for char in lower_case if char not in punctuation)
        else:
            no_punct = lower_case
        word_list.append(no_punct)  
    name_n_idabt.append([i[0], word_list])
    

matching_final = []
suffix = []

# first step, matching the suffix from both csv.
for i in range(len(name_n_idabt)):
    # assume suffix is the last word of name and it occurs after '-'
    if name_n_idabt[i][1][-1] not in suffix and name_n_idabt[i][1][-2] == '-':
        suffix.append(name_n_idabt[i][1][-1])

        
for i in range(len(name_n_idbuy)):
    if name_n_idbuy[i][1][-1] not in suffix and name_n_idbuy[i][1][-2] == '-':
        suffix.append(name_n_idbuy[i][1][-1])

    
# try matching by suffix.
for i in suffix:
    match = 0
    for j in name_n_idabt:
        if i in j[1]:
            match += 1
            id_abt = j[0]
            break
    for k in name_n_idbuy:
        if i in k[1]:
            match += 1
            id_buy = k[0]
            break
        
    # make sure the suffix appears in both of the name (in different csv).
    if match == 2:
        matching_final.append([id_abt, id_buy])   
        
        
# get rid of repeated ids in both idabt and idbuy.
index_list = []
for i in range(len(matching_final)):
    for j in range(len(matching_final)):
        if matching_final[i][1] == matching_final[j][1] and i < j:
            index_list.append(j)
        if matching_final[i][0] == matching_final[j][0] and i < j:
            index_list.append(j)
            
for i in range(len(index_list)):
    if i == 0:
        removing = index_list[i]
        matching_final.pop(removing)
    else:
        removing = index_list[i] - i
        matching_final.pop(removing)
        
# get rid of already matching names and ids.
for i in matching_final:
    for j in name_n_idbuy:
        if i[1] == j[0]:
            name_n_idbuy.remove(j)
            
for i in matching_final:
    for j in name_n_idabt:
        if i[0] == j[0]:
            name_n_idabt.remove(j)         

    
# try to do matching of names by counting the number of similar words.
matching_1 = []
# idbuy list
for i in name_n_idbuy:
    most_similar = 0
    # idabt list
    for j in name_n_idabt:
        similarity = 0
        # element in name of idbuy
        
        for k in range(1, len(i[1])):
            if i[1][k] in j[1] and i[1][k-1] in j[1]:
                # number of similar words between two names.
                similarity += 1
                
        # choose the most number of similar words as the matching pairs.
        if similarity > most_similar:
            most_similar = similarity
            matching_id = j[0]
            
    # assume the number of similiar words not less than 3.
    if most_similar < 1:
        None
    else:
        matching_1.append([matching_id, i[0]]) 
        
# exact the same method, just do it other way round to improve accuracy.
matching_2 = []
for i in name_n_idabt:
    most_similar = 0
    # idabt list
    for j in name_n_idbuy:
        similarity = 0
        # element in name of idbuy
        
        for k in range(1, len(i[1])):
            if i[1][k] in j[1] and i[1][k-1] in j[1]:
                # number of similar words between two names.
                similarity += 1
                
        # choose the most number of similar words as the matching pairs.
        if similarity > most_similar:
            most_similar = similarity
            matching_id = j[0]
            
    # assume the number of similiar words not less than 3.
    if most_similar < 1:
        None
    else:
        matching_2.append([i[0], matching_id])            
                
             
# see if the matching ids also appears in the other matching list.        
for i in matching_1:
    if i in matching_2:
        matching_final.append(i)
          
for i in matching_2:
    if i in matching_1 and i not in matching_final:
        matching_final.append(i)     
   
with open('task1a.csv', 'w', newline = '') as f:
    writer = csv.writer(f)
    writer.writerow(['idabt', 'idbuy'])
    for i in matching_final:
        writer.writerow(i)