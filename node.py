import os
import re
# import numpy as np
# import pandas as pd
# from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer


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

def count_freq(term, tokens):
    tokens = sorted(tokens)
    sum = 0
    for index, t in enumerate(tokens):
        if t == term:
            sum+=1
            if tokens[index + 1] != t:
                break
    return sum

def build_vocabulary(data):
    tokens = tetun_tokenizer(data)
    vocabulary = list(sorted(set(tokens)))
    return vocabulary

# number of ocurrency
def term_frequency(path):
    tokens = sorted(tetun_tokenizer(path))
    tf = {}
    top = tokens.pop()
    count = 0
    while len(tokens) > 0:
        current = tokens.pop()
        if current == top:
            count += 1
        else:
            tf[top] = count+1
            count = 0
            top = current
    tf[top] = count + 1
    return tf

#number of text occur
def document_frequency(path):
    file = load_data_as_dict(path)
    vocabulary = build_vocabulary(path)

    df = {}
    for term in vocabulary:
        sum = 0
        for line in file:
            tokens = re.findall(r"[íéêóáú]*[ÁÉÊÍÓÚ]*[A-Za-z]+[-’'íéêáóúñ]*[ÁÉÍêÓÚ]*[A-Za-z]*[-’'íéêáóú]*[A-Za-z]*",line.lower())
            if term in tokens:
                sum += 1


        df[term] = sum
    return df


if __name__ == '__main__':
    path = 'files/tetun.txt'

    tf = term_frequency(path)
    print(len(tf))
    print(tf)

    df = document_frequency(path)
    print(len(df))
    print(df)

    vocabulary = build_vocabulary(path)

    file = open('files/nodes.csv', "w", encoding="utf8")
    delimiter = ";"
    newline = '\n'
    file.writelines("id" + delimiter + "tf" + delimiter + "df" + delimiter + "tdf" + newline)

    for term in vocabulary:
        file.writelines(term + delimiter + str(tf[term]) + delimiter + str(df[term]) + delimiter + str(tf[term]*df[term]) + newline)
        print("{term} {tf} {df} {tdf}".format(term=term, tf=tf[term], df=df[term], tdf=tf[term]*df[term]))