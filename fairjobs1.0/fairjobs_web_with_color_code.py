import streamlit as st
import pandas as pd
import numpy as np
import re
import string
import requests
from PIL import Image
from nltk.tokenize import word_tokenize
from annotated_text import annotated_text


# app1.py

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
    search_word = st.text_input('Enter a jobtitel')

    # Serach field 2
    #form = st.form(key='my_form')
    #search_word = form.text_input(label='Enter jobtitel')

    # Personalizer Sliderbars
    my_expander = st.expander(label='personalise your search')
    with my_expander:
        "How important is to you ... ?"


        #company_culture = st.slider('How important is the company culture to you?', 1, 10)
        company_culture = st.slider(
            'company culture',
            0,
            10,
            help='lalalalala alalala'
        )
        inclusivity = st.slider('inclusivity', 0, 10, help='lalalalala alalala')
        family_benefits = st.slider('flexibility',
                                    0,
                                    10,
                                    help='lalalalala alalala')
        personal_development = st.slider('personal development',
                                         0,
                                         10,
                                         help='lalalalala alalala')


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

        option = st.selectbox('Sort by gender', df['options'])


    #Search Button
    if st.button('search'):
        #st.write('I was clicked 🎉')
        st.markdown(
            "<h1 style='text-align: right; color: red;'>sorted by</h1>",
            unsafe_allow_html=True)
        #st.write(f'sorted by {option} gender')
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
        'family benefits', 'Personal development', 'job_description',
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


        personal_ranked_df_left = personal_ranked_df_index_free[0:10]#.style.set_properties(
        #**{'text-align': 'left'})

        #color-coding job_describtions
        fem_words = ['support', 'responsible']
        masculin_words = ['leader', 'objectives']
        neutral_words = ['innovative']
        st.markdown("""

        """)

        lofl = []
        for row in personal_ranked_df_left['job_description']:
            List_for_annotation = []
            for word in row.split():
                if word in fem_words:
                    List_for_annotation.append((word + ' ', "female", "#faa"))

                elif word in masculin_words:
                    List_for_annotation.append((word + ' ', "male", "#8ef"))

                elif word in neutral_words:
                    List_for_annotation.append((word + ' ', "neutral", "#fea"))

                else:
                    List_for_annotation.append(word + ' ')
            lofl.append(List_for_annotation)
        personal_ranked_df_left['job_description_c'] = lofl
        print(personal_ranked_df_left['job_description_c'])
        #annotated_job_describtions = List_for_annotation)

        for index, row in personal_ranked_df_left.iterrows():
            expander = st.expander(label=f"{row['job_title']} {row['gender']}")

            with expander:
                st.markdown("---")
                col1, col2, col3, col4, col5, col6 = st.columns(6)
                col1.metric(label='company culture', value=row['company culture'])
                col2.metric(label='gender bias', value=row['gender'])
                col3.metric(label='inclusivity', value=row['inclusivity'])
                col4.metric(label='flexibility', value=row['family benefits'])
                col5.metric(label='personal development', value=row['Personal development'])
                col6.metric(label='matching score', value=row['Relevance Score'])
                st.write("---")

                st.write(annotated_text(*row['job_description_c']))

                #st.write(row['job_description'])









                #st.table(personal_ranked_df_left)






#[company website](http://github.com/streamlit)

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



#df_job_description = pd.DataFrame(job_list[['job_description']])
#st.dataframe(df_job_description)
