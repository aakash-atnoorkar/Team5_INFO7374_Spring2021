#Images
from PIL import Image
import streamlit as st
import snowflake.connector as sf
from snowflake.connector import DictCursor
from PIL import Image
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
conn = sf.connect (user=' ',
    password='  ',
    account='  ')

def execute_query (connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    cursor.close()

st.title("Designer Shoe Market")
img = Image.open("C:\\Users\\pooja\\Downloads\\shoe.jpg")
st.image(img,width=500)

#text_input
first,last = st.beta_columns(2)

first_name=first.text_input("First Name")
last_name=last.text_input("Last Name")

email=st.text_input("Email")

gender=st.radio("Gender",("F","M"))

#MultiSelect
shoe_size=st.multiselect("Shoe Size",("5","5.5","6","6.5","7","7.5","8","8.5","9","9.5","10","10.5","11","11.5","12","12.5","14","15"))
length=len(shoe_size)
str=""
for i in range(0,length):
    str=str+shoe_size[i]
    if(i!=length-1):
        str=str+","

#Fetching Shoe_colors
color=st.multiselect("Color",("Brown","Navy","Taupe","Black","Red","White","Gray","Black Gray","Pewter","Grey","Stone",
"Black White","Gold","Silver","Natural","Olive","Mushroom","Coral","Tan","Slate","Sand"))
color_length=len(color)
color_str=""
for i in range(0,color_length):
    color_str=color_str+"'"
    color_str=color_str+color[i]
    color_str=color_str+"'"
    if(i!=color_length-1):
        color_str=color_str+","

#Fetching Shoe_Brands
Brand = st.multiselect("Brand",("skechers","so","adidas","puma","Reebok","Fila","FitFlop",
"Jambu","eastland","new balance","croft barrow","simply vera vera wang","under armour","journee collection",
"SKECHERS","candies","Propet","seven7","vans","keds","rampage",
"Skechers","Kathlena","dr. scholls","easy street","a2 by aerosoles",
"spring step","style charles by charles david","ryka","lifestride"))
brand_length=len(Brand)
brand_str=""
for i in range(0,brand_length):
    brand_str=brand_str+"'"
    brand_str=brand_str+Brand[i]
    brand_str=brand_str+"'"
    if(i!=brand_length-1):
        brand_str=brand_str+","



#Slider
price_range=st.slider("What is your Price Range?",1,1000,(10,30),1)
low="{}".format(price_range[0])
high="{}".format(price_range[1])
button_start =st.button("Submit")
if button_start:
    sql = 'use {}'.format ('SHOEMARKET')
    execute_query (conn, sql)

    sql = 'use warehouse {}'.format ('compute_wh')
    execute_query (conn, sql)

    #query to display your records from database
    sql = "select distinct id from SHOES_DETAILS where prices_size IN("+str+")and gender='"+gender+"'"  #tablename is the name of the table in your snowflake database
    sql += " and avg_price >= " + low
    sql += " and avg_price <= " + high
    if color_str!="":
        sql+= " and prices_color IN ("+color_str+")"
    if brand_str!="":
        sql+= " and brand IN ("+brand_str+")"

    cursor = conn.cursor(DictCursor)
    cursor.execute(sql)
    count=1
    for c in cursor:
        if count<=4:
            base_image_url = 'https://raw.githubusercontent.com/aakash-atnoorkar/Team5_INFO7374_Spring2021/main/Project%3A%20Designer%20Shoes%20Recommendation%20System/Designer%20Shoe%20Recommendation%20App/images/'
            base_image_url=base_image_url+c["ID"]+".jpg"
            st.image(base_image_url,width=150)
            count=count+1
