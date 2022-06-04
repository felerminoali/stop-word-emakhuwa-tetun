import os
import re
import csv
from nltk.corpus import stopwords

from nltk import tokenize


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
def tetun_tokenizer(data):
    lower_data = data.lower() #lowercase the corpus
    tokens = re.findall(r"[íéêóáú]*[ÁÉÊÍÓÚ]*[A-Za-z]+[-’'íéêáóúñ]*[ÁÉÍêÓÚ]*[A-Za-z]*[-’'íéêáóú]*[A-Za-z]*", lower_data)
    return tokens

def portuguese_tokenizer(data):
    lower_data = data.lower()  # lowercase the corpus
    tokens = [token for token in tokenize.word_tokenize(lower_data, language='portuguese') if token.isalpha()]
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

def tokenize_func(lang, data_source):
    tokens = []
    data = load_data(data_source)
    if lang == 'tetun':
        tokens = tetun_tokenizer(data)
    elif lang == 'portuguese':
        tokens = portuguese_tokenizer(data)
    return tokens

def tokenize_data(lang, data):
    tokens = []
    if lang == 'tetun':
        tokens = tetun_tokenizer(data)
    elif lang == 'portuguese':
        tokens = portuguese_tokenizer(data)
    return tokens

def build_vocabulary(lang, data_path):
    # tokens = tetun_tokenizer(data)
    tokens = tokenize_func(lang, data_path)
    vocabulary = list(sorted(set(tokens)))
    return vocabulary

# number of ocurrency
def term_frequency(lang, data_path):
    # tokens = sorted(tetun_tokenizer(path))
    tokens = sorted(tokenize_func(lang, data_path))
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

def document_frequency(lang, path):
    file = load_data_as_dict(path)

    list_tokens = []
    for line in file:
        tokens = tokenize_data(lang, line)
        uniques = list(set(tokens))
        list_tokens.extend(uniques)

    list_tokens = sorted(list_tokens)
    print(list_tokens)
    df = {}
    top = list_tokens.pop()
    count = 0

    while len(list_tokens) > 0:
        current = list_tokens.pop()
        if current == top:
            count += 1
        else:
            df[top] = count + 1
            count = 0
            top = current
    df[top] = count + 1
    return df

if __name__ == '__main__':
    lang = 'portuguese'
    path = 'files/'+lang+'.txt'

    tf = term_frequency(lang, path)
    print(len(tf))
    print(tf)

    df = document_frequency(lang, path)
    print(len(df))
    print(df)

    vocabulary = build_vocabulary(lang, path)

    print(len(vocabulary))

    file = open('files/nodes-'+lang+'.csv', "w", encoding="utf8")
    delimiter = ","
    newline = '\n'
    file.writelines("id" + delimiter + "Label"+ delimiter + "tf" + delimiter + "df" + delimiter + "tdf" + delimiter +"stopword"+ newline)

    print(stopwords.words('portuguese'))

    stopw = stopwords.words('portuguese') if lang == 'portuguese' else []
    print(len(stopw))

    ids = {}
    for index, term in enumerate(df.keys()):
        ids[term] = index

        is_stop = '1' if term in stopw else '0'
        file.writelines(str(index) + delimiter + term + delimiter + str(tf[term]) + delimiter + str(df[term]) + delimiter + str(tf[term]*df[term]) + delimiter+ is_stop+ newline)
        # print("{term} {tf} {df} {tdf}".format(term=term, tf=tf[term], df=df[term], tdf=tf[term]*df[term]))

    print(ids)

    out = ["Source, Target, Type, Weight"]
    with open('files/edges-'+lang+'.csv', 'r', encoding="utf8") as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        for row in reader:
            print(row)
            # print(str(ids[row[0].strip()]) + ', '+str(ids[row[1].strip()]))
            out.append(str(ids[row[0].strip()]) + ', '+str(ids[row[1].strip()])+', Directed, 1.0')

    file2 = open("files/edges-"+lang+"-gephi.csv", "w", encoding="utf8")
    file2.writelines("\n".join(out))
    file2.close()

