import speech_recognition as sr
import pyttsx3
import ctypes
import time

# Define the keyword to listen for
KEYWORD = input("Enter the stop word:")

# Define the function to stop music playback
def stop_music():
    # Send the WM_APPCOMMAND message to the currently active window to stop playback
    APPCOMMAND_MEDIA_STOP = 0xE0000
    hwnd = ctypes.windll.user32.GetForegroundWindow()
    ctypes.windll.user32.SendMessageTimeoutW(hwnd, 0x319, 0, APPCOMMAND_MEDIA_STOP, 0, 5000, None)

# Create a recognizer object and set the microphone as the audio source
r = sr.Recognizer()
with sr.Microphone() as source:
    # Adjust the microphone's sensitivity
    r.adjust_for_ambient_noise(source)
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()
    print("Listening for keyword '{}'...".format(KEYWORD))
    while True:
        try:
            # Listen for audio input
            audio = r.listen(source, phrase_time_limit=4)
            # Use Google Speech Recognition to transcribe the audio input
            text = r.recognize_google(audio)
            print("Recognized: {}".format(text))
            # Check if the keyword was spoken
            if text.lower() == KEYWORD:
                print("Stopping music playback...")
                stop_music()
                # Speak the response phrase in the voice
                engine.say(f"{KEYWORD} Someone is calling you")
                engine.runAndWait()
        except sr.UnknownValueError:
            # Ignore audio input that could not be transcribed
            pass
        except sr.RequestError as e:
            print("Error: {}".format(e))
        # Wait for a short time before listening again
        time.sleep(0.05)

