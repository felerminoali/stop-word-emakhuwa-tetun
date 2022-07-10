from config import  load_data_as_dict, generate_edges

def run(lang, folder):
    path = folder+lang+'.txt'
    number_of_docs = len(load_data_as_dict(path))
    generate_edges(folder+"edges-"+lang+".csv", folder+lang+".txt", lang)

if __name__ == '__main__':
    
    run('english', 'wikiclir/')
    run('portuguese', 'wikiclir/')
    run('emakhuwa', 'tetun-emakhuwa/')
    run('tetun', 'tetun-emakhuwa/')
    

