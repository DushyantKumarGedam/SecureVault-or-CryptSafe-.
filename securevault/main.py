from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
import os
from encryption_utils import EncryptionUtils

class CalculatorScreen(Screen):
    def __init__(self, **kwargs):
        super(CalculatorScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.result = TextInput(
            readonly=True, font_size=32, halign='right', multiline=False)
        self.layout.add_widget(self.result)

        buttons = [
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['.', '0', '=', '+']
        ]

        for row in buttons:
            h_layout = BoxLayout()
            for label in row:
                button = Button(text=label, on_press=self.on_button_press)
                h_layout.add_widget(button)
            self.layout.add_widget(h_layout)

        self.add_widget(self.layout)

    def on_button_press(self, instance):
        if instance.text == '=':
            try:
                self.result.text = str(eval(self.result.text))
            except Exception:
                self.result.text = "Error"
        else:
            self.result.text += instance.text

        if self.result.text == '1234':  # Secret code
            self.manager.current = 'password'

class PasswordScreen(Screen):
    def __init__(self, **kwargs):
        super(PasswordScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.label = Label(text="Enter Password", font_size=32)
        self.layout.add_widget(self.label)
        self.password_input = TextInput(password=True, multiline=False)
        self.layout.add_widget(self.password_input)
        self.submit_button = Button(text="Submit", on_press=self.check_password)
        self.layout.add_widget(self.submit_button)
        self.add_widget(self.layout)

    def check_password(self, instance):
        if self.password_input.text == 'password123':  # Example password
            self.manager.current = 'vault'
        else:
            self.label.text = "Incorrect Password, Try Again"

class VaultScreen(Screen):
    def __init__(self, **kwargs):
        super(VaultScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.utils = EncryptionUtils()  # Initialize encryption utils

        self.layout.add_widget(Label(text="Welcome to the Vault", font_size=32))
        
        self.filechooser = FileChooserIconView()
        self.layout.add_widget(self.filechooser)

        button_layout = BoxLayout(size_hint_y=None, height=50)
        
        add_file_button = Button(text="Add File", on_press=self.add_file)
        button_layout.add_widget(add_file_button)

        retrieve_file_button = Button(text="Retrieve File", on_press=self.retrieve_file)
        button_layout.add_widget(retrieve_file_button)

        self.layout.add_widget(button_layout)
        self.add_widget(self.layout)

    def add_file(self, instance):
        if self.filechooser.selection:
            filepath = self.filechooser.selection[0]
            with open(filepath, 'rb') as file:
                data = file.read()
                encrypted_data = self.utils.encrypt(data)
                encrypted_filepath = os.path.join(os.path.dirname(filepath), f"{os.path.basename(filepath)}.enc")
                with open(encrypted_filepath, 'wb') as enc_file:
                    enc_file.write(encrypted_data)
            
            popup = Popup(title='File Encrypted', content=Label(text=f'File has been encrypted and saved at {encrypted_filepath}'), size_hint=(None, None), size=(400, 400))
            popup.open()

    def retrieve_file(self, instance):
        if self.filechooser.selection:
            filepath = self.filechooser.selection[0]
            if not filepath.endswith('.enc'):
                popup = Popup(title='Error', content=Label(text='Please select a valid encrypted file (.enc)'), size_hint=(None, None), size=(400, 400))
                popup.open()
                return

            with open(filepath, 'rb') as file:
                encrypted_data = file.read()
                try:
                    decrypted_data = self.utils.decrypt(encrypted_data)
                    original_filepath = filepath[:-4]  # Remove the .enc extension
                    with open(original_filepath, 'wb') as dec_file:
                        dec_file.write(decrypted_data)
                    
                    popup = Popup(title='File Decrypted', content=Label(text=f'File has been decrypted and saved at {original_filepath}'), size_hint=(None, None), size=(400, 400))
                    popup.open()
                except Exception as e:
                    popup = Popup(title='Decryption Error', content=Label(text='Failed to decrypt the file.'), size_hint=(None, None), size=(400, 400))
                    popup.open()

class CalculatorApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(CalculatorScreen(name='calculator'))
        sm.add_widget(PasswordScreen(name='password'))
        sm.add_widget(VaultScreen(name='vault'))
        return sm

if __name__ == '__main__':
    CalculatorApp().run()
