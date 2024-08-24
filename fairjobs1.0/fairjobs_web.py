import streamlit as st
import pandas as pd
import numpy as np
import re
import string
import requests
from PIL import Image
from nltk.tokenize import word_tokenize
from annotated_text import annotated_text
import os
import streamlit.components.v1 as components


# Fetch Data from Google Cloud (GCP)
#BUCKET_NAME = "wagon-data-672-fechner"
BUCKET_NAME = "fairjobs_data"
#storage_filename = "data/data_full_df_web_gd.csv"
storage_filename = "data.csv"
#upload_storage_filename = "data/data_full_df_web_gd.csv"
upload_storage_filename = "data.csv"


#local_filename = "train_1k_downloaded.csv"

# create credentials file
google_credentials_file = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]

if not os.path.isfile(google_credentials_file):

    print("write credentials file 🔥" + f"\n- path: {google_credentials_file}")

    # retrieve credentials
    json_credentials = os.environ["GOOGLE_CREDS"]

    # write credentials
    with open(google_credentials_file, "w") as file:

        file.write(json_credentials)

else:

    print("credentials file already exists 🎉")


def get_data():

    #os.environ[
    #"GOOGLE_APPLICATION_CREDENTIALS"] = '/Users/renesalmon/code/reneSalmon/fairjobs-324510-bbb3c4c828a9.json'
    # webpage = url
    # soup = BeautifulSoup(webpage, "lxml")

    # title = soup.find("meta", proterty="og:title")

    return pd.read_csv(
        #f"gs://wagon-data-672-fechner/data/data_data_full_df_web_gd.csv",
        f"gs://fairjobs_data/data.csv",
        converters={
            'masc_words_list': eval,
            'fem_words_list': eval,
            'list_for_annotation': eval
        })


def app():

    # def my_widget(key):
    #     st.subheader('Hello there!')
    #     clicked = st.button("Click me " + key)


    # sidebar_selection = st.sidebar.radio(
    #     'Select data:',
    #     ['Problem', 'Solution', 'Value for Society'],
    # )



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
    search_word = st.text_input('Enter a jobtitle')

    # Serach field 2
    #form = st.form(key='my_form')
    #search_word = form.text_input(label='Enter jobtitel')

    # Personalizer Sliderbars
    my_expander = st.expander(label='personalize your search')
    with my_expander:
        "How important is to you ... ?"

        #sort results by gender
        #@st.cache
        def get_select_box_data():

            return pd.DataFrame(
                {'options': ['all', 'neutral', 'feminine', 'masculine']})

        df = get_select_box_data()

        option = st.selectbox('Sort by tone', df['options'])

        st.write('How important is ...')
        company_culture = st.slider(
            'company culture',
            1,
            10,
            help="looks for occurences of the words 'support', 'collaboration', 'team', 'value', 'culture' and similar words in the job description"
        )
        inclusivity = st.slider('inclusion', 1, 10, help="looks for occurences of the words 'transparent', 'fair', 'inclusive', 'equal' and similar words in the job description")
        flexibility = st.slider('flexibility',
                                    1,
                                    10,
                                    help="looks for occurences of the words 'home', 'part time', 'flexible', 'balance', 'vacation' and similar words in the job description")
        personal_development = st.slider('personal development',
                                         1,
                                         10,
                                         help="looks for occurences of the words 'grow', 'learn', 'train', 'coach', 'develop' and similar words")


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



    #Search Button
    if st.button('search'):
        #st.write('I was clicked 🎉')

        #st.write(f'sorted by {option} gender')
        #Search field 2
        # if form.form_submit_button(label='search'):
        #     st.write('I was clicked 🎉')

        ### SEARCH ENGINE ###

        #Import monster job_database to access job_offers
        #job_database = pd.read_csv('raw_data/data_df_all_3108-20.csv')
        job_database = get_data()

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

        #st.dataframe(job_list)#[[
        #    'job_title', 'gender', 'company culture', 'inclusivity',
        #    'family benefits', 'Personal development',
        # ]])

        df_filtered = job_list
        # df_filtered = pd.DataFrame(job_list[[
        # 'job_title', 'gender', 'company culture', 'inclusion',
        # 'flexibility', 'personal development', 'job_description',
        # 'fem_coded', 'masc_coded', 'list_for_annotation'
        # ]])

        #   df_filtered["Relevance Score"]= round(100 * (company_culture*df_filtered["company culture"].apply(lambda x: 1 if x=="Good" else 0) + \
        #                                         inclusivity*df_filtered["inclusion"].apply(lambda x: 1 if x=="Good" else 0) + \
        #                                         flexibility*df_filtered["flexibility"].apply(lambda x: 1 if x=="Good" else 0)+ \
        #                                         personal_development*df_filtered["personal development"].apply(lambda x: 1 if x=="Good" else 0)) / (company_culture+inclusion+flexiblity+personal_development) ,2 )

        df_filtered["Relevance Score"]= round((company_culture*df_filtered["company culture"] + \
                                            inclusivity*df_filtered["inclusion"] + \
                                            flexibility*df_filtered["flexibility"]+ \
                                            personal_development*df_filtered["personal development"]) / (company_culture+inclusivity+flexibility+personal_development) ,0)

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
        #st.table(personal_ranked_df_left)

        # #color-coding job_describtions
        # fem_words = ['support', 'responsible']
        # masculin_words = ['leader', 'objectives']
        # neutral_words = ['innovative']

        # lofl = []
        # for row in personal_ranked_df_left['job_description']:
        #     List_for_annotation = []
        #     for word in row.split():
        #         if word in fem_words:
        #             List_for_annotation.append((word + ' ', "female", "#faa"))

        #         elif word in masculin_words:
        #             List_for_annotation.append((word + ' ', "male", "#8ef"))

        #         elif word in neutral_words:
        #             List_for_annotation.append((word + ' ', "neutral", "#fea"))

        #         else:
        #             List_for_annotation.append(word + ' ')
        #     lofl.append(List_for_annotation)
        # personal_ranked_df_left['job_description_c'] = lofl
        #print(personal_ranked_df_left['job_description_c'])
        #annotated_job_describtions = List_for_annotation)

        for index, row in personal_ranked_df_left[0:10].iterrows():
            expander = st.expander(
                label=
                f"{row['job_title']} at {row['company_name']}")
            # st.write(
            #     f"gender-tone: {row['gender']}"
            # )
            # st.write(
            #     f"personal matching {row['Relevance Score']}%"
            # )


            with expander:
                #st.markdown("---")

                col0, col1, col2, col3, = st.columns(4)
                col0.metric(label='female coded', value=row['fem_coded'])
                col1.metric(label='male coded', value=row['masc_coded'])
                col2.metric(label='picture score', value=round(row['woman_pic_ratio'],2)*100)
                col3.metric(label='relevance score',
                            value=row['Relevance Score'])

                col4, col5, col6, col7 = st.columns(4)
                col4.metric(label='culture',
                            value=row['company culture'])
                col5.metric(label='inclusivity', value=row['inclusion'])
                col6.metric(label='flexibility', value=row['flexibility'])
                col7.metric(label='personal development',
                            value=row['personal development'])

                st.write(f"city: {row['loc']}")

                st.write(annotated_text(*row['list_for_annotation']))



#st.write("---")
