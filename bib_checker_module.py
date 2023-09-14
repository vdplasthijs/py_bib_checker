import numpy as np 
import bibtexparser

class BibFile():
    def __init__(self, path_to_bib_file=''):
        self.path_to_bib_file = path_to_bib_file
        assert type(path_to_bib_file) == str, 'path_to_bib_file must be a string'
        self.load_bibtex_file(path_to_bib_file)

    def load_bibtex_file(self, filepath):
        '''Load bibtex file from path, and save data in self.info_dict'''
        with open(filepath) as bf:
            bib_db = bibtexparser.load(bf)
        self.bib_db = bib_db      

    def check_duplicates(self, key='ID', verbose=1):
        '''Check if there are duplicate keywords in the bibtex file'''
        all_keywords = []
        for entry in self.bib_db.entries:
            if key in entry:
                keywords = entry[key]
        all_keywords = np.array(keywords)
        unique_keywords = np.unique(all_keywords)
        duplicate_keywords = []
        for keyword in unique_keywords:
            if np.sum(all_keywords == keyword) > 1:
                duplicate_keywords.append(keyword)

        if len(duplicate_keywords) == 0:
            if verbose > 0:
                print(f'No duplicate {key} entries found')
            bool_duplicates = False
        else:
            bool_duplicates = True
            ## always print:
            print(f'{len(duplicate_keywords)} duplicate {key} entries found:')
            print(duplicate_keywords)
        return bool_duplicates, duplicate_keywords
    
    def standard_duplicate_check(self):
        for key in ['ID', 'doi', 'title']:
            bool_dup, _ = self.check_duplicates(key=key, verbose=0)
            assert bool_dup == False, f'Duplicate {key} entries found'