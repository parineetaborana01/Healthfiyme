import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
import pandas as pd

#Lets get the api key from environment
gemini_api_key=os.getenv('Gemini API Key2')

#lets configure the model
model=ChatGoogleGenerativeAI(
    model='gemini-2.5-flash-lite',
    api_key=gemini_api_key
)

# Design the UI of application
st.title(':green[Healthify me:] :orange[ Your Personal Health Assistant.]')
st.markdown('''
This application will assist you to get better and customized health advise.
You can ask your health related issues and get the perosnalised guidance.''' )          
st.write('''
Follow These Steps:
* Enter your details in sidebar.
* Rate your Activity and Fitness on the scale of 0-5.
* Submit Your Details
* Ask you question on the main page.
* click Generate and Relax.

'''            )

# Design the side bar for all the user parameters.
st.sidebar.header(':orange[Enter your Details]')
Name=st.sidebar.text_input('Enter your Name:')
Gender=st.sidebar.selectbox('Select Your Gender:',['Male','Female'])
age=st.sidebar.text_input('Enter your age:')
weight=st.sidebar.text_input('Enter your Weight in Kgs:')
height=st.sidebar.text_input('Enter your height in cms:')
bmi = pd.to_numeric(weight)/((pd.to_numeric(height)/100)**2)
active=st.sidebar.slider('Rate Your Activity :(0-5)',0,5,step=1)
fitness=st.sidebar.slider('Rate Your Fitness :(0-5)',0,5,step=1)

if st.sidebar.button('Submit'):
    st.sidebar.write(f"{Name},Your BMI is :{bmi} Kg/m^2")

# Lets use the Gemini Model to generate the report
user_input=st.text_input('Ask Me Your Question.')
prompt=f'''
<Role> You are an expert in health  and wellness and has 10+ years experience in Guiding People.
<Goal> Generate the customized report addressing the problem the user has asked.
Here is the Question that user has asked:{user_input}
<Context> here are the Details the user has provided.
Name={Name}
Age={age}
Gender={Gender}
Height={height}
Weight={weight}
BMI={bmi}
Activity rating(0-5)={active}
Fitness Rating(0-5)={fitness}


<format> Follwoing Should be outline of the report in the sequence 
* Start with the 2-3 line of comment on the details that user has provided.
* Explain What the Real problem could be on the basis of input the user has provided.
* Suggest the Possible Reasons for the problem what are the possible solutions.
* Mention the doctor from which specialization of a doctor can be visited if required.
* mention any change in the diet which is required .
* In last create a final summary of all the things that has been discussed in the report

<Instructions>
* Use the bullet points where ever possible.
* Create Tables to represent any data where ever possible.
* Strictly Do not advise any medicine.'''

if st.button('Generate'):
    response=model.invoke(prompt)
    st.write(response.content)
