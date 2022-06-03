import os
import re
import csv

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

def document_frequency(path):
    file = load_data_as_dict(path)

    list_tokens = []
    for line in file:
        tokens = re.findall(r"[íéêóáú]*[ÁÉÊÍÓÚ]*[A-Za-z]+[-’'íéêáóúñ]*[ÁÉÍêÓÚ]*[A-Za-z]*[-’'íéêáóú]*[A-Za-z]*", line.lower())
        uniques = list(set(tokens))
        list_tokens.extend(uniques)


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
    path = 'files/tetun.txt'

    tf = term_frequency(path)
    print(len(tf))
    print(tf)

    df = document_frequency(path)
    print(len(df))
    print(df)

    df = document_frequency(path)
    print(len(df))
    print(df)

    print(df.keys())

    vocabulary = build_vocabulary(path)

    print(len(vocabulary))

    file = open('files/nodes.csv', "w", encoding="utf8")
    delimiter = ","
    newline = '\n'
    file.writelines("id" + delimiter + "Label"+ delimiter + "tf" + delimiter + "df" + delimiter + "tdf" + newline)

    ids = {}
    for index, term in enumerate(df.keys()):
        ids[term] = index
        file.writelines(str(index) + delimiter + term + delimiter + str(tf[term]) + delimiter + str(df[term]) + delimiter + str(tf[term]*df[term]) + newline)
        print("{term} {tf} {df} {tdf}".format(term=term, tf=tf[term], df=df[term], tdf=tf[term]*df[term]))

    print(ids)

    out = ["Source, Target, Type, Weight"]
    with open('files/edges.csv', 'r', encoding="utf8") as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        for row in reader:
            # print(row)
            # print(str(ids[row[0].strip()]) + ', '+str(ids[row[1].strip()]))
            out.append(str(ids[row[0].strip()]) + ', '+str(ids[row[1].strip()])+', Directed, 1.0')

    file2 = open("files/edges-gephi.csv", "w", encoding="utf8")
    file2.writelines("\n".join(out))
    file2.close()

    # for id in ids.keys():
    #     print(id+" -- id: "+str(ids[id]) )