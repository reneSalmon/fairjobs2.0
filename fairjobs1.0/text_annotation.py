from annotated_text import annotated_text
from annotated_text import annotation
from nltk.tokenize import word_tokenize
import streamlit as st
import pandas as pd
import numpy as np


# app2.py

def app():
    st.title('APP3')
    st.write('Welcome to app3')


    annotated_text(
                "Hello ",
                annotation("world!", "noun", color="#8ef", border="1px dashed red"),
    )

    """
    # Annotated text example

    Below is an example of how to use the annotated_text function:
    """

    fem_words=['support','responsible']
    masculin_words=['leader', 'objectives']
    neutral_words=['innovative']
    #company_culture =["supportive", "collaborative", "team", "values", "culture"]
    #inclusivity=["transparent", "fair", "open", "inclusive", "equal"]
    #flexiblity=["family", "children", "healthcare", "home", "part time", "flexibel", "balance", "vacation"," maternity leave"],
    #personal_development=["development", "growth", "learning", "training"]

    job_description='We are looking for responsible part time leader with family for training our team who support innovative ideas in our objectives'
    #tokenized = word_tokenize(job_description)
    #st.dataframe(tokenized)

    List_for_annotation = []

    for word in job_description.split():
        if word in fem_words:
            List_for_annotation.append((word +' ', "female", "#faa"))

        elif word in masculin_words:
            List_for_annotation.append((word +' ', "male", "#8ef"))

        elif word in neutral_words:
            List_for_annotation.append((word +' ', "neutral", "#fea"))

        # if word in inclusivity:
        #     List_for_annotation.append((word+' ', "inclusivity", "##E8DAEF"))

        # if word in flexiblity:
        #     List_for_annotation.append((word+' ', "flexiblilty", "#CCCCFF"))

        # if word in personal_development:
        #     List_for_annotation.append((word+' ', "personal development", "#afa"))

        else:
            List_for_annotation.append(word +' ')


    # def convert(list):
    #     return tuple(i for i in list)

    # # Driver function
    # tuple_for_annotation= convert(List_for_annotation)

    # List_to_set = set(List_for_annotation)

    #annotated_text('Hello', annotation('world', 'female', "#8ef"))

    annotated_text(*List_for_annotation)

    # annotated_text(
    #     "This ",
    #     ("is", "male", "#8ef"),
    #     " some ",
    #     ("annotated", "adj", "#faa"),
    #     ("text", "noun", "#afa"),
    #     " for those of ",
    #     ("you", "pronoun", "#fea"),
    #     " who ",
    #     ("like", "verb", "#8ef"),
    #     " this sort of ",
    #     ("thing", "noun", "#afa"),
    # )
