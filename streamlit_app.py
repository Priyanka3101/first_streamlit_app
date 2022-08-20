import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

#streamlit.title('My Parents New Healthy Diner')
#streamlit.header('Breakfast Menu')
#streamlit.text('Omega 3 & Blueberry Oatmeal')
#streamlit.text('Kale, Spinach & Rocket Smoothie')
#streamlit.text('Hard-Boiled Free-Range Egg')

streamlit.title('My Moms New Healthy Diner')
streamlit.header('Breakfast Favourites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
#streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the table on the page.
#streamlit.dataframe(my_fruit_list)
streamlit.dataframe(fruits_to_show)


#creation of repeatable code block(called function)
def get_fruity_vice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized


# New section to display fruity vice api response
streamlit.header("Fruityvice Fruit Advice!")
try:
  #fruit_choice = streamlit.text_input('What fruit would you like information about?','apple')
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    #fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    #fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    back_from_function=get_fruity_vice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
    
except URLError as e:
  streamlit.error()
  
streamlit.header("The fruit load list contains :")
#Snowflake Related functions
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST")
    return my_cur.fetchall()
  
# Addition of button to load fruit list
if streamlit.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  streamlit.dataframe(my_data_rows)

  

    

  
    
    
#streamlit.write('The user entered ', fruit_choice)
#import requests
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "apple")
#streamlit.text(fruityvice_response.json()) # writes the data to the screen

# normalise the json version of the response
#fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# output on the screen as a table
#streamlit.dataframe(fruityvice_normalized)

#not running anything past this while we troubleshoot 
streamlit.stop()

#import snowflake.connector
#my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#my_cur = my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
#my_cur.execute("select * from PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST")
#my_data_row = my_cur.fetchone()
#streamlit.text("Hello from Snowflake:")
#streamlit.text("The fruit load list contains :")
#streamlit.text(my_data_row)

#my_data_rows = my_cur.fetchall()
#streamlit.header("The fruit load list contains :")
#streamlit.dataframe(my_data_rows)

# Allow the end user to add a fruit to the list
add_my_fruit= streamlit.text_input('What fruit would you like to add?','jackfruit')
streamlit.write('Thanks for adding the fruit ', add_my_fruit)
my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values('from streamlit')")
