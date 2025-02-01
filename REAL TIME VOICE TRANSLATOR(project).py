from flask import Flask, render_template_string
import pyaudio
import pyttsx3
import speech_recognition as s_r
from googletrans import Translator as Trans
from gtts import gTTS
import os
from playsound import playsound as PS
import traceback
import threading

app = Flask(__name__)

# Initialize pyttsx3 for text-to-speech (TTS)
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Define the function to speak the text using pyttsx3
def speak(audio):
    def speak_thread(audio):
        engine.say(audio)
        engine.runAndWait()

    # Start a new thread to speak
    t = threading.Thread(target=speak_thread, args=(audio,))
    t.start()

# Function to listen to user's voice command
def take_command():
    recognizer = s_r.Recognizer()
    with s_r.Microphone() as source:
        print("Adjusting microphone...")
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Calibrate for ambient noise (1 second)
        print("Listening...")
        recognizer.pause_threshold = 1  # Short pause to detect when the user stops speaking
        recognizer.energy_threshold = 400  # Lower threshold (more sensitive)
        
        try:
            # Increase timeout to 10 seconds for better responsiveness
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)  # Timeout and phrase limit
        except s_r.WaitTimeoutError:
            print("Listening timed out. Please try again.")
            speak("Listening timed out. Please try again.")
            return "None"
        except Exception as e:
            print(f"Error during listening: {e}")
            speak("An error occurred while listening.")
            traceback.print_exc()
            return "None"
        
    try:
        print("Recognizing your voice...")
        speak("Recognizing your voice...")
        query = recognizer.recognize_google(audio, language='en-in')  # Change language code if needed
        print(f"User said: {query}")
    except s_r.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        speak("Sorry, I could not understand the audio.")
        return "None"
    except s_r.RequestError as e:
        print(f"Could not request results; check your internet connection: {e}")
        speak("Could not request results; check your internet connection.")
        return "None"
    except Exception as e:
        print(f"Error during recognition: {e}")
        speak("An error occurred while recognizing your voice.")
        traceback.print_exc()
        return "None"
    return query

# Function to get the language the user wants to translate to
def destination_language():
    print("Please choose the language you want to convert the above input into. Example: English, Hindi, German, French etc.")
    to_language = take_command()
    while (to_language == "None"):
        to_language = take_command()
    to_language = to_language.lower()
    return to_language

# Predefined languages dictionary
dic_language = ('afrikaans', 'af', 'albanian', 'sq', 'amharic', 'am', 'arabic', 'ar', 'armenian', 'hy', 'azerbaijani', 'az', 'basque', 'eu', 'belarusian', 'be', 'bengali', 'bn', 'bosnian', 'bs', 'bulgarian', 'bg', 'catalan', 'ca', 'cebuano', 'ceb', 'chichewa', 'ny', 'chinese (simplified)', 'zh-cn', 'chinese (traditional)', 'zh-tw', 'corsican', 'co', 'croatian', 'hr', 'czech', 'cs', 'danish', 'da', 'dutch', 'nl', 'english', 'en', 'esperanto', 'eo', 'estonian', 'et', 'filipino', 'tl', 'finnish', 'fi', 'french', 'fr', 'frisian', 'fy', 'galician', 'gl', 'georgian', 'ka', 'german', 'de', 'greek', 'el', 'gujarati', 'gu', 'haitian creole', 'ht', 'hausa', 'ha', 'hawaiian', 'haw', 'hebrew', 'he', 'hindi', 'hi', 'hmong', 'hmn', 'hungarian', 'hu', 'icelandic', 'is', 'igbo', 'ig', 'indonesian', 'id', 'irish', 'ga', 'italian', 'it', 'japanese', 'ja', 'javanese', 'jw', 'kannada', 'kn', 'kazakh', 'kk', 'khmer', 'km', 'korean', 'ko', 'kurdish (Kurmanji)', 'ku', 'kyrgyz', 'ky', 'lao', 'lo', 'latin', 'la', 'latvian', 'lv', 'lithuanian', 'lt', 'luxembourgish', 'lb', 'macedonian', 'mk', 'malagasy', 'mg', 'malay', 'ms', 'malayalam', 'ml', 'maltese', 'mt', 'maori', 'mi', 'marathi', 'mr', 'mongolian', 'mn', 'myanmar (burmese)', 'my', 'nepali', 'ne', 'norwegian', 'no', 'odia', 'or', 'pashto', 'ps', 'persian', 'fa', 'polish', 'pl', 'portuguese', 'pt', 'punjabi', 'pa', 'romanian', 'ro', 'russian', 'ru', 'samoan', 'sm', 'scots gaelic', 'gd', 'serbian', 'sr', 'sesotho', 'st', 'shona', 'sn', 'sindhi', 'sd', 'sinhala', 'si', 'slovak', 'sk', 'slovenian', 'sl', 'somali', 'so', 'spanish', 'es', 'sundanese', 'su', 'swahili', 'sw', 'swedish', 'sv', 'tajik', 'tg', 'tamil', 'ta', 'telugu', 'te', 'thai', 'th', 'turkish', 'tr', 'ukrainian', 'uk', 'urdu', 'ur', 'uyghur', 'ug', 'uzbek', 'uz', 'vietnamese', 'vi', 'welsh', 'cy', 'xhosa', 'xh', 'yiddish', 'yi', 'yoruba', 'yo', 'zulu', 'zu')

