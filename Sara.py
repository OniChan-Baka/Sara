# imports
import requests
from Key import info
import pyttsx3
import speech_recognition as sr


# Initialize text-to-speech engine and set voice to use
def speak(phrase):
    engine = pyttsx3.init()
    voice = engine.getProperty('voices')
    engine.setProperty('voices', voice[0].id)
    engine.setProperty('rate', 200)
    # Say the phrase and wait for the engine to finish
    if phrase is not None:
        engine.say(phrase)
        engine.runAndWait()


# Record audio from the microphone and return the recognized speech as a string
def speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Recognizing...")
        audio = r.listen(source)
    try:
        # Use Google's Speech Recognition API to transcribe the audio
        output = r.recognize_google(audio)
        return output
    except sr.UnknownValueError:
        # If the API can't understand the audio, do nothing
        pass
    except sr.RequestError:
        # If there is an error with the API, do nothing
        pass


# Send a GET request to the API with a message
def req(msg):
    reply = None
    try:
        # Check that the "API URL" key is present in the info dictionary
        if "API URL" in info:
            url = info["API URL"]
            # Replace '[msg]' in the API URL with the message
            urlf = url.replace("[msg]", msg)
            # Send the GET request with a timeout of 5 seconds and return the response text
            reply = requests.get(urlf, timeout=5).text
            # Strip the response text of its surrounding quotes and curly braces
            reply = reply.strip('{"cnt":""}')
            print(reply)
    except (TypeError, requests.exceptions.RequestException):
        # If there is a TypeError or a request exception, do nothing
        pass
    return reply


# Main function
def main():
    # Run indefinitely
    speak("Sara v1 is activated")
    while True:
        # Get the recognized speech and send it to the API
        # Then speak the response from the hello API
        output = speech()
        if output is not None:
            response = req(output)
            if response is not None:
                speak(response)


# If this script is run directly (not imported), run the main function
if __name__ == '__main__':
    main()
