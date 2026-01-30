# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col, when_matched

# Write directly to the app
st.title("🥤 Pending Smoothie Orders 🥤")
st.write("Orders that need to be filled.")

# Create Snowflake connection
cnx = st.connection("snowflake")
session = cnx.session()

# Get pending orders
my_dataframe = (
    session
    .table("smoothies.public.orders")
    .filter(col("ORDER_FILLED") == 0)
    .collect()
)

if my_dataframe:
    editable_df = st.data_editor(my_dataframe)
    submitted = st.button("Submit")

    if submitted:
        og_dataset = session.table("smoothies.public.orders")
        edited_dataset = session.create_dataframe(editable_df)

        try:
            og_dataset.merge(
                edited_dataset,
                og_dataset["ORDER_UID"] == edited_dataset["ORDER_UID"],
                [when_matched().update(
                    {"ORDER_FILLED": edited_dataset["ORDER_FILLED"]}
                )]
            )
            st.success("Order(s) Updated!", icon="👍")
        except Exception as e:
            st.error("Something went wrong while updating orders.")
            st.write(e)

else:
    st.success("There are no pending orders right now 👍")
