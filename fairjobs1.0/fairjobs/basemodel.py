import data
import pickle
import pandas as pd

class BaseModel(object):

    def __init__(self, df):
        self.df = df

    # def fem_words(self, text):
    #     fh = open("../vocab_fem.pkl", 'rb')
    #     final_fem_vocab = pickle.load(fh)
    #     fh.close()

    #     self.fem_words_list = []

    #     n_fem_words = 0
    #     for word in text:
    #         if word in final_fem_vocab:
    #             self.fem_words_list.append(word)
    #             n_fem_words += 1

    #     return self.fem_words_list

    # def masc_words(self, text):
    #     fh = open("../vocab_masc.pkl", 'rb')
    #     final_masc_vocab = pickle.load(fh)
    #     fh.close()

    #     self.masc_words_list = []

    #     n_masc_words = 0
    #     for word in text:
    #         if word in final_masc_vocab:
    #             self.masc_words_list.append(word)
    #             n_masc_words += 1

    #     return self.masc_words_list

    # def text_for_annotation(self, text):

    #     self.neut_words_list = []
    #     self.List_for_annotation = []
    #     for i in range(len(self.df)):
    #         for word in text.split():
    #             if word in self.df['fem_words_list'][i]:
    #                 if word in self.df['masc_words_list'][i]:
    #                     self.List_for_annotation.append((word + ' ', "neutral", "#fea"))
    #                 self.List_for_annotation.append((word + ' ', "female", "#faa"))
    #             elif word in self.df['masc_words_list'][i]:
    #                 self.List_for_annotation.append((word + ' ', "male", "#8ef"))
    #             else:
    #                 self.List_for_annotation.append(word + ' ')
    #         return self.List_for_annotation

    def masc_fem_word_list(self, text):
        fh = open("../vocab_masc.pkl", 'rb')
        final_masc_vocab = pickle.load(fh)
        fh.close()
        fh = open("../vocab_fem.pkl", 'rb')
        final_fem_vocab = pickle.load(fh)
        fh.close()

        self.cleaned_description = data.clean_text(text)

        self.masc_words_list = []
        self.fem_words_list = []
        self.neut_words_list = []

        n_masc_words = 0
        n_fem_words = 0

        for word in self.cleaned_description:
            if word in final_masc_vocab:
                self.masc_words_list.append(word)
                n_masc_words += 1
            if word in final_fem_vocab:
                self.fem_words_list.append(word)
                n_fem_words += 1

        self.masc_words_list = list(dict.fromkeys(self.masc_words_list))
        self.fem_words_list = list(dict.fromkeys(self.fem_words_list))

        self.List_for_annotation = []
        for word in text.split():

            flag_neut = False
            flag_fem = False
            flag_masc = False

            for fem_word in self.fem_words_list:
                if word.lower().find(fem_word) == 0:
                    for masc_word in self.masc_words_list:
                        if word.lower().find(masc_word) == 0:
                            self.List_for_annotation.append((word + ' ', "neutral", "#fea"))
                            flag_neut = True
                            break
                    else:
                        if flag_neut == False:
                            self.List_for_annotation.append((word + ' ', "female", "#faa"))
                            flag_fem = True
                            break
            else:
                for masc_word in self.masc_words_list:
                    if word.lower().find(masc_word) == 0:
                        if flag_neut == False:
                            self.List_for_annotation.append((word + ' ', "male", "#8ef"))
                            flag_masc = True
                            break

            if flag_neut == False and flag_fem == False and flag_masc == False:
                self.List_for_annotation.append(word + ' ')

        return self.cleaned_description, self.masc_words_list, self.fem_words_list,\
               self.List_for_annotation, n_masc_words, n_fem_words

    def label_gender(self, row):
        if 100 >= row['fem_coded'] > 52 :
            return 'feminine'
        elif 100 >= row['masc_coded'] > 52:
            return 'masculine'
        else:
            return 'neutral'

    def masc_fem_words(self):
        # self.df['masc_words_list'] = self.df['clean_description'].apply(self.masc_words)
        # self.df['fem_words_list'] = self.df['clean_description'].apply(self.fem_words)
        # self.df['masc_words'] = self.df['masc_words_list'].apply(len)
        # self.df['fem_words'] = self.df['fem_words_list'].apply(len)

        # self.df['list_for_annotation'] = self.df['job_description'].apply(self.text_for_annotation)

        self.df['results'] = self.df['job_description'].apply(self.masc_fem_word_list)
        self.df[['clean_description', 'masc_words_list', 'fem_words_list',
                 'list_for_annotation', 'masc_words', 'fem_words']] =\
                pd.DataFrame(self.df['results'].tolist(), index=df.index)

        self.df['masc_coded'] = self.df['masc_words']/(self.df['masc_words'] +
                                                       self.df['fem_words'] + 0.001)
        self.df['fem_coded'] = self.df['fem_words']/(self.df['masc_words']
                                                     + self.df['fem_words'] + 0.001)

        self.df.masc_coded = self.df.masc_coded.round(2)*100
        self.df.fem_coded = self.df.fem_coded.round(2)*100
        self.df['gender'] = self.df.apply(lambda row: self.label_gender(row), axis=1)
        return self.df

    def df_to_csv(self):
        self.df.to_csv('../raw_data/data_full_df_web_gd.csv', encoding='utf-8')

if __name__ == '__main__':
    df = data.get_data()
    # df_clean = data.clean_df(df)
    # print(df_clean.columns)
    model = BaseModel(df)
    model.masc_fem_words()
    model.df_to_csv()
    print(model.df)
