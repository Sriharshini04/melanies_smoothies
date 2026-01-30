# # Import python packages
# import streamlit as st
# from snowflake.snowpark.functions import col

# st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
# st.write("Choose the fruits you want in your custom Smoothie!")

# name_on_order = st.text_input('Name on Smoothie:')
# st.write('The name on your Smoothie will be:', name_on_order)

# cnx = st.connection("snowflake")
# session = cnx.session()

# # Get fruit options (badge way)
# my_dataframe = session.table("smoothies.public.fruit_options") \
#                       .select(col('FRUIT_NAME')) \
#                       .collect()

# ingredients_list = st.multiselect(
#     'Choose up to 5 ingredients:',
#     my_dataframe,
#     max_selections=5
# )

# if ingredients_list and name_on_order:

#     ingredients_string = ''
#     for fruit_chosen in ingredients_list:
#         ingredients_string += fruit_chosen['FRUIT_NAME'] + ' '

#     my_insert_stmt = f"""
#         insert into smoothies.public.orders (ingredients, name_on_order)
#         values ('{ingredients_string}', '{name_on_order}')
#     """

#     if st.button('Submit Order'):
#         session.sql(my_insert_stmt).collect()
#         st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")

import streamlit as st

# ----------------------------------------
# Page config
# ----------------------------------------
st.set_page_config(page_title="Melanie's Smoothies", page_icon="🥤")

st.title("🥤 Customize Your Smoothie 🥤")
st.write("Choose the fruits you want in your custom Smoothie!")

# ----------------------------------------
# Input: Name on Smoothie
# ----------------------------------------
name_on_order = st.text_input("Name on Smoothie:")

st.write("The name on your Smoothie will be:")
st.write(name_on_order)

# ----------------------------------------
# Snowflake Connection (uses Streamlit Secrets)
# ----------------------------------------
cnx = st.connection("snowflake")
session = cnx.session()

# ----------------------------------------
# Get fruit options from Snowflake
# ----------------------------------------
fruit_df = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS") \
                   .select("FRUIT_NAME") \
                   .to_pandas()

fruit_list = fruit_df["FRUIT_NAME"].tolist()

# ----------------------------------------
# Fruit selection (MAX 5)
# ----------------------------------------
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_list,
    max_selections=5
)

# ----------------------------------------
# Submit Button
# ----------------------------------------
submit_button = st.button("Submit Order")

# ----------------------------------------
# Submit Logic
# ----------------------------------------
if submit_button:

    if not name_on_order:
        st.error("Please enter a name for your Smoothie")

    elif len(ingredients_list) == 0:
        st.error("Please select at least 1 ingredient")

    else:
        # Convert list → string
        ingredients_string = ", ".join(ingredients_list)

        # Insert into Snowflake
        insert_stmt = f"""
            INSERT INTO SMOOTHIES.PUBLIC.ORDERS (INGREDIENTS, NAME_ON_ORDER)
            VALUES ('{ingredients_string}', '{name_on_order}')
        """

        session.sql(insert_stmt).collect()

        st.success("✅ Your Smoothie order has been placed!")
        st.write("🥤 Ingredients:", ingredients_string)

