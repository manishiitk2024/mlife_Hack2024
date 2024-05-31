import streamlit as st
import util,json
import os
import time
# Title of the web app
# Function to load JSON data with caching

smallKYC = {"name":None,"date":None,"plicyNumber":None}

with open('questions.json', 'r') as file:
        listOfQues = json.load(file)


with open('data.json','r') as file:
            msterList = json.load(file)
            msterListOfQuestions = msterList['questions']

smallList = list(msterListOfQuestions[0:4])

def chat_interface(smallList):
    options = ["en-US","ja-JP"]
    selected_option = st.selectbox("Choose user language.", options)
    
    messages = st.container()
    
    welcomeMsg = "Hello! Welcome to Kaizen Cliams - How may I assist you."
    messages.chat_message("assistant").write(welcomeMsg)
    util.respondtoUser(welcomeMsg)

    userCall = util.recognize_from_microphone(selected_option)
    messages.chat_message("user").write(userCall)

    util.respondtoUser(smallList[0])
    messages.chat_message("assistant").write(smallList[0])

    ## Small KYC
    

    cntr = 1
    for kyc in smallKYC.keys():
         util.respondtoUser(smallList[cntr])
         messages.chat_message("assistant").write(smallList[cntr])


         responseFromUserForKYC = util.recognize_from_microphone(selected_option)
         messages.chat_message("user").write(responseFromUserForKYC)

         extractKYC = "You are a expert call centre agent who can extract KYC details such name, date, policy number from user response. Just return the KYC and dont repeat the whole text."
    
         ## Extract and update KYC
         kyc_FromResponse = util.prompt_Creation(responseFromUserForKYC,extractKYC,.1)
         smallKYC[kyc] = kyc_FromResponse
         cntr += 1
         
    uploadDocs = "Please upload the bills and forms."
    util.respondtoUser(uploadDocs)
    util.respondtoUser("Please wait while we fill the form for you.")


@st.cache_data()
def scrollable_list():
     with st.container(border=True):
          st.write(list(msterListOfQuestions))
        
     

def main():
    # Set up the two-column layout
    col1, col2, col3= st.columns(3,gap="medium")
    

    with col1:
        st.markdown('Customer Interface')
        if st.button('Natural Conversation with user'):
              chat_interface(smallList)

    with col2:
        with st.spinner('Fetching User Case KYC Questions.'):
            time.sleep(10) 
            st.markdown('Master Question List')
            scrollable_list()  # Right column: Scrollable list

    with col3:
        st.markdown('Retrieved Responses')
        time.sleep(2)
        st.markdown(smallKYC)
        
        uploaded_file_bytes = st.file_uploader("Choose a file")
        if uploaded_file_bytes is not None:
            with st.spinner('Image being scanned for details...'):
                extractedJson = util.extractFromForm(uploaded_file_bytes)
                st.write(extractedJson)
                st.success('Done!')
            uploaded_file_bytes = None
            st.markdown(extractedJson)

main()