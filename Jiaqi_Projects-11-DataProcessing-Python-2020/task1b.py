# Put task1b.py code here
import csv
import pandas as pd
import time
import numpy
from sklearn import neighbors
from sklearn import preprocessing
from sklearn.tree import DecisionTreeClassifier
from pandas import DataFrame
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier


csv_buy_small = pd.read_csv("buy.csv", encoding='ISO-8859-1')
csv_abt_small = pd.read_csv("abt.csv", encoding='ISO-8859-1')   

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
    
    
# first step, matching the suffix from both csv.
matching_final = []
suffix = []
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
        matching_final.append([id_abt, id_buy, i])   
        
        
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
            
            
# Second step, getting the prefix of both csv names.
prefix = []
for i in name_n_idbuy:
    if i[1][0] in prefix or i[1][0] == 'the' or i[1][0] == 'a' or i[1][0] == 'an':
        None
    elif i[1][0] == 'the' and i[1][1] not in prefix:
        prefix.append(i[1][1])
    else:
        prefix.append(i[1][0])
        
for i in name_n_idabt:
    if i[1][0] in prefix or i[1][0] == 'the' or i[1][0] == 'a' or i[1][0] == 'an':
        None
    elif (i[1][0] == 'the' or i[1][0] == 'a' or i[1][0] == 'an') and i[1][1] not in prefix:
        prefix.append(i[1][1])
    else:
        prefix.append(i[1][0])        
        
        
# classify the names with the same prefix because I assume the prefix is the brand name.
classification_by_prefix = []
for i in prefix:
    name_contain_prefix_1 = []
    name_contain_prefix_2 = []
    for j in name_n_idbuy:
        if i in j[1]:
            name_contain_prefix_1.append(j)
    for k in name_n_idabt:
        if i in k[1]:
            name_contain_prefix_2.append(k)
    classification_by_prefix.append([i, name_contain_prefix_1, 
name_contain_prefix_2])       
    
     
# try to do matching of names by counting how many words are similar inside each brand groups "classification_by_prefix".
for i in classification_by_prefix:
    # loop idbuy list
    for j in i[1]:
        most_similar = 0
        # loop idabt list
        for k in i[2]:
            similarity = 0
            # loop element in name of idbuy
            for m in j[1]:
                if m in k[1]:   
                    # number of similar words between two names.
                    similarity += 1
            # choose the most number of similar words as the matching pairs.
            if similarity > most_similar:
                most_similar = similarity
                matching_id = k[0]
        # assume the number of similiar words not less than 3.
        if most_similar < 1:
            None
        else:
            matching_final.append([matching_id, j[0], i[0]])
            
            
# exact the same method, just do it other way round to improve accuracy.
for i in classification_by_prefix:
    # loop idabt list
    for j in i[2]:
        most_similar = 0
        # loop idbuy list
        for k in i[1]:
            similarity = 0
            # loop element in name of idabt
            for m in j[1]:
                if m in k[1]:
                    similarity += 1
            if similarity > most_similar:
                most_similar = similarity
                matching_id = k[0]
        if most_similar < 1:
            None
        else:
            matching_final.append([j[0], matching_id, i[0]])             
                
with open('abt_blocks.csv', 'w', newline = '') as f:
    writer = csv.writer(f)
    writer.writerow(['block_key', 'product_id'])
    for i in matching_final:
        writer.writerow((i[2], i[0]))
        
with open('buy_blocks.csv', 'w', newline = '') as f:
    writer = csv.writer(f)
    writer.writerow(['block_key', 'product_id'])
    for i in matching_final:
        writer.writerow((i[2], i[1]))        
        
        
