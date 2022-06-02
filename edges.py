from nltk import ngrams
import re


# function to load data
def load_data(file_path):
  with open(file_path, 'r') as f:
    data = f.read()

  return data


# function to generate edges using 2 grams as default value
def generate_edges(file, data_source, n=2, delimiter=" ", newline="\n", weight=1):
    data = load_data(data_source)
    tokens = re.findall(r"[íéóáú]*[ÁÉÍÓÚ]*[A-Za-z0-9]+[-’'íéáóúñ]*[ÁÉÍÓÚ]*[A-Za-z0-9]*[-’'íéáóú]*[a-z0-9]*", data) 
    two_grams = list(ngrams(tokens, 2))

    file = open(file, "w")
    for two_gram in two_grams:
        gram_1, gram_2 = two_gram
        file.writelines(gram_1 + delimiter + gram_2 + delimiter + str(weight) + newline)
    file.close()

# generate the file for edges
generate_edges("files/edges.txt", "files/tetun.txt")