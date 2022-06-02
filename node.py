import os
import re
# import pandas as pd

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



    # tf = term_frequency(path)
    # print(len(tf))
    # print(tf)


    df = document_frequency(path)
    print(len(df))
    print(df)

    vocabulary = build_vocabulary(path)

    for term in vocabulary:
        print("{term} {df}".format(term=term, df=df[term]))









