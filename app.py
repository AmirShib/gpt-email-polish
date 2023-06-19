import streamlit as st 
from langchain import PromptTemplate, LLMChain
from langchain.llms import OpenAI
import os
from PIL import Image
from deep_translator import GoogleTranslator

template = """
    Below is an email that may be poorly worded.
    Your goal is to:
    - Properly format the email
    - Convert the input text to a specified tone

    Here are some examples different Tones:
    - Formal: We went to London for the weekend. We have a lot of things to tell you.
    - Informal: Went to London for the weekend. Lots to tell you.

    Please start the email with a warm introduction. Add the introduction if you need to.
    Please end the email with a closing phrase. Add the closing phrase if you need to.
    Make sure to take into account who the recipient is and adjust the message accordingly.
    
    Below is the email and tone:
    TONE: {tone}
    EMAIL: {email}
    
    YOUR RESPONSE:"""
 

def translate(input_text):
    # translate the text if it is not english
    translater = GoogleTranslator(source='auto', target='en')
    output_text = translater.translate(text=input_text)
    return output_text
    

def get_prompt(template):
    prompt = PromptTemplate(
        input_variables=["tone", "email"],
        template=template,
    )
    return prompt

def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(temperature=.7, openai_api_key=openai_api_key)
    return llm

st.set_page_config(page_title="Polish my Email", page_icon="✉️")
image = Image.open("assets/logo.png")
st.image(image, width=200)
st.header("Polish my Email :robot_face: :e-mail:")

col1, col2 = st.columns(2)

with col1:
    st.markdown("Writing an email in english is not easy for many people, especially when trying to write a fromal email. \n\n This tool \
                will help you improve your email skills by translating your email and/or converting it into a more professional format. \
                    \n\n Begin by writing the important sentences in your most comfortable language")
    

st.markdown("## Enter Your Email To Convert")

def get_tone():
    tone = st.selectbox(
        'Which tone would you like your email to have?',
        ('Formal', 'Informal'))
    return tone

with col2:
    option_tone = get_tone()
    
def get_key():
    input_text = st.text_input(label="OpenAI API Key ",  placeholder="Ex: sk-2twmA8tfCb8un4...", key="openai_api_key_input")
    return input_text
openai_api_key = get_key()
    
def get_text():
    input_text = st.text_area(label="Email Input", label_visibility='collapsed', placeholder="Your Email here")
    if input_text:
        translated_text = translate(input_text)
        return translated_text
    return input_text



email_input = get_text()
if len(email_input.split(" ")) > 500:
    st.write("Please enter a shorter email. The maximum length is 500 words.")
    st.stop()
    

def update_text_with_example():
    print ("is updated")
    st.session_state.email_input = "Sally I am starts work at yours monday from Gai"
    
st.button("*Generate email*", type='secondary', help="Click to see an example of the email you will be converting.", on_click=update_text_with_example)


st.markdown("### Your Converted Email:")

prompt = get_prompt(template)


if email_input:
    if not openai_api_key:
        st.warning('Please insert OpenAI API Key. Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', icon="⚠️")
        st.stop()

    llm = load_LLM(openai_api_key)

    prompt_with_email = prompt.format(tone=option_tone, email=email_input)

    formatted_email = llm(prompt_with_email)

    st.write(formatted_email)
