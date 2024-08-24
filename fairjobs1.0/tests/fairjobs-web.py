import streamlit as st
import pandas as pd
import numpy as np
import re
import string
import requests
from PIL import Image
from nltk.tokenize import word_tokenize


# def my_widget(key):
#     st.subheader('Hello there!')
#     clicked = st.button("Click me " + key)


sidebar_selection = st.sidebar.radio(
    'Select data:',
    ['Problem', 'Solution', 'Value for Society'],
)


# AND in st.sidebar!
# with st.sidebar:
#     clicked = my_widget("third")

# st.set_page_config(
#         page_title="Quick reference", # => Quick reference - Streamlit
#         page_icon=":aktentasche:",
#          layout="centered", # wide
#         initial_sidebar_state="auto") # collapsed


# '''
# # fairjobs - job search engine
# '''


#fairjobs logo
image = Image.open('./images_website/fairjobs_logo.png')
st.image(image)

#Personalized Filter-Weights
sessions_state = 0

# Search field
search_word = st.text_input('Enter a jobtitel')

# Serach field 2
#form = st.form(key='my_form')
#search_word = form.text_input(label='Enter jobtitel')

# Personalizer Sliderbars
my_expander = st.expander(label='personalise your search')
with my_expander:
    "How important is to you ... ?"


    #company_culture = st.slider('How important is the company culture to you?', 1, 10)
    company_culture = st.slider('company culture', 1, 10)
    inclusivity = st.slider('inclusivity', 1, 10)
    family_benefits = st.slider('flexibility', 1, 10)
    personal_development = st.slider('personal development', 1, 10)


    # if company_culture:
    #     st.session_state.company_culture = company_culture

    # if inclusivity:
    #     st.session_state.inclusivity = inclusivity

    # if family_benefits:
    #     st.session_state.family_benefits = family_benefits

    # if personal_development:
    #     st.session_state.personal_development = personal_development

    #Sort jobs-button
    #clicked = my_expander.button('sort jobs')

    #sort results by gender
    #@st.cache
    def get_select_box_data():

        return pd.DataFrame({
            'options': ['all', 'neutral', 'feminine', 'masculine']
        })

    df = get_select_box_data()

    option = st.selectbox('Select gender', df['options'])


#Search Button
if st.button('search'):
    print('button clicked!')
    st.write('I was clicked 🎉')

    #Search field 2
    # if form.form_submit_button(label='search'):
    #     st.write('I was clicked 🎉')

    ### SEARCH ENGINE ###

    #Import monster job_database to access job_offers
    job_database = pd.read_csv('raw_data/basemodel_crit.csv')

    #Clean job_title column
    job_title = job_database['job_title']

    job_title_clean = []
    for d in job_title:
        # Remove Unicode
        title_cleaning = re.sub(r'[^\x00-\x7F]+', ' ', d)
        # Remove Mentions
        title_cleaning = re.sub(r'@\w+', '', title_cleaning)
        # Lowercase the document
        title_cleaning = title_cleaning.lower()
        # Remove punctuations
        title_cleaning = re.sub(r'[%s]' % re.escape(string.punctuation), ' ',
                                title_cleaning)
        # Lowercase the numbers
        title_cleaning = re.sub(r'[0-9]', '', title_cleaning)
        # Remove the doubled space
        title_cleaning = re.sub(r'\s{2,}', ' ', title_cleaning)
        job_title_clean.append(title_cleaning)

    #Return clean job title column back to dataframe by creating new column "searchable_jobtitles"
    job_database['searchable_jobtitles'] = job_title_clean

    #Clean input 'search_word'

    # Remove Unicode
    clean_search_word = re.sub(r'[^\x00-\x7F]+', ' ', search_word)
    # Remove Mentions
    clean_search_word = re.sub(r'@\w+', '', clean_search_word)
    # Lowercase the document
    clean_search_word = clean_search_word.lower()
    # Remove punctuations
    clean_search_word = re.sub(r'[%s]' % re.escape(string.punctuation), ' ',
                        clean_search_word)
    # Lowercase the numbers
    clean_search_word = re.sub(r'[0-9]', '', clean_search_word)
    # Remove the doubled space
    clean_search_word = re.sub(r'\s{2,}', ' ', clean_search_word)
    print(clean_search_word)

    # Search function
    #matched_titels = job_database['searchable_jobtitles'] == clean_search_word
    matched_titels = job_database['searchable_jobtitles'].str.contains(clean_search_word)

    # print dataframe 1
    job_list = job_database[matched_titels]

    # st.dataframe(job_list[[
    #    'job_title', 'gender', 'company culture', 'inclusivity',
    #    'family benefits', 'Personal development',
    # ]])

    df_filtered = pd.DataFrame(job_list[[
       'job_title', 'gender', 'company culture', 'inclusivity',
       'family benefits', 'Personal development',
    ]])

    df_filtered["Relevance Score"]= round(100 * (company_culture*df_filtered["company culture"].apply(lambda x: 1 if x=="Good" else 0) + \
                                        inclusivity*df_filtered["inclusivity"].apply(lambda x: 1 if x=="Good" else 0) + \
                                        family_benefits*df_filtered["family benefits"].apply(lambda x: 1 if x=="Good" else 0)+ \
                                        personal_development*df_filtered["Personal development"].apply(lambda x: 1 if x=="Good" else 0)) / (company_culture+inclusivity+family_benefits+personal_development) ,2 )


    personal_ranked_df = df_filtered.sort_values(by=['Relevance Score', 'gender'] , ascending=False)

    #personal_ranked_df_index_free = personal_ranked_df.assign(hack='').reset_index(drop=True)

    if option == 'all':
        personal_ranked_df_index_free = personal_ranked_df.reset_index(
                drop=True)
    else:
        personal_ranked_df_index_free = personal_ranked_df[
            personal_ranked_df['gender'] == option].reset_index(
                drop=True)

    personal_ranked_df_left = personal_ranked_df_index_free#.style.set_properties(
    #**{'text-align': 'left'})

    for index, row in personal_ranked_df_left.iterrows():
        expander = st.expander(label=f"{row['job_title']} {row['gender']}")
        with expander:
            st.metric(label='score', value=row['Relevance Score'])


    #st.table(personal_ranked_df_left)








