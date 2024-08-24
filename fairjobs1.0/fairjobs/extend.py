import gensim.downloader
from nltk.stem import PorterStemmer
from vocabulary import fem_vocab, masc_vocab
import pickle

glove_wiki_vectors = gensim.downloader.load('glove-wiki-gigaword-100')
ps = PorterStemmer()

class ExtendVocabulary():

    def __init__(self):
        pass

    def extend_vocab(self, vocab):

        self.vocab = vocab
        self.extended_vocab = []

        for word in self.vocab:
            match_words = [key for key, val in glove_wiki_vectors.key_to_index.items()
                            if key.find(word) == 0]
            match_words = list(dict.fromkeys(match_words))
            for match_word in match_words:
                for index in range(3):
                    self.extended_vocab.append(match_word)
                    self.extended_vocab.append(glove_wiki_vectors
                                            .most_similar(match_word, topn=10)[index][0])

        self.extended_vocab = list(dict.fromkeys(self.extended_vocab))

        return self.extended_vocab

    def rm_overlap_words(self, basic_vocab, large_vocab):
        self.basic_vocab = basic_vocab
        self.large_vocab = large_vocab
        for base_word in self.basic_vocab:
            for word in self.large_vocab:
                if word.find(base_word) != -1:
                    self.large_vocab.remove(word)

        return self.large_vocab

vocabulary = ExtendVocabulary()
extended_fem_vocab = vocabulary.extend_vocab(fem_vocab)
extended_masc_vocab = vocabulary.extend_vocab(masc_vocab)

final_masc_vocab = vocabulary.rm_overlap_words(fem_vocab, extended_masc_vocab)
final_fem_vocab = vocabulary.rm_overlap_words(masc_vocab, extended_fem_vocab)

fh = open("../vocab_fem.pkl", 'wb')
pickle.dump(final_fem_vocab, fh)
fh.close()

fh = open("../vocab_masc.pkl", 'wb')
pickle.dump(final_masc_vocab, fh)
fh.close()

if __name__ == '__main__':
    print(len(final_fem_vocab), final_fem_vocab)
    print(len(final_masc_vocab), final_masc_vocab)
