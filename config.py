from nltk import ngrams
from nltk.tokenize import word_tokenize
import re
from nltk import tokenize
from english_words import english_words_lower_set

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

def whitespace_tokenizer(data, lang='portuguese'):
    lower_data = data.lower()  # lowercase the corpus
    tokens = [token for token in tokenize.word_tokenize(lower_data, language=lang) if token.isalpha()]
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
    else:
        tokens = whitespace_tokenizer(data, lang)
    return tokens

def tokenize_data(lang, data):
    tokens = []
    if lang == 'tetun':
        tokens = tetun_tokenizer(data)
    else:
        tokens = whitespace_tokenizer(data)
    return tokens


# function to generate edges using 2 grams as default value
def generate_edges(file, data_source, n=2, delimiter=", ", newline="\n"):

    tokens = tokenize_func(lang, data_source)

    two_grams = list(ngrams(tokens, 2))

    file = open(file, "w", encoding="utf8")
    for two_gram in two_grams:
        gram_1, gram_2 = two_gram
        
        # if gram_1[-1] == "-":
        #     gram_1 = gram_1[:-1] #remove "-" if it is the last char of word

        # if gram_2[-1] == "-":
        #     gram_2 = gram_2[:-1] #remove "-" if it is the last char of word

        file.writelines(gram_1 + delimiter + gram_2 + newline)
    file.close()


def build_vocabulary(lang, data_path):
    # tokens = tetun_tokenizer(data)
    tokens = tokenize_func(lang, data_path)
    vocabulary = list(sorted(set(tokens)))
    return vocabulary

# number of ocurrency
def term_frequency(lang, data_path):
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


def nomalized_term_frequency(lang, data_path):
    number_words = 0 
    tf = term_frequency(lang, data_path)
    
    for term in tf.items():
      number_words += tf[term]
    
    ntf = {}
    for term in tf.items():
      ntf[term] = round(tf[term]/number_words, 6)
    return ntf


def document_frequency(lang, path):
    file = load_data_as_dict(path)

    list_tokens = []
    for line in file:
        tokens = tokenize_data(lang, line)
        uniques = list(set(tokens))
        list_tokens.extend(uniques)

    list_tokens = sorted(list_tokens)

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

def words_dict(lang):
  words_dic = {}
  if lang == 'portuguese':
    folder = '/resources/'
    f = open(folder+lang+'/wordsList', 'r', encoding = "ISO-8859-1")
    words_dic = set(f.readlines())
  elif lang == 'english':
    words_dic = english_words_lower_set

  return words_dic

def remove_noise(weightModel, lang):
  clean_tf = {}
  dic = words_dict(lang)
  if dic:
    for term in weightModel.keys():
      if term+'\n' in dic or term in dic:
        clean_tf[term] = weightModel[term]
  return clean_tf

