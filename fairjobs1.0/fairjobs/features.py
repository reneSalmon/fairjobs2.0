from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import gensim.downloader  #import error?
import requests
import string
import unidecode
import re

# List of criterias to engineer extra features for the datasets
# TODO move to parameters file
Criterias=["support",
             "collaborat",
             "team",
             "value",
             "cultur",
             "transparent",
             "fair",
             "open",
             "inclusi",
             "equal",
             "equal",
             "home",
             "part time",
             "flexib",
             "balance",
             "vacation",
             "develop",
             "grow",
             "learn",
             "train"]

# Anita's customized criterias dictionary:
# TODO move to parameters file
anita_dict={"Company culture":["support", "collaborat", "team", "value", "cultur"],
            "Inclusivity": ["transparen", "fair", "open", "inclusi", "equal"],
            "Flexibility" :["home", "part time", "flexib", "balance", "vacation"],
            "Personal development": ["develop", "grow", "learn", "train"]}

# loading a Word2Vec, other possibilities are:
# print(list(gensim.downloader.info()['models'].keys()))
def model_build(w2vec_model):
    model_wiki= gensim.downloader.load(w2vec_model)  #glove-wiki-gigaword-300
    return model_wiki

# retrieving synonyms (inspect class if not working anymore)
def synonyms(term):
    response = requests.get('https://www.thesaurus.com/browse/{}'.format(term))
    soup = BeautifulSoup(response.text, 'lxml')
    soup.find('section', {'class': 'css-191l5o0-ClassicContentCard e1qo4u830'})
    return [span.text.strip() for span in soup.findAll('a', {'class': 'css-1kg1yv8 eh475bn0'})] #check if class works

# creating dictionaries of criterias terms based on synonyms
def syn_dict_list(Criterias):
    syn_dict={}
    syn_list=[]
    model_wiki=model_build("glove-wiki-gigaword-300") # using glove-wiki-gigaword-300
    for word in Criterias:
        syn_list=synonyms(word)+[word]
        if word in model_wiki.key_to_index.keys():
            syn_list+=[x[0] for x in model_wiki.most_similar(word)]
        syn_dict[word]=[x for x in set(syn_list)]
    return syn_dict #potential TODO: return only single common root for word with similar common roon

# count occurences of criteria and related terms in descriptions
def count_sup(description, dict_list):
    count_support=len([x for x in dict_list if x in description])
    return count_support

# count occurences of criteria and related terms in descriptions and categorize right away
def count_sup_cat(description, dict_list):
    count_support=len([x for x in dict_list if x in description])
    if count_support ==0:
      return "None"
    if count_support <3:
      return "Few"
    return "Lot"

# count occurences of criteria and related terms in descriptions and categorize right away as bool
def count_sup_cat_bool(description, dict_list):
    count_support=len([x for x in dict_list if x in description])
    if count_support ==0:
      return "None"
    return "Yes"

# Score criterias avalability
# Be careful, only works while using my cleaning description function which return a single string
def proper_count_sup(description, dict_list):
      count_support=[]
      for y in dict_list:
        test_list1=[u for u in  description.split() if y in u ]
        count_support.append(len(test_list1))
      if sum(count_support)/len(dict_list)<1:
        return sum(count_support)/len(dict_list)
      return 1

# count occurences of criteria and related terms in descriptions
# Be careful, only works while using my cleaning description function which return a single string
# ---> Anita here: function disabled and replaced by criteria_percentage_count function
# def proper_count_sup_rene(description, dict_list):
#       count_support=[]
#       for y in dict_list:
#         test_list1=[u for u in description.split() if y in u ]
#         count_support.append(len(test_list1))
#       if sum(count_support)>0:
#         return 'Good'
#       return 'Bad'

# check if keywords are in description and return a percentage based on it
def criteria_percentage_count(description, dict_list):
    count_percentage=[]
    for x in dict_list:
        help_list=[u for u in description.split() if x in u]
        count_percentage.append(len(help_list))
        if count_percentage ==0:
            return 0
        if count_percentage ==1:
           return 20
        if count_percentage ==2:
            return 40
        if count_percentage ==3:
            return 60
        if count_percentage ==4:
            return 80
        return 100

