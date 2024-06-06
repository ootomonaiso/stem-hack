import tkinter as tk  
from tkinter import messagebox  
import MeCab  
import json  

class TrainingDataGUI:
    def __init__(self, master):  # GUIの実装
        self.master = master  # インスタンス保持
        master.title("データ登録用ソフトウェア")  # タイトル設定

        self.label = tk.Label(master, text="Enter Text:", font=("Helvetica", 16))  # テキスト入力ラベル
        self.label.pack()  # ラベルをメインウィンドウに配置

        self.text_entry = tk.Text(master, height=5)  # テキストボックスを作成
        self.text_entry.pack()  # テキストボックスをメインウィンドウに配置

        self.register_button = tk.Button(master, text="Register", command=self.register_text)  # テキストを登録するためのボタンを作成
        self.register_button.pack()  # ボタンをメインウィンドウに配置

    def tokenize(self, text):  # テキストをmecabでトークンにする処理
        tagger = MeCab.Tagger('-Owakati')  # MeCabの形態素解析器を初期化
        tokens = tagger.parse(text).split()  # 入力テキストを形態素解析し、トークンのリストを取得
        return tokens  # トークンのリストを返す

    def preprocess_text(self, text):
        return self.tokenize(text)
     
    def register_text(self):
        # テキスト入力ボックスから入力された文字列を取得
        new_text = self.text_entry.get("1.0", "end-1c").strip()  # テキストボックスに入力された文字列を取得し、先頭と末尾の空白を削除
        if not new_text:  # 入力された文字列が空の場合
            messagebox.showwarning("待ってくれ", "文字を入力してから実行してくれ")  # 警告メッセージボックスを表示
            return  # register_textメソッドを終了

        try:
            # greetings.jsonファイルを読み込む
            with open('greetings.json', 'r', encoding='utf-8') as file:  # greetings.jsonファイルを読み込みモードで開く
                data = json.load(file)  # JSONデータを読み込む
        except FileNotFoundError:  # ファイルが存在しない場合
            # ファイルが存在しない場合は新しいデータを作成
            data = {"sentences": []}  # 空のデータ辞書を作成

        # 前処理済みのテキストをデータに追加
        data["sentences"].append(self.preprocess_text(new_text))  # 前処理済みのテキストをデータに追加

        # 更新されたデータをgreetings.jsonに書き込む
        with open('greetings.json', 'w', encoding='utf-8') as file:  # greetings.jsonファイルを書き込みモードで開く
            json.dump(data, file, ensure_ascii=False, indent=4)  # JSONデータを書き込む（UTF-8で出力、インデント付き）

        messagebox.showinfo("Information", "Text registered successfully.")  # 登録完了のメッセージボックスを表示

# メインループ
def main():
    root = tk.Tk()  # メインウィンドウを作成
    app = TrainingDataGUI(root)  # TrainingDataGUIクラスのインスタンスを作成
    root.mainloop()  # メインループを開始

# スクリプトが直接実行された場合のみmain()を呼び出す
if __name__ == "__main__":
    main()