# Route to render the UI page
@app.route('/')
def home():
    return render_template_string('''  
    <html>
        <head>
            <title>Voice Command Recognition</title>
            <style>
                 h1 { 
                        font-size: 56px; 
                        color: #1ca6f7; 
                        filter: drop-shadow(0px 0px 10px #11abda);
                    }
                    div { 
                        margin-top: 20px; 
                        background-color: #3A1F4D;
                    }
                    body { 
                        text-align: center; 
                        color: white; 
                        font-family: Arial, sans-serif; 
                        padding: 50px; 
                        background-color: #3A1F4D; 
                    }
                    button { 
                        font-weight: bolder; 
                        font-size: 20px; 
                        padding: 15px 30px; 
                        cursor: pointer; 
                        color: white; 
                        background-color: #7127BA; 
                        border-radius: 20px;
                    }

                    .bulb-container {
                        text-align: center;
                        margin-top: 15%;
                    }

                    .bulb {
                        width: 90px;
                        height: 110px;
                        background: radial-gradient(circle, #fff, #ffeb3b, #fbc02d);
                        border-radius: 50% 50% 45% 45%;
                        position: relative;
                        box-shadow: 0 0 30px #ffeb3b;
                        transition: box-shadow 0.3s ease, background 0.3s ease;
                        margin: 20px auto;
                    }

                    .bulb::after {
                        content: '';
                        position: absolute;
                        bottom: -20px;
                        left: 35%;
                        width: 30px;
                        height: 40px;
                        background: black;
                        border-radius: 5px;
                    }

                    .off {
                        background: black;
                        box-shadow: none;
                    }
                    #bulb-1{
                        font-weight: bolder; 
                        font-size: 10px; 
                        padding: 5px 10px; 
                        cursor: pointer; 
                        color: white; 
                        background-color: #c51414; 
                        border-radius: 50px;
                    }
            </style>
        </head>
        <body>
            <div class="bulb-container">
                <div class="bulb" id="bulb"></div>
                <button id="bulb-1" onclick="toggleBulb()">Touch</button>
            </div>
             <div>
                <h1>Voice Command Recognition App</h1>
                <p>Click the button below to start listening for your voice command:</p>
                <button onclick="window.location.href='/start-listening'">Start Listening</button>
            </div>
            <script>
                function toggleBulb() {
                    const bulb = document.getElementById('bulb');
                    bulb.classList.toggle('off');
                }
            </script>
        </body>
    </html>
    ''')

# Route to handle button click and start listening
@app.route('/start-listening')
def start_listening():
    try:
        print("Starting the listening process...")
        query_1 = take_command()
        while query_1 == "None":
            query_1 = take_command()

        to_language = destination_language()

        while to_language not in dic_language:
            print("The language in which the user wants to convert the voice command is currently not available.")
            speak("The language is not available. Please input another language.")
            to_language = destination_language()

        to_language = dic_language[dic_language.index(to_language) + 1]  # Get corresponding language code

        # Translate the text
        translator1 = Trans()
        text_to_translate_1 = translator1.translate(query_1, dest=to_language)
        translated_text = text_to_translate_1.text

        # Convert translated text to speech (TTS)
        tts_speech = gTTS(text=translated_text, lang=to_language, slow=False)

        # Save the speech as an MP3 file
        tts_speech.save("captured_JTP_voice.mp3")

        # Play the MP3 file
        PS('captured_JTP_voice.mp3')

        # Delete the MP3 file after playing it
        os.remove('captured_JTP_voice.mp3')

        # Print the translated text
        print(f"Translated Text: {translated_text}")
        return f"Recognized and Translated Text: {translated_text}"
    except Exception as e:
        print(f"Error during the listening or translation process: {e}")
        traceback.print_exc()
        speak("An error occurred during the process. Please try again.")
        return "An error occurred during the process. Please try again."

# Enable threading to handle blocking operations in Flask
if __name__ == '__main__':
    app.run(debug=True, threaded=True)
