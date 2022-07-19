from tkinter import Tk, RIGHT, BOTH, RAISED, LEFT, Text, BOTTOM, Button, END
from tkinter.ttk import Frame, Style
from matplotlib.pyplot import get

import time
import requests
import os

current_time = ''.join(str(x) for x in time.localtime()[0:3])
valid_key = open("time.txt", "r")
path = "https://developers.lingvolive.com/api/v1.1/authenticate"
if valid_key.read() != current_time or not open("api_token.txt", "r").read():
    valid_key = open("time.txt", "w+")
    valid_key.write(current_time)
    valid_key.close()
    with open("APIkey.txt", "r") as file:
        headers = {"Authorization ": "Basic " + file.read()}
        result = requests.post(url=path, headers=headers)
        file_with_token = open("api_token.txt", "w+")
        file_with_token = open("api_token.txt", "a")
        file_with_token.write(result.text)
        file_with_token.close()


def get_translate(value):
    minicard_path = "https://developers.lingvolive.com/api/v1/Minicard"
    params = {"text": value, "srcLang": 1033, "dstLang": 1049}
    try:
        token = open("api_token.txt", "r")
        headers = {"Authorization ": "Bearer " + token.read()}
        result = requests.get(minicard_path, params=params, headers=headers)
        with open("output.txt", "w+") as output:
            output.seek(0)
            output.write(str(result.json()))
        return result.json()

    except FileNotFoundError as error:
        print("can't open file ", error)


class Example(Frame):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.master.title("Переводчик")
        self.style = Style()
        self.style.theme_use("default")

        frame = Frame(self, relief=RAISED, borderwidth=3, width=600,
                      height=180)
        # frame.pack(fill=BOTH, expand=True)
        frame.pack(side=LEFT)
        frame.pack_propagate(False)

        self.text = Text(master=frame, font=("Arial", 24))
        self.text.place(x=1, y=1, width=280, height=170)

        self.output = Text(master=frame, width=380, font=("Arial", 24))
        self.output.place(x=300, y=0, width=280, height=170)
        self.pack(fill=BOTH, expand=True)

        btn_frame = Frame()
        btn_frame.pack(side=BOTTOM, expand=True, fill=BOTH)
        translateButton = Button(master=btn_frame, text="Перевести",
                                 background='grey', font=("Arial", 29),
                                 foreground="blue", command=self.translate)
        translateButton.pack()

    def translate(self):
        value = self.text.get(1.0, END)
        json = get_translate(value)

        self.output.delete(1.0, END)
        self.output.insert(1.0, json["Translation"]["Translation"])


def main():
    result = 0
    root = Tk()
    root.geometry("600x220+600+300")
    root.resizable(0, 0)
    app = Example()
    root.mainloop()


if __name__ == '__main__':
    main()
