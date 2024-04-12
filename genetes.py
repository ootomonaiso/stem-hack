import tkinter as tk #GUI
from tkinter import filedialog #GUI
from tkinter import scrolledtext #GUI
from PIL import Image, ImageTk #GUI
import random 
import json

class MarkovChainTextGenerator:
    def __init__(self): #初期化
        self.chain = None 

    def build_chain(self, data_files): #チェーン構築
        chain = {} 
        for data_file in data_files:
            with open(data_file, 'r', encoding='utf-8') as file: #utf8を信じている
                data = json.load(file) #jsonファイルの読み込み
            for sentence in data["sentences"]: #データの走査開始
                words = ["<START>"] + sentence + ["<END>"]
                for i in range(len(words) - 1):
                    current_word = words[i] #現在の単語を取得
                    next_word = words[i + 1] #次の単語取得
                    if current_word not in chain: #現在の単語がチェーンにないなら
                        chain[current_word] = [] #現在の単語をキーとして空リストへ
                    chain[current_word].append(next_word)  #現在の単語を次の単語につける
        self.chain = chain #チェーン更新

    def generate_text(self, max_length=100): #テキスト生成
        if self.chain is None: #もしチェーンがnoneならエラーを出す(起こるはずがないと信じてる)
            return "Error: Chain not built. Please load data first."
        
        text = [] #初期化
        current_word = "<START>" #現在の単語に開始タグをつけて処理
        while len(text) < max_length: #テキストの長さは最大長未満か?
            if current_word not in self.chain: #現在の単語がチェーンにないならば
                break 
            next_word_options = self.chain[current_word] #次の単語情報を取得
            next_word = random.choice(next_word_options) #ランダムに次の単語を選択
            if next_word == "<END>": #終了タグが付いたなら終わる
                break
            text.append(next_word) #次の単語をtextに追加する
            current_word = next_word #現在の単語を更新
        return " ".join(text) #スペース入れて返す(動作確認のため)

def select_files(text_widget, retry_button): #jsonファイルの選択するやつ
    global generator
    file_paths = filedialog.askopenfilenames(filetypes=[("JSON files", "*.json")]) #jsonファイルのみ表示させる
    if file_paths:
        generator = MarkovChainTextGenerator() #ダイヤログでファイル
        generator.build_chain(file_paths) #チェーン構築
        generated_text = generator.generate_text() #生成したテキストを連れてくる
        text_widget.configure(state='normal') 
        text_widget.delete('1.0', tk.END) #中身クリア
        text_widget.insert(tk.END, generated_text)#生成したテキストを挿入
        text_widget.configure(state='disabled') #編集できなくなってるはずどうだろう
        retry_button.config(state="normal")
        # ログをだすぞ
        with open("text_generation_log.txt", "a", encoding="utf-8") as log_file:
            log_file.write("Generated Text:\n" + generated_text + "\n\n")

def retry(text_widget, retry_button):#リトライボタンが押された後の処理
    global generator
    generated_text = generator.generate_text()
    text_widget.configure(state='normal') #編集可能に
    text_widget.delete('1.0', tk.END) #テキスト削除
    text_widget.insert(tk.END, generated_text) #テキスト挿入
    text_widget.configure(state='disabled') #編集不可に
    with open("text_generation_log.txt", "a", encoding="utf-8") as log_file:#utf8で書き出し
        log_file.write("Generated Text:\n" + generated_text + "\n\n") #1行開けて書き込むように調整

def main(): 
    root = tk.Tk()
    root.title("マルコフ連鎖式朝の挨拶生成機")

    text_widget = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10) #スクロールできるテキストボックス
    text_widget.grid(row=0, column=0, columnspan=2)

    try: #太陽の画像を差し込み
        image = Image.open("taiyou.png")
        resized_image = image.resize((100, 100))
        photo = ImageTk.PhotoImage(resized_image)
        label = tk.Label(root, image=photo)
        label.image = photo
        label.grid(row=0, column=2, rowspan=2, padx=10, pady=10)
    except FileNotFoundError:#見つからなかったらNotFoundと書き込み
        not_found_label = tk.Label(root, text="NotFound")
        not_found_label.grid(row=0, column=2, rowspan=2, padx=10, pady=10)

    select_button = tk.Button(root, text="Select Files", command=lambda: select_files(text_widget, retry_button))
    select_button.grid(row=1, column=0, sticky="ew", padx=10, pady=10)

    retry_button = tk.Button(root, text="Retry", command=lambda: retry(text_widget, retry_button), state="disabled")
    retry_button.grid(row=1, column=1, sticky="ew", padx=10, pady=10)
    root.mainloop()

if __name__ == "__main__":
    main()