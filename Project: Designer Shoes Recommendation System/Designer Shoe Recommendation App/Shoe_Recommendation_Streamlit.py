import streamlit as st
import os
import pandas as pd
import altair as alt
import seaborn as sns
from PIL import Image
import plotly.express as px


st.title('Designer Shoe Recommendation System')

images = ['AV_A1j-CKZqtpbFMTMv3.jpg', 'AV_A2b1oKZqtpbFMTMza.jpg', 'AV_A2ve2Hh53nbDR_ugb.jpg', 'AV_A3W8wHh53nbDR_unp.jpg', 'AV_A4GPuuC1rwyj_g8Xg.jpg']
st.image(images, width=100, caption=images)

cols = st.beta_columns(5)
for idx, img in enumerate(images):

    cols[idx].image(images[idx], use_column_width=True, width=80, caption=idx+1)


image_selection_list = ['']
image_selection_list.extend(images)
selected = st.selectbox('Select an image:', image_selection_list, format_func=lambda x: 'Select an image here..' if x == '' else x)

if selected:
    #perform elastic search to get relevant images
    #if we get the results then following success
    st.success('Yay! 🎉')
    #if we dont then display
    st.info('This is a purely informational message')
    col1, col2 = st.beta_columns(2)

    with col1:
        st.image(selected, use_column_width=True, width=80, caption=selected)

    with col2:
        st.info("From Col2")
        my_year = st.number_input("Year",1995,2040)
        st.write(my_year)


    #Get the similar images
    cols_1 = st.beta_columns(5)
    for idx, img in enumerate(images):

        cols_1[idx].image(images[idx], use_column_width=True, width=80, caption=idx+1)
else:
    st.warning('No image is selected. Please select an image')
