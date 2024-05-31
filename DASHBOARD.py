import streamlit as st
import util,json
# Title of the web app
st.title("Autobots - Kaizen Claims")



# Input text box

with open('prompts.json', 'r') as file:
    # Parse the JSON data
    promptLibrary = json.load(file)

#promptLibrary['USER_INTENT_RECOGNITION']

# Slider
#age = st.slider("Select your age", 0, 100, 25)

options = ["en-US","ja-JP"]
selected_option = st.selectbox("Choose user language.", options)

# Display the selected option
st.write(f"User Language: {selected_option}")
# Button
step = 0
if st.button("Intent Recognition"):
    util.respondtoUser("Hello! Welcome to Kaizen Cliams - How may I assist you.")
    st.write("Please speak.")
    userCall = util.recognize_from_microphone(selected_option)
    #st.write("STEP "+str(step) + " : "+userCall)

    userIntent = util.prompt_Creation(userCall,promptLibrary['USER_INTENT_RECOGNITION'],.2)
    st.write(userIntent)
    if userIntent == 'Not Known':
        gatheruserIntent = util.prompt_Creation('Not Known',promptLibrary['EXTRACT_INTENT'],.1)
        st.write(gatheruserIntent)

        util.respondtoUser(gatheruserIntent)
        userCall_Retry = util.recognize_from_microphone(selected_option)
        userIntentRetry = util.prompt_Creation(userCall_Retry,promptLibrary['USER_INTENT_RECOGNITION'],.2)
        st.write(userIntentRetry)


if st.button('Natural Conversation with user'):
## START NATURAL DIALOGUE
    messages = st.container()

    with open('questions.json', 'r') as file:
# Parse the JSON data
        listOfQues = json.load(file)
    #print(promptLibrary)
    listOfKeyPhrases = {}
    for ques in listOfQues:
        listOfKeyPhrases[ques] = util.prompt_to_question(ques)

    extractKYC = "You are a expert call centre agent and have the folloing text :"
    whatWeNeed = "If present extract name, date , age, gender,number from the text"
    receivedKYC = {}
    for kyc,question in listOfKeyPhrases.items():
        #st.write('Respond to queries')
        messages.chat_message("assistant").write(question)
        util.respondtoUser(question)
        userResponse = util.recognize_from_microphone()
        messages.chat_message("user").write(userResponse)
        kyc_FromResponse = util.prompt_Creation("Extract "+kyc+" from the text",extractKYC+userResponse+" just return extracted entity text and dont repeat the provided text.",.1)
        receivedKYC[kyc] = kyc_FromResponse
    st.write(receivedKYC)
    

uploaded_file_bytes = st.file_uploader("Choose a file")
if uploaded_file_bytes is not None:
    with st.spinner('Image being scanned for details...'):
        extractedJson = util.extractFromForm(uploaded_file_bytes)
        st.write(extractedJson)
        st.success('Done!')
    uploaded_file_bytes = None
    