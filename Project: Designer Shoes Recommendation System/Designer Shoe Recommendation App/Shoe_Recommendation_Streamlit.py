import streamlit as st
import os
import pandas as pd
from PIL import Image
import plotly.express as px
import snowflake.connector
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import ast
import numpy as np



st.title('Designer Shoe Market')

#text_input

functionalities = ["Set Preferences", "See Similar Products"]
selected_func = st.sidebar.radio('I want to: ', functionalities)

pages = ["Product Image", "Product Name"]
section = st.sidebar.radio('See similar products based on ', pages)

# Images are stored in github for retrieval
base_image_url = 'https://raw.githubusercontent.com/aakash-atnoorkar/Team5_INFO7374_Spring2021/main/Project%3A%20Designer%20Shoes%20Recommendation%20System/Designer%20Shoe%20Recommendation%20App/images/'

# Connection to Snowflake
def create_snowflake_connection():
    #create connection
    conn=snowflake.connector.connect(
                user=os.getenv('USER'),
                password=os.getenv('PASSWORD'),
                account=os.getenv('ACCOUNT'),
                warehouse=os.getenv('WAREHOUSE'),
                database=os.getenv('DATABASE'),
                schema=os.getenv('SCHEMA')
                )
    #create cursor
    curs=conn.cursor()
    return curs

# Fetching queries
def fetch_results(curs, query):
    results = curs.execute(query).fetchall()
    return results

def get_recommendations(id):
    shoes_tfidf_group = pd.read_csv('https://raw.githubusercontent.com/aakash-atnoorkar/Team5_INFO7374_Spring2021/main/Project%3A%20Designer%20Shoes%20Recommendation%20System/Designer%20Shoe%20Recommendation%20App/shoes_tfidf_group.csv')
    shoes_tfidf_group = shoes_tfidf_group.set_index('id')
    cosine_sim = np.loadtxt('https://raw.githubusercontent.com/aakash-atnoorkar/Team5_INFO7374_Spring2021/main/Project%3A%20Designer%20Shoes%20Recommendation%20System/Designer%20Shoe%20Recommendation%20App/cosine_sim.npz')
    recommended_products = []
    index = indices[indices['id'] == id].index[0]
    score_series = pd.Series(cosine_sim[index]).sort_values(ascending = False)
    #print(score_series)
    top_similar_products = list(score_series.iloc[1:11].index)

    for i in top_similar_products:
        recommended_products.append(list(shoes_tfidf_group.index)[i])

    return recommended_products

def return_product_results(filtered_results):
    product_results = pd.DataFrame(columns = ['Id','Brand', 'Name', 'Avg_price'])
    lst = []
    for res in filtered_results:
        lst.append({'Id': res[0], 'Brand': res[1], 'Name': res[2], 'Avg_price': res[3]})
    product_results = product_results.append(lst)
    product_results = product_results.drop_duplicates(subset = 'Id')
    product_results = product_results.reset_index()
    return product_results

