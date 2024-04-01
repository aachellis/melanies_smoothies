# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col 

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """
Choose the fruits you want in your custom smoothie!
    """
)


name_on_order = st.text_input("Name on Smoothie: ")
st.write("The name of your smoothie will be: ", name_on_order)

session = get_active_session()
my_dataframe = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS").select(col("FRUIT_NAME"))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    "Choose upto 5 ingredients:",
    my_dataframe,
    max_selections = 5
)

time_to_insert = st.button("Submit Order")
if time_to_insert:
    if ingredients_list: 
        ingredients_string = " ".join(ingredients_list)
    
    else:   ingredients_string = ""
    st.write(ingredients_string)
    
    my_insert_stmt = f"""
    INSERT INTO SMOOTHIES.PUBLIC.ORDERS(INGREDIENTS, NAME_ON_ORDER)
    VALUES ('{ingredients_string}', '{name_on_order}');
    """


    if ingredients_string:  
        session.sql(my_insert_stmt).collect()
        st.success(f"Your smoothie is ordered, {name_on_order}!", icon = "✅")