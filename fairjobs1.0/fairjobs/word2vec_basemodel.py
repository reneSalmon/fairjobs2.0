# from vocabulary import masc_vocab, fem_vocab
# from gensim.models import Word2Vec

#     def word2vec(self):

#         self.word2vec_description = Word2Vec(sentences=self.df['clean_description'],
#                                              vector_size=50,
#                                              min_count=1)
#         return self

#     def save_model(self):
#         return self.word2vec_description.save("../word2vec.model")

#     def load_model(self):
#         self.word2vec_description = Word2Vec.load("../word2vec.model")
#         return self.word2vec_description

#     def masc_similar_words(self, text):
#         # simil_masc_vocab = []
#         # match_masc_vocab = []

#         n_simil_masc = 0
#         n_match_masc = 0

#         for word in text:
#             for masc_word in masc_vocab:
#                 if masc_word in self.word2vec_description.wv.key_to_index:
#                     if self.word2vec_description.wv.similarity(word, masc_word) > 0.9 and\
#                     self.word2vec_description.wv.similarity(word, masc_word) < 0.99:
#                         n_simil_masc += 1
#                         # simil_masc_vocab.append((word, masc_word))
#                         # simil_masc_vocab = list(dict.fromkeys(simil_masc_vocab))
#                 if word.find(masc_word) == 0:
#                     n_match_masc += 1
#                     # match_masc_vocab.append((word, masc_word))
#                     # match_masc_vocab = list(dict.fromkeys(match_masc_vocab))

#         return (n_simil_masc + n_match_masc)

#     def fem_similar_words(self, text):
#         # simil_fem_vocab = []
#         # match_fem_vocab = []

#         n_simil_fem = 0
#         n_match_fem = 0

#         for word in text:
#             for fem_word in fem_vocab:
#                 if fem_word in self.word2vec_description.wv.key_to_index:
#                     if self.word2vec_description.wv.similarity(word, fem_word) > 0.9 and\
#                     self.word2vec_description.wv.similarity(word, fem_word) < 0.99:
#                         n_simil_fem += 1
#                         # simil_fem_vocab.append((word, fem_word))
#                         # simil_fem_vocab = list(dict.fromkeys(simil_fem_vocab))
#                 if word.find(fem_word) == 0:
#                     n_match_fem += 1
#                     # match_fem_vocab.append((word, fem_word))
#                     # match_fem_vocab = list(dict.fromkeys(match_fem_vocab))

#         return (n_simil_fem + n_match_fem)

# model.word2vec()
# model.save_model()
# model.load_model()