try:
    if selected_func == "Set Preferences":

        first,last = st.beta_columns(2)

        first_name = first.text_input("First Name")
        last_name = last.text_input("Last Name")

        gender = st.radio("Gender",("F","M"))

        #MultiSelect
        sizes =st.multiselect("Shoe Size",("5","5.5","6","6.5","7","7.5","8","8.5","9","9.5","10","10.5","11","11.5","12","12.5","14","15"))

        colors = st.multiselect("Color",("Brown","Navy","Taupe","Black","Red","White","Gray","Black Gray","Pewter","Grey","Stone",
        "Black White","Gold","Silver","Natural","Olive","Mushroom","Coral","Tan","Slate","Sand"))


        brands = st.multiselect("Brand",("skechers","so","adidas","puma","Reebok","Fila","FitFlop",
        "Jambu","eastland","new balance","croft barrow","simply vera vera wang","under armour","journee collection",
        "SKECHERS","candies","Propet","seven7","vans","keds","rampage",
        "Skechers","Kathlena","dr. scholls","easy street","a2 by aerosoles",
        "spring step","style charles by charles david","ryka","lifestride"))

        price_range=st.slider("What is your Price Range?",0,1000,(10,30),10)
        min_price = "{}".format(price_range[0])
        max_price="{}".format(price_range[1])

        button_start =st.button("Submit")

        if button_start:
            #query to display your records from database
            query = "select id,brand, name, avg_price from SHOES_DETAILS where PRICES_SIZE in " + str(tuple(sizes)).replace(',)',')')
            query += " and gender = \'" + gender + "\'"
            query += " and avg_price >= " + str(min_price)
            query += " and avg_price <= " + str(max_price)
            if len(colors) > 0:
                query += " and prices_color IN " + str(tuple(colors)).replace(',)',')')
            if len(brands) > 0:
                query += " and brand IN " + str(tuple(brands)).replace(',)',')')

            curs = create_snowflake_connection()
            filtered_results = fetch_results(curs, query)
            product_results = return_product_results(filtered_results)

            if len(product_results) > 0:
                st.markdown('##')
                st.header('Hey ' + first_name + '! Here are products for you! 😃')
                st.markdown('##')
                # Showing the initial results
                num_of_images = 4 if len(product_results) >= 4 else len(product_results)
                init_cols_1 = st.beta_columns(num_of_images)
                init_cols_2 = st.beta_columns(num_of_images)
                init_cols_3 = st.beta_columns(num_of_images)
                for index, row in product_results.iterrows():
                    if index < num_of_images:
                        img_link = base_image_url + row['Id'] + '.jpg'
                        init_cols_1[index].image(img_link, width=150)
                        init_cols_2[index].write(row['Name'].title())
                        init_cols_3[index].write('$' + str(row['Avg_price']).title())


                # Saving the preferences
                save_gender = "'" + gender + "'"
                save_sizes = "'" + str(sizes).replace('[','').replace(']','').replace('\'', '').replace(', ',',') + "'"
                save_min = "'" + str(min_price) + "'"
                save_max = "'" + str(max_price) + "'"
                save_colors = "'" + str(colors).replace('[','').replace(']','').replace('\'', '').replace(', ',',') + "'"
                #if len(save_colors) == 0:
                    #save_colors = "''"
                save_brands = "'" + str(brands).replace('[','').replace(']','').replace('\'', '').replace(', ',',') + "'"
                #if len(save_brands) == 0:
                    #save_brands = "''"

                save_first_name = "'" + first_name + "'"
                #if len(save_first_name) == 0:
                    #save_first_name = "''"

                #Clearing the preferences
                fetch_pref = 'truncate table user_preferences'
                curs = create_snowflake_connection()
                pref_result = fetch_results(curs, fetch_pref)
                store_pref_statement = "INSERT INTO USER_PREFERENCES values (" + save_gender + "," + save_sizes + "," + save_min + "," + save_max + "," + save_colors + "," + save_brands + "," + save_first_name + ")"
                fetch_results(curs, store_pref_statement)

            if len(product_results) == 0:
                st.info('Sorry! We couldn\'t match your choices 😶. Please tune your preferences!')







    if selected_func == "See Similar Products":
        #fetch preferences
        fetch_pref = 'select * from user_preferences limit 1'
        curs = create_snowflake_connection()
        pref_result = fetch_results(curs, fetch_pref)
        if len(pref_result) > 0:
            gender = pref_result[0][0]
            sizes = pref_result[0][1].split(',')
            min_price = pref_result[0][2]
            max_price = pref_result[0][3]
            colors = ''
            if pref_result[0][4] != '':
                colors = pref_result[0][4].split(',')
            brands = ''
            if pref_result[0][5] != '':
                brands = pref_result[0][5].split(',')
            first_name = pref_result[0][6]

            #query to display your records from database
            query = "select id,brand, name, avg_price from SHOES_DETAILS where PRICES_SIZE in " + str(tuple(sizes)).replace(',)',')')
            query += " and gender = \'" + gender + "\'"
            query += " and avg_price >= " + str(min_price)
            query += " and avg_price <= " + str(max_price)
            if colors != '':
                query += " and prices_color IN " + str(tuple(colors)).replace(',)',')')
            if brands != '':
                query += " and brand IN " + str(tuple(brands)).replace(',)',')')


            #curs = create_snowflake_connection()
            filtered_results = fetch_results(curs, query)
            product_results = return_product_results(filtered_results)

            product_id_list = []

            st.header('Hey ' + first_name + '! Here are products for you! 😃')
            st.markdown('##')
            # Showing the initial results
            num_of_images = 4 if len(product_results) >= 4 else len(product_results)
            ret_cols_1 = st.beta_columns(num_of_images)
            ret_cols_2 = st.beta_columns(num_of_images)
            ret_cols_3 = st.beta_columns(num_of_images)
            for index, row in product_results.iterrows():
                if index < num_of_images:
                    img_link = base_image_url + row['Id'] + '.jpg'
                    ret_cols_1[index].image(img_link, width=150)
                    ret_cols_2[index].write(row['Name'].title())
                    ret_cols_3[index].write('$' + str(row['Avg_price']).title())
                    product_id_list.append(row['Id'])

            # Showing the product Id in list because of the streamlit limitations
            image_selection_list = ['']
            image_selection_list.extend(product_id_list)

            selected = st.selectbox('Select an image:', image_selection_list, format_func=lambda x: 'Select an image here..' if x == '' else x)

            if selected:
                query = "select brand, name, avg_price from SHOES_DETAILS where id = \'" + selected + "\' limit 1"
                #curs = create_snowflake_connection()
                results = fetch_results(curs, query)
                #print('selected == ',results[0][0])
                selected_brand, selected_name, selected_price = results[0][0], results[0][1], results[0][2]

                if section == "Product Image":
                    query = "SELECT SIMILAR_PI, MASTER_PI, SIMILARITY_SCORE FROM SIMILARITY_SCORES WHERE MASTER_PI = \'" + selected + "\' AND SIMILARITY_SCORE!=1 ORDER BY SIMILARITY_SCORE DESC"

                    curs = create_snowflake_connection()
                    results = fetch_results(curs, query)
                    sim_products_score = []
                    for rec in results:
                        sim_products_score.append(rec[0])
                    sim_products_score = tuple(sim_products_score)

                    query = "select id,brand, name, avg_price from SHOES_DETAILS where id in " + str(sim_products_score).replace(',)',')')
                    query += " and gender = \'" + gender + "\'"
                    query += " and avg_price >= " + str(min_price)
                    query += " and avg_price <= " + str(max_price)
                    if colors != '':
                        query += " and prices_color IN " + str(tuple(colors)).replace(',)',')')
                    if brands != '':
                        query += " and brand IN " + str(tuple(brands)).replace(',)',')')


                    #Filtering the similar products based on preferences
                    filtered_results = fetch_results(curs, query)
                    product_results = return_product_results(filtered_results)

                    #if we get the results then following success
                    if len(filtered_results) > 0:
                        st.success('You have got a good taste in shoes! 🎉')
                    else:
                        #if we dont then display
                        query = "select id,brand, name, avg_price from SHOES_DETAILS where id in " + str(sim_products_score)
                        filtered_results = fetch_results(curs, query)
                        product_results = return_product_results(filtered_results)
                        st.info('Sorry! We couldn\'t match your preferences 😶. But here are products you might like!')

                if section == "Product Name":
                    indices = pd.read_csv('https://raw.githubusercontent.com/aakash-atnoorkar/Team5_INFO7374_Spring2021/main/Project%3A%20Designer%20Shoes%20Recommendation%20System/Designer%20Shoe%20Recommendation%20App/indices.csv')
                    recommended_products = get_recommendations(selected)
                    sim_products_score = tuple(recommended_products)
                    query = "select id,brand, name, avg_price from SHOES_DETAILS where id in " + str(sim_products_score).replace(',)',')')
                    query += " and gender = \'" + gender + "\'"
                    query += " and avg_price >= " + str(min_price)
                    query += " and avg_price <= " + str(max_price)
                    if colors != '':
                        query += " and prices_color IN " + str(tuple(colors)).replace(',)',')')
                    if brands != '':
                        query += " and brand IN " + str(tuple(brands)).replace(',)',')')

                    #Filtering the similar products based on preferences
                    filtered_results = fetch_results(curs, query)
                    product_results = return_product_results(filtered_results)

                    #if we get the results then following success
                    if len(filtered_results) > 0:
                        st.success('You have got a good taste in shoes! 🎉')
                    else:
                        #if we dont then display
                        query = "select id,brand, name, avg_price from SHOES_DETAILS where id in " + str(sim_products_score)
                        filtered_results = fetch_results(curs, query)
                        product_results = return_product_results(filtered_results)
                        st.info('Sorry! We couldn\'t match your preferences 😶. But here are products you might like!')

                col1, col2, col3 = st.beta_columns([1,3,4])

                with col1:
                    pass

                with col2:
                    st.image(base_image_url + selected + '.jpg', width=200)

                with col3:
                    st.header(selected_name.title())
                    st.write(selected_brand.title())
                    st.write('$' + str(selected_price))

                st.markdown('##')
                st.header('Here are similar products for you! 😃')
                st.markdown('##')
                #Get the similar images
                num_of_images = 4 if len(product_results) >= 4 else len(product_results)
                cols_1 = st.beta_columns(num_of_images)
                cols_2 = st.beta_columns(num_of_images)
                cols_3 = st.beta_columns(num_of_images)
                for index, row in product_results.iterrows():
                    if index < num_of_images:
                        img_link = base_image_url + row['Id'] + '.jpg'
                        cols_1[index].image(img_link, width=150)
                        cols_2[index].write(row['Name'].title())
                        cols_3[index].write('$' + str(row['Avg_price']).title())
        if len(pref_result) == 0:
            st.info("Yowza!! Seems like we don\'t have your preferences yet. Please submit your preferences in the \"Set Preferences\" section. 🙂")
except Exception as e:
    st.error('Oh no, Oh no, Oh no no no no no!')
    st.error('Sorry, some error has occurred, we recommend you to provide more preferences!')
