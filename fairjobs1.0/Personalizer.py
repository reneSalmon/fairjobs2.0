import streamlit as st
import pandas as pd
import numpy as np
import re
import string
import requests
from PIL import Image

# app1.py


def app():

    st.title('Personalizer')
    st.markdown(
    '''
    Which problem did we want to solve?
    What is it doing?
    What did we do?
    What was the biggest challenge?
    ''')

    #fairjobs logo
# image = Image.open('./images_website/fairjobs_logo.png')
#  st.image(image)
