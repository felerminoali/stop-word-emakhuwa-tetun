from nltk import ngrams
import re


# function to load data
def load_data(file_path):
  with open(file_path, 'r') as f:
    data = f.read()

  return data


# lowercasing and tokenize
def tetun_tokenizer(data_source):
    data = load_data(data_source)
    lower_data = data.lower() #lowercase the corpus
    tokens = re.findall(r"[íéêóáú]*[ÁÉÊÍÓÚ]*[A-Za-z]+[-’'íéêáóúñ]*[ÁÉÍêÓÚ]*[A-Za-z]*[-’'íéêáóú]*[A-Za-z]*", lower_data)

    return tokens


# function to generate edges using 2 grams as default value
def generate_edges(file, data_source, n=2, delimiter=" ", newline="\n", weight=1):
    tokens = tetun_tokenizer(data_source)
    two_grams = list(ngrams(tokens, 2))

    file = open(file, "w")
    for two_gram in two_grams:
        gram_1, gram_2 = two_gram
        
        if gram_1[-1] == "-":
            gram_1 = gram_1[:-1] #remove "-" if it is the last char of word
        
        if gram_2[-1] == "-":
            gram_2 = gram_2[:-1] #remove "-" if it is the last char of word

        file.writelines(gram_1 + delimiter + gram_2 + delimiter + str(weight) + newline)
    file.close()

# generate the file for edges
generate_edges("files/edges.txt", "files/tetun.txt")