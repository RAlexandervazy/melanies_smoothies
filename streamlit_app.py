# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col, when_matched

cnx = st.connection("snowflake")
session = cnx.session()

# Write directly to the app
st.title(":cup_with_straw: Pending Smoothies Orders :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

# name_on_order = st.text_input("Name on Smoothie")
# st.write("The name on your Smoothie will be", name_on_order)

#session = get_active_session()
my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()
editable_df = st.data_editor(my_dataframe)


submitted = st.button('submit')

if my_dataframe:
    if submitted:
        og_dataset = session.table("smoothies.public.orders")
        try:
            edited_dataset = session.create_dataframe(editable_df)
            og_dataset.merge(edited_dataset
                    , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                    , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                )
            st.success("Someone clicked the button.", icon="👍")
        except:
            st.write("Something went wrong.")
else:
    st.success("There are no pending orders right now",  icon="👍")
        
# ingredients_List = st.multiselect('Choose up to  5 ingredients:', my_dataframe)

# if ingredients_List:
#     ingredients_string = ''
#     for fruit_chosen in ingredients_List:
#         ingredients_string += fruit_chosen + ' '
#     # st.write(ingredients_string)
#     my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
#             values ('""" + ingredients_string + """', '""" + name_on_order + """')"""
#     st.write(my_insert_stmt)
#     #st.stop()

#     time_to_insert = st.button('Submit Order')
    
#     if time_to_insert:
#         session.sql(my_insert_stmt).collect()
#         st.success(f'Your Smoothie is ordered, {name_on_order}', icon="✅")
