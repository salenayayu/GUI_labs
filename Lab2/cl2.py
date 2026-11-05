import tkinter as tk


class CurrencyField(tk.Frame):
    def __init__(self, parent, title):
        super().__init__(parent)
        tk.Label(self, text=title, width=16, anchor="w").pack(side="left")
        self.value = tk.StringVar()
        tk.Entry(self, textvariable=self.value, width=22).pack(side="left")