# --> include def proper_count_sup(description, dict_list):
    #   count_support=[]
    #   for y in dict_list:
    #     test_list1=[u for u in  description.split() if y in u ]
    #     count_support.append(len(test_list1))
    #   if sum(count_support)/len(dict_list)<1:
    #     return sum(count_support)/len(dict_list)
    #   return 1

# Cleaning function that should be imported elsewhere
# Be careful, this is my version which returns a single string
# careful as well, it does not seem to play nicely while exporting to csv
def clean (text):
    text_urless=re.sub(r"(https?:\/\/)(\s)*(www\.)?(\s)*((\w|\s)+\.)*([\w\-\s]+\/)*([\w\-]+)((\?)?[\w\s]*=\s*[\w\%&]*)*", '', text)
    for punctuation in string.punctuation:
        text = text_urless.replace(punctuation, ' ') # Remove Punctuation
        lowercased = text.lower() # Lower Case
        unaccented_string = unidecode.unidecode(lowercased) # remove accents
        tokenized = word_tokenize(unaccented_string) # Tokenize
        words_only = [word for word in tokenized if word.isalpha()] # Remove numbers
        stop_words = set(stopwords.words('english')) # Make stopword list
        without_stopwords = [word for word in words_only if not word in stop_words] # Remove Stop Words
    return " ".join(without_stopwords)

# Building features columns
def building_features(df):
    syn_dict=syn_dict_list(Criterias)
    df["clean_description"]=df["job_description"].apply(clean)
    for x in syn_dict.keys():
        dict_list=syn_dict[x]
        df[f"{x}"]=df["clean_description"].apply(count_sup, args=([dict_list]))

# Building feature columns with Anita's dict:
def building_features_anita(df):
    df["clean_description"]=df["job_description"].apply(clean)
    for x in anita_dict.keys():
        dict_list=anita_dict[x]
        df[f"{x}"]=df["clean_description"].apply(count_sup_cat, args=([dict_list]))

# Using Anita's proposed scoring function which returns a float if under 1 or 1
def building_features_w_AnitaScore(df):
    for x in anita_dict.keys():
        dict_list=anita_dict[x]
        df[f"{x}_score"]=df["clean_description"].apply(proper_count_sup, args=([dict_list]))

# Function to return good or bad if criterias are found or not according to René formating suggestion
def building_features_rene(df):
    for x in anita_dict.keys():
        dict_list=anita_dict[x]
        df[f"{x}"]=df["clean_description"].apply(criteria_percentage_count, args=([dict_list]))

# Function to make a compound score with the criterias matching
# Assuming the dataframe is named basemodel (but to be changed with the name you are giving it)
# Anita here: function disabled and replaced by comp_relevance_score function
# def calc_rel_score(df, var1, var2, var3, var4):
#     df["Relevance Score"]= round( 100 * ( var1*df["company culture"].apply(lambda x: 1 if x=="Good" else 0) + \
#                                     var2*df["inclusivity"].apply(lambda x: 1 if x=="Good" else 0) + \
#                                     var3*df["flexibility"].apply(lambda x: 1 if x=="Good" else 0)+ \
#                                     var4*df["personal development"].apply(lambda x: 1 if x=="Good" else 0)) \
#                                         / (var1 + var2 + var3 + var4) ,2 )

# Function to make a compound score with the criterias matching
# Using the score columns directly
# Anita here: function disabled and replaced by comp_relevance_score function
# def calc_rel_score_direct(df, var1, var2, var3, var4):
#     df["Relevance Score_score"]= round( 100 * ( var1*df["company culture_score"] + \
#                                     var2*df["inclusivity_score"] + \
#                                     var3*df["flexibility_score"] + \
#                                     var4*df["personal development_score"] ) \
#                                     / (var1+var2+var3+var4),2)

# compute relevance score by using slider value and main criteria percentage
def comp_relevance_score(df, var1, var2, var3, var4):
    df["Relevance Score_score"]= round(var1*df["company culture_score"] + \
                                    var2*df["inclusivity_score"] + \
                                    var3*df["flexibility_score"] + \
                                    var4*df["personal development_score"] \
                                    / (var1+var2+var3+var4),2)
