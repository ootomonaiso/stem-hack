import tkinter as tk  # GUI
from tkinter import messagebox  # GUI
import MeCab  # 分かち書きマン
import json  # Jsonファイル処理

class TrainingDataGUI:
    def __init__(self, master):  # GUIの実装
        self.master = master
        master.title("データ登録用ソフトウェア")

        self.label = tk.Label(master, text="Enter Text:", font=("Helvetica", 16))
        self.label.pack()

        self.text_entry = tk.Text(master, height=5)
        self.text_entry.pack()

        self.register_button = tk.Button(master, text="Register", command=self.register_text)
        self.register_button.pack()

    def tokenize(self, text):  # テキストをmecabでトークンにする処理
        tagger = MeCab.Tagger('-Owakati')
        tokens = tagger.parse(text).split()
        return tokens

    def preprocess_text(self, text):
        return self.tokenize(text)

    def register_text(self):
        new_text = self.text_entry.get("1.0", "end-1c").strip()
        if not new_text:
            messagebox.showwarning("待ってくれ", "文字を入力してから実行してくれ")
            return

        try:
            with open('greetings.json', 'r', encoding='utf-8') as file:  # utf-8でエンコードしたJsonファイルを探す
                data = json.load(file)
        except FileNotFoundError:
            data = {"sentences": []}  # ないなら作る

        data["sentences"].append(self.preprocess_text(new_text))

        with open('greetings.json', 'w', encoding='utf-8') as file:  # UTF8で書き込む
            json.dump(data, file, ensure_ascii=False, indent=4)  # indentを追加して見やすくする

        messagebox.showinfo("Information", "Text registered successfully.")  # 登録完了のメッセージボックス

def main():
    root = tk.Tk()
    app = TrainingDataGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()