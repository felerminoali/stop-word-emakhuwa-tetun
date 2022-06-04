from nltk import ngrams
from nltk.tokenize import word_tokenize
import re
from nltk import tokenize

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

def portuguese_tokenizer(data_source):
    data = load_data(data_source)
    lower_data = data.lower()  # lowercase the corpus
    tokens = [token for token in tokenize.word_tokenize(lower_data, language='portuguese') if token.isalpha()]
    # print(tokens)
    return tokens

# function to generate edges using 2 grams as default value
def generate_edges(file, data_source, n=2, delimiter=", ", newline="\n"):
    # tokens = tetun_tokenizer(data_source)
    tokens = portuguese_tokenizer(data_source)

    two_grams = list(ngrams(tokens, 2))

    file = open(file, "w", encoding="utf8")
    for two_gram in two_grams:
        gram_1, gram_2 = two_gram
        
        if gram_1[-1] == "-":
            gram_1 = gram_1[:-1] #remove "-" if it is the last char of word

        if gram_2[-1] == "-":
            gram_2 = gram_2[:-1] #remove "-" if it is the last char of word

        file.writelines(gram_1 + delimiter + gram_2 + newline)
    file.close()

# generate the file for edges
lang='portuguese'
generate_edges("files/edges-"+lang+".csv", "files/"+lang+".txt")