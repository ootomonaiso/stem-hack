import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext
from PIL import Image, ImageTk
import random
import json
import pyttsx3

engine = pyttsx3.init()

class MarkovChainTextGenerator:
    def __init__(self):
        self.chain = None

    def build_chain(self, data_files):
        chain = {}
        for data_file in data_files:
            with open(data_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
            for sentence in data["sentences"]:
                words = ["<START>"] + sentence + ["<END>"]
                for i in range(len(words) - 1):
                    current_word = words[i]
                    next_word = words[i + 1]
                    if current_word not in chain:
                        chain[current_word] = []
                    chain[current_word].append(next_word)
        self.chain = chain

    def generate_text(self, max_length=100):
        if self.chain is None:
            return "Error: Chain not built. Please load data first."
        
        text = []
        current_word = "<START>"
        while len(text) < max_length:
            if current_word not in self.chain:
                break
            next_word_options = self.chain[current_word]
            next_word = random.choice(next_word_options)
            if next_word == "<END>":
                break
            text.append(next_word)
            current_word = next_word
        return " ".join(text)

def select_files(text_widget, retry_button):
    global generator
    file_paths = filedialog.askopenfilenames()
    if file_paths:
        generator = MarkovChainTextGenerator()
        generator.build_chain(file_paths)
        generated_text = generator.generate_text()
        text_widget.configure(state='normal')
        text_widget.delete('1.0', tk.END)
        text_widget.insert(tk.END, generated_text)
        text_widget.configure(state='disabled')
        retry_button.config(state="normal")

def retry(text_widget, retry_button):
    global generator
    global engine
    if engine is not None:  # engineがNoneでないことを確認
        engine.stop()
    generated_text = generator.generate_text()
    text_widget.configure(state='normal')
    text_widget.delete('1.0', tk.END)
    text_widget.insert(tk.END, generated_text)
    text_widget.configure(state='disabled')
    read_text(generated_text)

def read_text(text):
    global engine
    engine.say(text)
    engine.runAndWait()

def main():
    root = tk.Tk()
    root.title("マルコフ連鎖で生成した朝の挨拶読み上げ君")

    text_widget = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)
    text_widget.grid(row=0, column=0, columnspan=2)

    # 画像をリサイズして表示する
    try:
        image = Image.open("taiyou.png")  # 画像ファイルのパスを指定(注意team3を開いた状態じゃないと動かないぞ!STEM-HACKから開いたら動かなかった!ファイルパスのせい!)
        resized_image = image.resize((100, 100))  # 100x100にリサイズ
        photo = ImageTk.PhotoImage(resized_image)
        label = tk.Label(root, image=photo)
        label.image = photo
        label.grid(row=0, column=2, rowspan=2, padx=10, pady=10)
    except FileNotFoundError:
        not_found_label = tk.Label(root, text="NotFound")
        not_found_label.grid(row=0, column=2, rowspan=2, padx=10, pady=10)

    select_button = tk.Button(root, text="Select Files", command=lambda: select_files(text_widget, retry_button))
    select_button.grid(row=1, column=0, sticky="ew", padx=10, pady=10)

    retry_button = tk.Button(root, text="Retry", command=lambda: retry(text_widget, retry_button), state="disabled")
    retry_button.grid(row=1, column=1, sticky="ew", padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()