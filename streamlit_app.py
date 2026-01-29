# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

# Get fruit options (badge way)
my_dataframe = session.table("smoothies.public.fruit_options") \
                      .select(col('FRUIT_NAME')) \
                      .collect()

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)

if ingredients_list and name_on_order:

    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen['FRUIT_NAME'] + ' '

    my_insert_stmt = f"""
        insert into smoothies.public.orders (ingredients, name_on_order)
        values ('{ingredients_string}', '{name_on_order}')
    """

    if st.button('Submit Order'):
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
