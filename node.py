from config import load_data_as_dict, term_frequency, document_frequency, remove_noise, normalized_term_frequency, idf, normalized_idf
from nltk.corpus import stopwords
import csv

if __name__ == '__main__':
    
    lang = 'portuguese'
    folder = 'wikiclir/'
    path = folder+lang+'.txt'

    number_of_docs = len(load_data_as_dict(path))

    stopw = stopwords.words(lang)
    file = open(folder+lang+'/nodes-'+lang+'.csv', "w", encoding="utf-8")

    tf = term_frequency(lang, path)
    tf = remove_noise(tf, lang)

    ntf = normalized_term_frequency(tf)

    df = document_frequency(lang, path)
    df = remove_noise(df, lang)

    idf_ = idf(number_of_docs, df)
    nidf = normalized_idf(number_of_docs, df)

    delimiter = ","
    newline = '\n'
    ids = {}
    nodes = [
            "id" + delimiter + 
            "Label"+ delimiter + 
            "tf" + delimiter + 
            "df" + delimiter + 
            "tdf" + delimiter + 
            "tf-idf" + delimiter + 
            "idf" + delimiter +
            "nidf" + delimiter + 
            "ntf" + delimiter+ 
            "stopword" + newline
            ]

    for index, term in enumerate(tf.keys()):
        ids[term] = index
        is_stop = '1' if term in stopw else '0'
        nodes.append(
            str(index) + delimiter + 
            term + delimiter +
            str(tf[term]) + delimiter + 
            str(df[term]) + delimiter + 
            str(tf[term]*df[term]) + delimiter  + 
            str(ntf[term]*idf_[term]) + delimiter  + 
            str(idf_[term]) + delimiter + 
            str(nidf[term]) + delimiter + 
            str(ntf[term]) + delimiter + 
            is_stop+ newline)
    file.writelines(nodes)
    file.close()

    out = ["Source, Target, Type, Weight"]
    error = []
    edges = []
    with open(folder+lang+'/edges-'+lang+'.csv', 'r', encoding="utf8") as csvfile:
      reader = csv.reader(csvfile)
      header = next(reader)
      for row in reader:
          if (row[0].strip() in ids) and (row[1].strip() in ids):
            out.append(str(ids[row[0].strip()]) + ', '+str(ids[row[1].strip()])+', Directed, 1.0')
            edges.append([str(ids[row[0].strip()]), str(ids[row[1].strip()]), 1])
          else:
            error.append(row[0].strip()+', '+row[1].strip())

    file2 = open(folder+lang+"/edges-"+lang+"-gephi.csv", "w", encoding="utf8")
    file2.writelines("\n".join(out))
    file2.close()
