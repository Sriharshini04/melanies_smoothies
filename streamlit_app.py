import streamlit as st
st.set_page_config(page_title="Melanie's Smoothies", page_icon="🥤")
st.title("🥤 Customize Your Smoothie 🥤")
st.write("Choose the fruits you want in your custom Smoothie!")
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:",name_on_order)
cnx = st.connection("snowflake")
session = cnx.session()
fruit_df = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS") \
                   .select("FRUIT_NAME") \
                   .to_pandas()

fruit_list = fruit_df["FRUIT_NAME"].tolist()
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_list,
    max_selections=5
)

submit_button = st.button("Submit Order")

if submit_button:
    if not name_on_order:
        st.error("Please enter a name for your Smoothie")
    elif len(ingredients_list) == 0:
        st.error("Please select at least 1 ingredient")
    else:
        ingredients_string = ", ".join(ingredients_list)

        insert_stmt = f"""
            INSERT INTO SMOOTHIES.PUBLIC.ORDERS (INGREDIENTS, NAME_ON_ORDER)
            VALUES ('{ingredients_string}', '{name_on_order}')
        """
        session.sql(insert_stmt).collect()
        st.success("✅ Your Smoothie order has been placed!")
        st.write("🥤 Ingredients:", ingredients_string)

import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
# st.text(smoothiefroot_response.json)
sf_df = st.dataframe(
    data=smoothiefroot_response.json(),
    use_container_width=True
)
