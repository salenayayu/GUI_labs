import math
import tkinter as tk

from Lab2 import cl1, cl2


class Some(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Конвертер валют")
        self.resizable(False, False)
        self.data = cl1.Data()
        self.updating = False

        tk.Label(self, text="Измените сумму в любом поле:").pack(pady=10)
        self.fields = {}
        for currency, title in [("RUB", "Рубли"), ("USD", "Доллары"), ("EUR", "Евро")]:
            field = cl2.CurrencyField(self, title)
            field.pack(padx=15, pady=5)
            self.fields[currency] = field
            field.value.trace_add("write", lambda *args, code=currency: self.convert(code))

        tk.Label(self, text="Условные курсы: 1 USD = 90 RUB; 1 EUR = 100 RUB").pack(padx=15, pady=10)
        self.message = tk.Label(self, text="", fg="red")
        self.message.pack(pady=5)
        self.fields["USD"].value.set("1")

    def convert(self, currency):
        if self.updating:
            return
        text = self.fields[currency].value.get().strip().replace(",", ".")
        if not text:
            self.message.config(text="Введите сумму")
            return
        try:
            amount = float(text)
            if not math.isfinite(amount) or amount < 0 or amount > 1_000_000_000:
                raise ValueError
        except ValueError:
            self.message.config(text="Введите число от 0 до 1 000 000 000")
            return

        self.message.config(text="")
        self.data.setData(amount, currency)
        # блокировка повторных вызовов при обновлении остальных полей.
        self.updating = True
        try:
            for code, value in zip(("RUB", "USD", "EUR"), self.data.getData()):
                if code != currency:
                    self.fields[code].value.set(f"{value:.2f}")
        finally:
            self.updating = False


if __name__ == "__main__":
    window = Some()
    window.mainloop()