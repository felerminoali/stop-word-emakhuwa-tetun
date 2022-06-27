from config import  load_data_as_dict, generate_edges

if __name__ == '__main__':
    # generate the file for edges
    # lang = 'portuguese'
    lang = 'english'
    folder = 'wikiclir/'
    path = folder+lang+'.txt'

    number_of_docs = len(load_data_as_dict(path))
    generate_edges(folder+"edges-"+lang+".csv", folder+lang+".txt", lang)