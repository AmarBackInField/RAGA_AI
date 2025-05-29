import speech_recognition as sr
import pyttsx3
import os
import logging

logger = logging.getLogger(__name__)

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

        try:
            print("Converting speech to text...")
            text = recognizer.recognize_google(audio)
            print("You said:", text)
            return text
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None




# Globals for speech engine/thread
tts_engine = None
tts_thread = None

def text_to_speech(text):
    """
    Convert text to speech. Falls back gracefully if TTS is not available.
    """
    try:
        global tts_engine
        tts_engine = pyttsx3.init()
        tts_engine.setProperty('rate', 150)
        tts_engine.setProperty('volume', 1.0)
        logger.info("🔊 Speaking...")
        tts_engine.say(text)
        tts_engine.runAndWait()
    except RuntimeError as e:
        if "eSpeak" in str(e):
            logger.warning("Text-to-speech is not available (eSpeak not installed). This is normal in cloud environments.")
            # In a cloud environment, we could potentially use a different TTS service here
            # For now, we'll just log that TTS is not available
            return
        else:
            logger.error(f"Error in text-to-speech: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error in text-to-speech: {str(e)}")

