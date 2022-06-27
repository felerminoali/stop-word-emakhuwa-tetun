from config import term_frequency, document_frequency, remove_noise
from nltk.corpus import stopwords
import csv

if __name__ == '__main__':
    
    lang = 'portuguese'
    folder = 'wikiclir/'
    path = folder+lang+'.txt'


    stopw = stopwords.words(lang)
    file = open(folder+lang+'/nodes-'+lang+'.csv', "w", encoding="utf-8")

    tf = term_frequency(lang, path)
    tf = remove_noise(tf, lang)

    df = document_frequency(lang, path)
    df = remove_noise(df, lang)


    delimiter = ","
    newline = '\n'
    ids = {}
    nodes = ["id" + delimiter + "Label"+ delimiter + "tf" + delimiter + "df" + delimiter + "tdf" + delimiter +"stopword"+ newline]
    for index, term in enumerate(tf.keys()):
        ids[term] = index
        is_stop = '1' if term in stopw else '0'
        nodes.append(str(index) + delimiter + term + delimiter + str(tf[term]) + delimiter + str(df[term]) + delimiter + str(tf[term]*df[term]) + delimiter+ is_stop+ newline)
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
            # print(str( (row[0].strip() in ids))+' '+ row[0].strip()+' '+row[1].strip()+' '+str((row[1].strip() in ids)))


    file2 = open(folder+lang+"/edges-"+lang+"-gephi.csv", "w", encoding="utf8")
    file2.writelines("\n".join(out))
    file2.close()




