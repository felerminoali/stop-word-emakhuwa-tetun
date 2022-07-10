from nltk import ngrams
from nltk.tokenize import word_tokenize
import re
from nltk import tokenize
from english_words import english_words_lower_set


import math

# function to load data as dictionary
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
    tokens = re.findall(r"[áéíóú]*[a-z]+[-’'áéíóúñ]*[a-z]*[-’'áéíóú]*[a-z]*", lower_data)
    
    return tokens


# white space tokenizer, set portuguese as default value
def whitespace_tokenizer(data, lang='portuguese'):
    lower_data = data.lower()  # lowercase the corpus
    tokens =[]
    tokens = [token for token in tokenize.word_tokenize(lower_data, language=lang) if token.isalpha()]
    
    return tokens


# Counts the frequency of a term
def count_freq(term, tokens):
    tokens = sorted(tokens)
    sum = 0
    for index, t in enumerate(tokens):
        if t == term:
            sum+=1
            if tokens[index + 1] != t:
                break
    
    return sum


# Tokenizer
def tokenize_func(lang, data_source):
    tokens = []
    lines = load_data_as_dict(data_source)

    for i, line in enumerate(lines):
        tokenized = tokenize_data(lang, line)
        tokens.extend(tokenized)

    return tokens


# function to tokenize the corpus
def tokenize_data(lang, data):
    tokens = []
    if lang == 'tetun':
        tokens = tetun_tokenizer(data)
    else:
        tokens = whitespace_tokenizer(data)
    
    return tokens


# function to generate edges using 2 grams as default value
def generate_edges(file, data_source, lang, n=2, delimiter=", ", newline="\n"):

    tokens = tokenize_func(lang, data_source)
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


# Builds a vocabulary of unique words
def build_vocabulary(lang, data_path):
    tokens = tokenize_func(lang, data_path)
    vocabulary = list(sorted(set(tokens)))
    
    return vocabulary


# function to calculate term frequency (TF)
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


# function to calculate normalized term frequency (NTF)
def normalized_term_frequency(tf):
    number_words = 0

    for term in tf.keys():
      number_words += tf[term]
    
    ntf = {}
    for term in tf.keys():
      ntf[term] = math.log(tf[term]/number_words)*(-1)

    return ntf


# function to calculate inverse document frequency (IDF)
def idf(n, df):
  idf = {}
  for term in df.keys():
    idf[term] = math.log(n/df[term])

  return idf


# function to calculate normalized inverse document frequency (NIDF)
def normalized_idf(n, df):
  nidf = {}
  for term in df.keys():
    nidf[term] = math.log((n-df[term]+0.5)/(df[term])+0.5)

  return nidf


# function to calculate document frequency (DF)
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


# function to pre-process English and Portuguese
def remove_noise(weightModel, lang):
  clean_tf = {}
  dic = words_dict(lang)
  if dic:
    for term in weightModel.keys():
      if term+'\n' in dic or term in dic:
        clean_tf[term] = weightModel[term]
  
  return clean_tf


# Return the wordlist or vocabulary of a given language
def words_dict(lang):
  words_dic = {}
  if lang == 'portuguese':
    folder = '/resources/'
    f = open(folder+lang+'/wordsList', 'r', encoding = "ISO-8859-1")
    words_dic = set(f.readlines())
  elif lang == 'english':
    words_dic = english_words_lower_set

  return words_dic
