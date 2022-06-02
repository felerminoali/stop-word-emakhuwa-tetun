import os
import re
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer


def load_data_as_dict(path):
    lines = []
    with open(path, "r", encoding="utf8") as file:
        lines = file.readlines()
    return lines

# function to load data
def load_data(file_path):
  with open(file_path, 'r', encoding="utf8") as f:
    data = f.read()
  return data

# lowercasing and tokenize
def tetun_tokenizer(data_source):
    data = load_data(data_source)
    lower_data = data.lower() #lowercase the corpus
    tokens = re.findall(r"[íéêóáú]*[ÁÉÊÍÓÚ]*[A-Za-z]+[-’'íéêáóúñ]*[ÁÉÍêÓÚ]*[A-Za-z]*[-’'íéêáóú]*[A-Za-z]*", lower_data)
    return tokens

def tetun_tokenizer_data(data):
    lower_data = data.lower() #lowercase the corpus
    tokens = re.findall(r"[íéêóáú]*[ÁÉÊÍÓÚ]*[A-Za-z]+[-’'íéêáóúñ]*[ÁÉÍêÓÚ]*[A-Za-z]*[-’'íéêáóú]*[A-Za-z]*", lower_data)
    return tokens

def count_freq(data, term):
    tokens = tetun_tokenizer_data(data)
    sum = 0
    for t in tokens:
        if t == term:
            sum+=1
    return sum

def build_vocabulary(data):
    tokens = tetun_tokenizer(data)
    vocabulary = list(sorted(set(tokens)))
    return vocabulary

# number of ocurrency
def term_frequency(path):
    data = load_data(path)
    data.lower()
    tf = {}
    vocabulary = build_vocabulary(path)
    for term in vocabulary:
        count = count_freq(data, term)
        tf[term] = count
    return tf

#number of text occur
def document_frequency(path):
    file = load_data_as_dict(path)
    vocabulary = build_vocabulary(path)

    df = {}
    for term in vocabulary:
        sum = 0
        for line in file:
            line = line.lower()
            if term in line:
                sum += 1
        df[term] = sum
    return df


if __name__ == '__main__':
    path = 'files/tetun.txt'



    docs = [load_data("files/tetun.txt")]

    cv = CountVectorizer()
    term_cv = cv.fit_transform(docs)
    term = np.array(cv.get_feature_names())
    term_freq = term_cv.toarray().sum(axis=0)
    tf = dict(zip(term, term_freq))
    print(tf['a'])
    #dict_tf = dict(sorted(tf.items(), key=lambda x: x[1], reverse=True))
    #df_tf = pd.DataFrame.from_dict(dict_tf, orient='index', columns=["tf"])[:10]

    df = document_frequency(path)
    print(len(df))
    print(df)

    vocabulary = build_vocabulary(path)

    file = open('files/nodes.csv', "w")
    delimiter = ";"
    newline = '\n'
    file.writelines("id" + delimiter + "tf" + delimiter + "df" + delimiter + "tdf" + newline)

    #for term in vocabulary:
        #file.writelines(term + delimiter + str(tf[term]) + delimiter + str(df[term]) + delimiter + str(tf[term]*df[term]) + newline)
        #print("{term} {df} {tf}".format(term=term, df=df[term], tf=tf[term]))
        #file.writelines(term + delimiter + "a" + delimiter + "x" + delimiter + "y" + newline)
