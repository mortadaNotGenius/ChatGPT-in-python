import openai
import tkinter as tk
from tkinter import ttk
import threading

class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.openai_api_key = "API key"
        self.initUI()
        self.conversation = []
    def initUI(self):
        # Create text input and output fields
        self.input_field = tk.Text(self, width=65, height=13)
        self.input_field.pack()
        self.output_field = tk.Text(self, width=65, height=30)
        self.output_field.pack()

        # Create buttons
        clear_button = ttk.Button(self, text='Clear', command=self.clear_text)
        clear_button.pack()
        paste_button = ttk.Button(self, text='Paste', command=self.paste_text)
        paste_button.pack()
        copy_button = ttk.Button(self, text='Copy', command=self.copy_text)
        copy_button.pack()
        generate_button = ttk.Button(self, text='Generate', command=self.generate_response)
        generate_button.pack()

        # Set window properties
        self.title('ChatGPT')
        self.geometry('500x800')

    def clear_text(self):
        self.input_field.delete(0, 'end')
        self.output_field.delete('1.0', 'end')

    def paste_text(self):
        self.input_field.insert('end', self.clipboard_get())

    def copy_text(self):
        self.clipboard_clear()
        self.clipboard_append(self.output_field.get('1.0', 'end'))

    def generate_response(self):
        def generate():
            openai.api_key = self.openai_api_key
            ask = self.input_field.get('1.0', 'end')
            self.conversation.append(('Human:', ask))  # Add user's input to conversation
            prompt = ''
            for speaker, message in self.conversation:
                prompt += f"{speaker} {message}\n"
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                temperature=0.5,
                max_tokens=4000,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0.6,
                stop=[" Human:", " AI:"]
                )
            text = response['choices'][0]['text']
            self.conversation.append(('AI:', text))  # Add AI's response to conversation
            self.output_field.delete('1.0', 'end')
            self.output_field.insert('end', text)

        thread = threading.Thread(target=generate)
        thread.start()

if __name__ == '__main__':
    app = MyApp()
    app.mainloop()
