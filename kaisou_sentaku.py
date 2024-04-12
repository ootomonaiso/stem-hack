#動かない
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from tkinter import scrolledtext
from PIL import Image, ImageTk
import random
import json

class MarkovChainTextGenerator:
    def __init__(self):
        self.chain = None 
        self.order = None

    def build_chain(self, data_files):
        if self.order is None:
            messagebox.showerror("Error", "Markov Chain order is not set.")  
            return
        chain = {} 
        for data_file in data_files:
            with open(data_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
            for sentence in data["sentences"]:
                words = ["<START>"] + sentence + ["<END>"]
                for i in range(len(words) - self.order):
                    current_words = tuple(words[i:i+self.order])
                    next_word = words[i + self.order]
                    if current_words not in chain:
                        chain[current_words] = []
                    chain[current_words].append(next_word)
        self.chain = chain 

    def generate_text(self, max_length=100):
        if self.chain is None:
            return "Error: Chain not built. Please load data first."
        
        text = []
        current_words = ("<START>",) * self.order  
        while len(text) < max_length:
            if current_words not in self.chain:
                break
            next_word_options = self.chain[current_words]
            next_word = random.choice(next_word_options)
            if next_word == "<END>":
                break
            text.append(next_word)
            current_words = tuple(list(current_words[1:]) + [next_word])
        generated_text = " ".join(text)
        return generated_text

def select_files(text_widget, retry_button):
    global generator
    file_paths = filedialog.askopenfilenames()
    if file_paths:
        order = simpledialog.askinteger("Order of Markov Chain", "Enter the order of Markov Chain:")  
        if order is not None:  
            generator = MarkovChainTextGenerator() 
            generator.order = order  
            generator.build_chain(file_paths)
            generated_text = generator.generate_text() 
            text_widget.configure(state='normal') 
            text_widget.delete('1.0', tk.END) 
            text_widget.insert(tk.END, generated_text) 
            text_widget.configure(state='disabled') 
            retry_button.config(state="normal")

def retry(text_widget, retry_button):
    global generator
    if generator is None or generator.order is None:  
        messagebox.showerror("Error", "Markov Chain is not initialized.")  
        return
    
    generated_text = generator.generate_text() 
    text_widget.configure(state='normal') 
    text_widget.delete('1.0', tk.END) 
    text_widget.insert(tk.END, generated_text) 
    text_widget.configure(state='disabled') 

def main():
    root = tk.Tk() 
    root.title("出来損ないのマルコフ連鎖式朝の挨拶生成機") 

    text_widget = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10) 
    text_widget.grid(row=0, column=0, columnspan=2) 

    try:
        image = Image.open("taiyou.png") 
        resized_image = image.resize((100, 100)) 
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