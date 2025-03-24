# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Chose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input("Name on Smoothie")
st.write("The name on the Smoothie will be ", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    "Chose up to 5 ingredients:",
    my_dataframe,
    max_selections = 5,
    #placeholder = 'choose smoothie ingredients',
    
)

#Test your multiselect. We tell them to choose up to 5 ingredients but we don't enforce that number limit. 

#📓 The Data Returned is both a list and a LIST
#We are placing the multiselect entries into a variable called "ingredients." We can then write "ingredients" back out to the screen.

#Our ingredients variable is an object or data type called a LIST. So it's a list in the traditional sense of the word, but it is also a datatype or object called a LIST. A LIST is different than a DATAFRAME which is also different from a STRING!

#We can use the st.write() and st.text() methods to take a closer look at what is contained in our ingredients LIST. 
if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    #st.write(my_insert_stmt) 
    #st.stop()
    
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, ' + name_on_order + '!', icon="✅" )
