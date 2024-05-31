from openai import OpenAI
import azure.cognitiveservices.speech as speechsdk

from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient




import json

with open("prompts.json", "r") as file:
    # Parse the JSON data
    promptLibrary = json.load(file)

promptLibrary["USER_INTENT_RECOGNITION"]


client = OpenAI(api_key=OPENAI_API_KEY)
global speech_config
speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)


def recognize_from_microphone(locale="en-US"):
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    # speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))

    speech_config.speech_recognition_language = locale  # ja-JP | en-US

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )

    print("Speak into your microphone.")
    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(speech_recognition_result.text))
        return speech_recognition_result.text
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print(
            "No speech could be recognized: {}".format(
                speech_recognition_result.no_match_details
            )
        )
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")
    return "NO CONTENT RECOGNIZED"


def respondtoUser(text):
    speech_config.speech_synthesis_voice_name = "en-US-AvaMultilingualNeural"

    # Creates a speech synthesizer using the default speaker as audio output.
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    # Synthesizes the received text to speech.
    # The synthesized speech is expected to be heard on the speaker with this line executed.
    result = speech_synthesizer.speak_text_async(text).get()

    # Checks result.
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        # print("Speech synthesized to speaker for text [{}]".format(text))
        return True
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
        print("Did you update the subscription info?")
    return False


def prompt_to_question(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a professional chatbot, given a input convert it to a relevant question.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=50,  # Limit the maximum length of the generated question
        temperature=0.1,  # Controls the randomness of the generated text
        n=1,  # Generate only one response
        stop=None,  # Stop generation at a specific token
    )
    return response.choices[0].message.content


def prompt_Creation(query, prmpt, temp=0.1):

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prmpt},
            {"role": "user", "content": query},
        ],
        max_tokens=75,  # Limit the maximum length of the generated question
        temperature=temp,  # Controls the randomness of the generated text
        n=1,  # Generate only one response
        stop=None,  # Stop generation at a specific token
    )
    return response.choices[0].message.content


def extractFromForm(imageFile):
    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )
    fileBytes = imageFile.read()
# result = document_client.begin_analyze_document(document_data)
# poller = document_analysis_client.begin_analyze_document_from_url("prebuilt-document", formUrl)
    poller = document_analysis_client.begin_analyze_document(
        "prebuilt-document", fileBytes
    )
    result = poller.result()

    # valuesToExtract = ['ADDRESSEE','STATEMENT DATE','PATIENT NAME','HOSPITAL NAME','FROM','Laboratory General','TOTAL CHARGES','']

    computerVision_FormOCR = {}

    # print("----Key-value pairs found in document----")
    for kv_pair in result.key_value_pairs:
        if kv_pair.key and kv_pair.value:
            # print("Key '{}': Value: '{}'".format(kv_pair.key.content, kv_pair.value.content))
            # if kv_pair.key.content in valuesToExtract:
            computerVision_FormOCR[kv_pair.key.content] = kv_pair.value.content

    return computerVision_FormOCR
