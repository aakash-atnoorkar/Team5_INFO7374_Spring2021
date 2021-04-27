#Images
from PIL import Image
import streamlit as st


st.title("Designer Shoe Market")
img = Image.open("C:\\Users\\pooja\\Downloads\\shoe.jpg")
st.image(img,width=500)

#text_input
first,last = st.beta_columns(2)

first.text_input("First Name")
last.text_input("Last Name")

st.text_input("Email")

st.radio("Gender",("Female","Male"))

#MultiSelect
st.multiselect("Shoe Size",("5","5.5","6","6.5","7","7.5","8","8.5","9","10"))
st.multiselect("Color",("Brown","Biege","Blue","Black","Red","Rinse","Gold","Pink Ribbon","Flower"))

Brand = st.multiselect("Brand",("Zoot","Wild Pair","Sutton Studio","LaLeela","Reebok","Jessica Simpson","The Highest Heel","Qupid","Alfani","Me Too","New Balance","Under Armour","Bruno Magli","Nine West","Celebrity Pink Jeans","Cheer Bunny","Easy Spirit","Touch Ups","Caterpillar","Dearfoams","Karma Canvas","Boulet","Comfy Feet","Allegra K","FIEL","Landau","Allegra K","FIEL","Easy Spirit","Unique Bargains","Crocs","Dream Girl","Skechers","Kathlena","Dan Post","Tkees","Big Accessories","Spring Step","Nike","Bali","Nina"))
st.write("You selected",len(Brand),"Brands")

#Slider
st.slider("What is your Price Range?",1,1000)

st.button("Submit")
