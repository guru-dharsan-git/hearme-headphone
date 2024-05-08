from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
import threading
import speech_recognition as sr
import pyttsx3
import ctypes

KV = '''
BoxLayout:
    orientation: 'vertical'
    MDToolbar:
        title: 'Voice Command App'
    MDTextField:
        id: keyword_field
        hint_text: "Enter stop word"
        pos_hint: {'center_x': 0.5, 'center_y': 0.6}
        size_hint_x: 0.8
    MDRaisedButton:
        id: button
        text: 'Start Listening'
        pos_hint: {'center_x': 0.5, 'center_y': 0.4}
        on_release: app.start_listening()
'''

class VoiceCommandApp(MDApp):
    def build(self):
        self.root = Builder.load_string(KV)
        self.listening = False

    def start_listening(self):
        if not self.listening:
            self.listening = True
            self.keyword = self.root.ids.keyword_field.text.lower()
            self.root.ids.button.text = "Listening..."
            threading.Thread(target=self.listen).start()

    def listen(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            engine = pyttsx3.init()
            while self.listening:
                try:
                    audio = r.listen(source, phrase_time_limit=4)
                    text = r.recognize_google(audio)
                    if text.lower() == self.keyword:
                        self.stop_music()
                        engine.say(f"{self.keyword} Someone is calling you")
                        engine.runAndWait()
                except sr.UnknownValueError:
                    pass
                except sr.RequestError as e:
                    print("Error: {}".format(e))

    def stop_music(self):
        APPCOMMAND_MEDIA_STOP = 0xE0000
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        ctypes.windll.user32.SendMessageTimeoutW(hwnd, 0x319, 0, APPCOMMAND_MEDIA_STOP, 0, 5000, None)

VoiceCommandApp().run()