#pd.set_option('display.max_colwidth', None)


#my_expander = st.beta_expander()
#my_expander.write('Hello there!')
#clicked = my_expander.button('Click me!')

#df = pd.DataFrame({
#       'job':[job_database[matched_titels]['job_title']]
# 'Company': ['Google', 'Tesla', 'Facebook', 'Volkswagen'],
# 'Rating': ['4 stars', '3 stars', '5 stars', '3 stars'],
# 'Tone': ['female', 'male', 'neutral', 'female'],
# 'City': ['London', 'Hamburg', 'Dublin', 'Paris'],
# 'Relevance Score': ['90%', '75%', '60%', '43%']
# })
#df = pd.DataFrame(np.random.randn(3, 5),
#                  columns=['Job', 'Company', 'City', 'Tone','Matching Score'])

#st.table(df.head())


# Filter
#if st.checkbox('Filter 1'):
#    st.write('active')

#if st.checkbox('Filter 2'):
#    st.write('active')

#if st.checkbox('Filter 3'):
#    st.write('active')

#if st.checkbox('Filter 4'):
#    st.write('active')

#if st.checkbox('Filter 5'):
#    st.write('active')

# Display search results

#df = pd.DataFrame(job_database[matched_titels]),
#                  columns=['Job', 'Company', 'City', 'Tone','Matching Score'])

#Create output dataframe

#Create markdown Toogle to see job describtion

#Add Css for color coding for filter words


# or using the score directly
#job_database["Relevance Score_score"]= round( 100 * (company_culture*job_database["company culture_score"] + \
#                                  inclusivity*job_database["inclusivity_score"] + \
#                                 family_benefits*job_database["family benefits_score"] + \
#                                personal_development*job_database["Personal development_score"] ) \
#                             / (company_culture+inclusivity+family_benefits+personal_development),2)

"""
# Annotated text example

Below is an example of how to use the annotated_text function:
"""

from annotated_text import annotated_text


fem_words = ['support','responsible']
masculin_words =['leader', 'objectives']
neutral_words =['innovative']

job_description ='We are looking for responsible leader who support innovative ideas in our objectives'


List_for_annotion = []
tokenized = word_tokenize(job_description)
for word in tokenized:
    if word in fem_words:
        List_for_annotion.append((word, 'female', "#8ef"))
    else:
        List_for_annotion.append(word)

annotated_text(List_for_annotion)

annotated_text(
    "This ",
    ("is", "male", "#8ef"),
    " some ",
    ("annotated", "adj", "#faa"),
    ("text", "noun", "#afa"),
    " for those of ",
    ("you", "pronoun", "#fea"),
    " who ",
    ("like", "verb", "#8ef"),
    " this sort of ",
    ("thing", "noun", "#afa"),
)


#df_job_description = pd.DataFrame(job_list[['job_description']])
#st.dataframe(df_job_description)
